"""Bounded C16 formation; evaluator labels never enter observation or matching."""

from __future__ import annotations

import copy
import itertools

import numpy as np

from sparkbrain.v03_seed.concepts import ConceptFormationConfig, OnlineConceptFormer

from .learning import encode, normalize, vector
from .worlds import canonical, digest, text_hash


def cosine(left: list, right: list) -> float:
    return float(np.clip(np.dot(left, right), -1.0, 1.0))


class ConceptBank:
    def __init__(self, protocol: dict, run_seed: int, representation: str,
                 discovery_order: str, encoder: dict | None = None,
                 bank_kind: str = "primary") -> None:
        if representation not in protocol["scope"]["primary_representations"]:
            raise ValueError("unregistered representation")
        if discovery_order not in protocol["scope"]["discovery_orders"]:
            raise ValueError("unregistered discovery order")
        if bank_kind not in protocol["scope"]["bank_kinds"]:
            raise ValueError("unregistered bank kind")
        if (representation == "learned_local_prototype") != (encoder is not None):
            raise ValueError("learned representation requires its fixed encoder only")
        self.protocol = copy.deepcopy(protocol)
        self.identity = dict(run_seed=run_seed, representation=representation,
                             bank_kind=bank_kind, discovery_order=discovery_order)
        self.encoder = copy.deepcopy(encoder)
        self.features = [f'{protocol["world_generator"]["modality"]}:{channel}'
                         for channel in protocol["world_generator"]["channels"]]
        self.config_hash = digest({
            "representation_spec": protocol["representations"][representation],
            "formation_spec": protocol["formation"], "channel_map": self.features,
            "control_spec_for_kind": None if bank_kind == "primary"
            else protocol["matched_controls"],
        })
        self._seen: dict[str, str] = {}
        self._live: dict[str, dict] = {}
        self._retired: dict[str, dict] = {}
        self._births = 0
        self._frozen = False
        self._slots: list[str | None] | None = None
        self._source = None
        self._source_ids: dict[str, str] = {}
        if representation == "cc0_assembly" and bank_kind == "primary":
            self._source = OnlineConceptFormer(ConceptFormationConfig(.70, 3, 2, .60, 8))

    @property
    def slot_candidate_ids(self) -> list:
        ids = sorted(self._live) if self._slots is None else list(self._slots)
        return ids + [None] * (self.protocol["formation"]["capacity"] - len(ids))

    def freeze(self) -> None:
        if not self._frozen:
            self._slots = self.slot_candidate_ids
            self._frozen = True

    def candidates(self) -> list[dict]:
        return copy.deepcopy(sorted([*self._live.values(), *self._retired.values()],
                                    key=lambda row: row["birth_ordinal"]))

    def _source_state(self) -> dict | None:
        if self._source is None:
            return None
        return {
            "feature_counts": dict(sorted(self._source.feature_counts.items())),
            "pair_counts": [{"left_feature_id": left, "right_feature_id": right, "count": n}
                            for (left, right), n in sorted(self._source.pair_counts.items())],
            "concepts": [{"source_candidate_id": c.concept_id, "members": list(c.members),
                          "strength": c.strength, "observations": c.observations,
                          "reuse_count": c.reuse_count, "first_seen": c.first_seen,
                          "last_seen": c.last_seen} for c in self._source.candidates()],
            "id_mapping": [{"source_candidate_id": source, "candidate_id": candidate}
                           for source, candidate in sorted(self._source_ids.items())],
        }

    def state(self) -> dict:
        return copy.deepcopy({
            "schema_version": "0.3", "bank": self.identity, "config_hash": self.config_hash,
            "accepted_observation_count": len(self._seen),
            "seen_observations": [{"observation_id": key, "vector_sha256": value}
                                  for key, value in sorted(self._seen.items())],
            "birth_counter": self._births,
            "live_candidates": sorted(self._live.values(), key=lambda row: row["birth_ordinal"]),
            "retired_candidates": sorted(self._retired.values(),
                                         key=lambda row: row["birth_ordinal"]),
            "cc0_source_state": self._source_state(),
        })

    def hash(self) -> str:
        return digest(self.state())

    def _representation(self, x: list) -> list | None:
        if self.identity["representation"] == "cc0_assembly":
            return None
        return encode(x, self.encoder)

    def _feature_ids(self, x: list) -> list[str]:
        return [name for name, value in zip(self.features, x, strict=True) if value != 0]

    def _match(self, x: list, z: list | None, exclude_id: str | None = None,
               *, raw_cosine: bool = False) -> tuple[str | None, float | None, str | None]:
        active = set(self._feature_ids(x))
        assembly = self.identity["representation"] == "cc0_assembly"
        if (assembly and not active) or (not assembly and z is None):
            return None, None, "zero_norm"
        matches = []
        for candidate_id, candidate in self._live.items():
            if candidate_id == exclude_id:
                continue
            if assembly:
                members = candidate["member_feature_ids"]
                score = len(active.intersection(members)) / len(members)
                eligible = score >= .60
            else:
                raw = cosine(z, candidate["prototype"])
                eligible = raw >= .8
                score = raw if raw_cosine else raw - .05 * candidate["usage"]
            if eligible:
                matches.append((-score, candidate_id))
        if not matches:
            return None, None, "no_eligible_candidate"
        negative_score, candidate_id = min(matches)
        return candidate_id, -negative_score, None

    def query(self, x: object, exclude_id: str | None = None) -> dict:
        values = vector(x)
        if exclude_id is not None and exclude_id not in self._live:
            raise ValueError("excluded candidate is not live in this bank")
        winner, score, reason = self._match(values, self._representation(values), exclude_id)
        return {"winner_id": winner, "slot_index": None if winner is None
                else self.slot_candidate_ids.index(winner), "match_score": score,
                "no_match_reason": reason}

    def _birth(self, prototype: list | None, exemplars: list, frame: int | None,
               *, parents: list | None = None, usage: float = 0.0,
               source_id: str | None = None, pattern_id: str | None = None,
               members: list | None = None) -> dict:
        ident = self.identity
        prefix = "ca-" if ident["bank_kind"] == "primary" else "rf-"
        text = (f'c16|{ident["bank_kind"]}|{ident["representation"]}|{ident["run_seed"]}|'
                f'{ident["discovery_order"]}|{self._births}')
        candidate_id = prefix + text_hash(text)[:24]
        retained = sorted(exemplars, key=lambda row: (row["global_frame_index"],
                                                    row["observation_id"]))[-32:]
        candidate = {
            "candidate_id": candidate_id, "birth_ordinal": self._births, "status": "active",
            "parent_ids": sorted(parents or []), "source_candidate_id": source_id,
            "pattern_id": pattern_id, "prototype": copy.deepcopy(prototype),
            "member_feature_ids": sorted(members) if members is not None else sorted({
                feature for row in retained for feature in row["feature_ids"]}),
            "retained_exemplars": copy.deepcopy(retained), "usage": float(usage),
            "first_seen": frame, "last_seen": max((r["global_frame_index"] for r in retained),
                                                  default=frame),
        }
        self._births += 1
        self._live[candidate_id] = candidate
        return candidate

    def _retire(self, candidate_id: str) -> dict:
        candidate = self._live.pop(candidate_id)
        candidate["status"] = "retired"
        self._retired[candidate_id] = candidate
        return candidate

    def _event(self, events: list, operation: str, candidate: dict | None,
               *, before: dict | None = None, reason: str | None = None,
               births: int = 0) -> None:
        events.append({
            "event_index": len(events), "operation": operation,
            "candidate_id": None if candidate is None else candidate["candidate_id"],
            "parent_ids": [] if candidate is None else list(candidate["parent_ids"]),
            "reason": reason,
            "prototype_before": None if before is None else copy.deepcopy(before["prototype"]),
            "prototype_after": None if candidate is None else copy.deepcopy(candidate["prototype"]),
            "member_feature_ids": [] if candidate is None
            else list(candidate["member_feature_ids"]),
            "retained_observation_ids": [] if candidate is None else [
                row["observation_id"] for row in candidate["retained_exemplars"]],
            "usage_before": None if before is None else before["usage"],
            "usage_after": None if candidate is None else candidate["usage"],
            "births_consumed": births, "candidate_count_after": len(self._live),
        })

    def _retain(self, candidate: dict, exemplar: dict) -> None:
        candidate["retained_exemplars"] = sorted(
            [*candidate["retained_exemplars"], exemplar],
            key=lambda row: (row["global_frame_index"], row["observation_id"]),
        )[-self.protocol["formation"]["maximum_retained_exemplars_per_candidate"]:]
        if self.identity["representation"] != "cc0_assembly":
            candidate["member_feature_ids"] = sorted({
                feature for row in candidate["retained_exemplars"]
                for feature in row["feature_ids"]})

    def _observe_assembly(self, values: list, exemplar: dict, frame: int, events: list) -> tuple:
        previous = {c.concept_id: c for c in self._source.candidates()}
        before = copy.deepcopy(self._live)
        source_candidates = self._source.observe(self._feature_ids(values), time=frame)
        born = set()
        for source in source_candidates:
            if source.concept_id not in self._source_ids:
                candidate = self._birth(None, [], frame, source_id=source.concept_id,
                                        members=list(source.members))
                self._source_ids[source.concept_id] = candidate["candidate_id"]
                born.add(candidate["candidate_id"])
            candidate = self._live[self._source_ids[source.concept_id]]
            candidate["last_seen"] = source.last_seen
        winner, score, reason = self._match(values, None)
        if winner is not None:
            self._retain(self._live[winner], exemplar)
        for source in source_candidates:
            candidate = self._live[self._source_ids[source.concept_id]]
            key = candidate["candidate_id"]
            if key in born:
                self._event(events, "birth", candidate, births=1)
            elif source != previous[source.concept_id] or key == winner:
                self._event(events, "update", candidate, before=before[key])
        return winner, score, reason

    def _split(self, original: set, frame: int, events: list) -> set:
        choices = []
        for key in sorted(original.intersection(self._live)):
            candidate = self._live[key]
            rows = candidate["retained_exemplars"]
            dispersion = float(np.mean([np.sum((np.asarray(r["representation"])
                                                - candidate["prototype"]) ** 2) for r in rows]))
            if dispersion > .2:
                choices.append((-dispersion, key))
        if not choices:
            return set()
        _, key = min(choices)
        parent = self._live[key]
        rows = sorted(parent["retained_exemplars"], key=lambda row: row["observation_id"])
        pairs = [(-float(np.sum((np.asarray(a["representation"])
                                 - b["representation"]) ** 2)), a["observation_id"],
                  b["observation_id"], a, b) for a, b in itertools.combinations(rows, 2)]
        if not pairs:
            return set()
        _, _, _, left, right = min(pairs, key=lambda item: item[:3])
        groups = [[], []]
        for row in rows:
            distances = [float(np.sum((np.asarray(row["representation"])
                                      - pivot["representation"]) ** 2)) for pivot in (left, right)]
            groups[0 if distances[0] <= distances[1] else 1].append(row)
        reason = None
        means = []
        if any(len(group) < 4 for group in groups):
            reason = "minimum_child_exemplars"
        else:
            means = [normalize(np.mean([r["representation"] for r in group], axis=0))
                     for group in groups]
            if any(mean is None for mean in means):
                reason = "zero_norm"
            elif len(self._live) + 1 > self.protocol["formation"]["capacity"]:
                reason = "capacity"
            elif self._births + 2 > self.protocol["formation"]["maximum_births_per_primary_bank"]:
                reason = "birth_budget"
        if reason is not None:
            self._event(events, "split_rejected", parent, before=parent, reason=reason)
            return set()
        snapshot = copy.deepcopy(parent)
        self._retire(key)
        children = [self._birth(mean, group, frame, parents=[key],
                                usage=snapshot["usage"] * len(group) / len(rows))
                    for mean, group in zip(means, groups, strict=True)]
        for child in children:
            self._event(events, "split", child, before=snapshot, births=1)
        return {key}

    def _merge(self, original: set, operated: set, frame: int, events: list) -> None:
        options, rejected = [], []
        for left_id, right_id in itertools.combinations(sorted(original - operated), 2):
            if left_id not in self._live or right_id not in self._live:
                continue
            left, right = self._live[left_id], self._live[right_id]
            similarity = cosine(left["prototype"], right["prototype"])
            if similarity < .95:
                continue
            union = {r["observation_id"]: r for r in [*left["retained_exemplars"],
                                                      *right["retained_exemplars"]]}
            rows = list(union.values())
            complete = all(cosine(a["representation"], b["representation"]) >= .8
                           for a, b in itertools.combinations(rows, 2))
            (options if complete else rejected).append((-similarity, left_id, right_id, rows))
        if not options:
            if rejected:
                _, key, _, _ = min(rejected, key=lambda item: item[:3])
                self._event(events, "merge_rejected", self._live[key],
                            before=self._live[key], reason="complete_link")
            return
        _, left_id, right_id, rows = min(options, key=lambda item: item[:3])
        left, right = self._live[left_id], self._live[right_id]
        if self._births >= self.protocol["formation"]["maximum_births_per_primary_bank"]:
            self._event(events, "merge_rejected", left, before=left, reason="birth_budget")
            return
        prototype = normalize(np.mean([r["representation"] for r in rows], axis=0))
        if prototype is None:
            raise ValueError("nonzero complete-link union produced zero prototype")
        usage = min(1.0, left["usage"] + right["usage"])
        self._retire(left_id)
        self._retire(right_id)
        child = self._birth(prototype, rows, frame, parents=[left_id, right_id], usage=usage)
        self._event(events, "merge", child, births=1)

    def observe(self, x: object, observation_id: str) -> dict:
        values = vector(x)
        if not isinstance(observation_id, str) or not observation_id.strip():
            raise ValueError("observation_id must be a nonblank opaque string")
        if self._frozen or self.identity["bank_kind"] != "primary":
            raise ValueError("frozen and reference banks cannot observe")
        vector_hash = digest(values)
        before_hash = self.hash()
        if observation_id in self._seen:
            if self._seen[observation_id] != vector_hash:
                raise ValueError("observation identity changed vector")
            return dict(winner_id=None, match_score=None, no_match_reason="duplicate_ignored",
                        events=[], representation_vector=self._representation(values),
                        global_frame_index=None, bank_hash_before=before_hash,
                        bank_hash_after=before_hash)
        if len(self._seen) >= self.protocol["formation"]["max_unique_observations"]:
            raise ValueError("bounded observation registry exhausted")
        z = self._representation(values)
        frame = len(self._seen)
        self._seen[observation_id] = vector_hash
        exemplar = dict(observation_id=observation_id, global_frame_index=frame,
                        feature_ids=self._feature_ids(values), emitted_vector=values,
                        representation=z)
        events = []
        if self._source is not None:
            winner, score, reason = self._observe_assembly(values, exemplar, frame, events)
        else:
            original = set(self._live)
            for key in sorted(original):
                candidate = self._live[key]
                previous = copy.deepcopy(candidate)
                idle = frame - candidate["last_seen"]
                if idle >= 32:
                    self._event(events, "delete", self._retire(key), before=previous)
            for key in sorted(self._live):
                candidate = self._live[key]
                previous = copy.deepcopy(candidate)
                idle = frame - candidate["last_seen"]
                if idle >= 16 and candidate["status"] != "dormant":
                    candidate["status"] = "dormant"
                    self._event(events, "dormant", candidate, before=previous)
            winner, score, reason = self._match(values, z)
            for key in sorted(self._live):
                candidate = self._live[key]
                previous = copy.deepcopy(candidate)
                candidate["usage"] = .95 * candidate["usage"] + .05 * (key == winner)
                if key == winner:
                    candidate["prototype"] = normalize(.9 * np.asarray(candidate["prototype"])
                                                       + .1 * np.asarray(z))
                    if candidate["prototype"] is None:
                        raise ValueError("matched update produced zero prototype")
                    candidate["last_seen"] = frame
                    self._retain(candidate, exemplar)
                    if candidate["status"] == "dormant":
                        candidate["status"] = "active"
                        self._event(events, "awaken", candidate, before=previous)
                    self._event(events, "update", candidate, before=previous)
            if winner is None and z is not None:
                if len(self._live) >= self.protocol["formation"]["capacity"]:
                    reason = "capacity"
                elif self._births >= self.protocol["formation"]["maximum_births_per_primary_bank"]:
                    reason = "birth_budget"
                else:
                    candidate = self._birth(z, [exemplar], frame)
                    winner, score, reason = candidate["candidate_id"], 1.0, None
                    self._event(events, "birth", candidate, births=1)
                if winner is None:
                    self._event(events, "birth_rejected", None, reason=reason)
            operated = self._split(original, frame, events)
            self._merge(original, operated, frame, events)
        return dict(winner_id=winner, match_score=score, no_match_reason=reason, events=events,
                    representation_vector=z, global_frame_index=frame,
                    bank_hash_before=before_hash, bank_hash_after=self.hash())


def build_controls(primary: ConceptBank, train_frames: list[dict]) -> tuple[dict, dict]:
    if not primary._frozen or primary.identity["bank_kind"] != "primary":
        raise ValueError("controls require a frozen primary bank")
    if len(train_frames) != 288:
        raise ValueError("controls require288 canonical base-train frames")
    groups = {}
    for frame in train_frames:
        values = vector(frame["emitted_vector"])
        features = primary._feature_ids(values)
        if not features:
            continue
        pattern_id = "pa-" + text_hash(canonical(features))[:24]
        group = groups.setdefault(pattern_id, dict(features=features, vectors=[], episodes=set()))
        group["vectors"].append(values)
        group["episodes"].add(frame["episode_id"])
    inventory = []
    for pattern_id, group in sorted(groups.items()):
        if primary.identity["representation"] == "cc0_assembly":
            mean, eligible = None, True
        else:
            vectors = [primary._representation(x) for x in group["vectors"]]
            # Preserve the entire group's fixed denominator even for zero latent directions.
            dimension = 4 if primary.encoder is not None else 12
            directions = [z if z is not None else [0.0] * dimension for z in vectors]
            mean = normalize(np.mean(directions, axis=0))
            eligible = mean is not None
        inventory.append(dict(pattern_id=pattern_id, feature_ids=group["features"],
                              frame_count=len(group["vectors"]),
                              distinct_episode_count=len(group["episodes"]),
                              mean_representation=mean, eligible=eligible))
    banks, construction = {}, []
    ident = primary.identity
    target_count = len(primary._live)
    for kind in ("matched_random", "frequency_topk"):
        bank = ConceptBank(primary.protocol, ident["run_seed"], ident["representation"],
                           ident["discovery_order"], primary.encoder, kind)
        if kind == "matched_random":
            ranking = sorted(inventory, key=lambda row: (
                text_hash(f'c16|random|{ident["run_seed"]}|{ident["representation"]}|'
                          f'{ident["discovery_order"]}|{row["pattern_id"]}'), row["pattern_id"]))
        else:
            ranking = sorted(inventory, key=lambda row: (-row["frame_count"], row["pattern_id"]))
        selected = [row for row in ranking if row["eligible"]][:target_count]
        for row in selected:
            bank._birth(row["mean_representation"], [], None, pattern_id=row["pattern_id"],
                        members=row["feature_ids"])
        if ident["representation"] != "cc0_assembly":
            for frame in train_frames:
                x = vector(frame["emitted_vector"])
                winner, _, _ = bank._match(x, bank._representation(x), raw_cosine=True)
                for key, candidate in bank._live.items():
                    candidate["usage"] = .95 * candidate["usage"] + .05 * (key == winner)
        bank.freeze()
        banks[kind] = bank
        construction.append({
            "bank_kind": kind, "primary_count": target_count,
            "reference_count": len(selected), "shortfall": target_count - len(selected),
            "selection_order_pattern_ids": [row["pattern_id"] for row in selected],
            "slot_candidate_ids": bank.slot_candidate_ids,
            "references": [{"reference_id": row["candidate_id"], "pattern_id": row["pattern_id"],
                            "member_feature_ids": row["member_feature_ids"],
                            "prototype": row["prototype"], "train_usage": row["usage"],
                            "grade": None, "qualification": "reference_control_not_discovered"}
                           for row in bank.candidates()],
            "bank_hash": bank.hash(),
        })
    return banks, {
        "schema_version": "0.3", "protocol_id": primary.protocol["protocol_id"],
        "source_commit": primary.protocol["source_commit"], "row_kind": "control",
        "run_seed": ident["run_seed"], "representation": ident["representation"],
        "discovery_order": ident["discovery_order"], "pattern_inventory": inventory,
        "reference_banks": construction,
    }
