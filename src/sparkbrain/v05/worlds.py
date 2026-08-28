from __future__ import annotations

import random
from dataclasses import dataclass

from sparkbrain.v04.contracts import SignalPulse


@dataclass(frozen=True, slots=True)
class MotifDefinition:
    name: str
    channels: tuple[str, ...]
    offsets_ms: tuple[float, ...]
    future_event: str
    rewarded_action: str

    def __post_init__(self) -> None:
        if len(self.channels) != len(self.offsets_ms):
            raise ValueError("channels and offsets_ms must have equal length")


@dataclass(frozen=True, slots=True)
class MotifEpisode:
    episode_id: str
    condition: str
    motif_name: str | None
    pulses: tuple[SignalPulse, ...]
    future_event: str | None
    rewarded_action: str | None


# Both hidden generators use exactly the same receptor symbols and total
# timing mass.  Only temporal order differs.  This prevents the runtime from
# solving the task by channel identity or event frequency.
MOTIF_X = MotifDefinition(
    "motif_x",
    ("A", "F", "C"),
    (0.0, 5.0, 7.0),
    "outcome-0",
    "action-0",
)
MOTIF_Y = MotifDefinition(
    "motif_y",
    ("C", "F", "A"),
    (0.0, 5.0, 7.0),
    "outcome-1",
    "action-1",
)


@dataclass(frozen=True, slots=True)
class MotifWorldConfig:
    noise_channels: tuple[str, ...] = tuple("HIJKLMNPQ")
    noise_events: int = 5
    noise_magnitude: float = 0.025
    motif_magnitude: float = 1.18
    duration_ms: float = 28.0
    jitter_ms: float = 0.0
    distractor_events: int = 0


def _motif_pulses(
    motif: MotifDefinition,
    *,
    start_ms: float,
    rng: random.Random,
    config: MotifWorldConfig,
    condition: str,
) -> list[SignalPulse]:
    channels = list(motif.channels)
    offsets = list(motif.offsets_ms)
    if condition == "order_shuffle":
        # Exclude both learned canonical orders from the null control.
        canonical = {MOTIF_X.channels, MOTIF_Y.channels}
        permutations = [
            ("A", "C", "F"),
            ("F", "A", "C"),
            ("F", "C", "A"),
            ("C", "A", "F"),
        ]
        channels = list(permutations[rng.randrange(len(permutations))])
        assert tuple(channels) not in canonical
    elif condition == "timing_shuffle":
        # Preserve channels and event count while changing arrival geometry.
        timing_controls = ((0.0, 7.0, 5.0), (5.0, 0.0, 7.0), (7.0, 5.0, 0.0))
        offsets = list(timing_controls[rng.randrange(len(timing_controls))])
    elif condition == "one_event_omission":
        drop = rng.randrange(len(channels))
        channels.pop(drop)
        offsets.pop(drop)
    pulses: list[SignalPulse] = []
    for channel, offset in zip(channels, offsets, strict=True):
        jitter = rng.uniform(-config.jitter_ms, config.jitter_ms)
        pulses.append(
            SignalPulse(
                time_ms=max(start_ms, start_ms + offset + jitter),
                channel=channel,
                magnitude=config.motif_magnitude,
                novelty=0.25,
                source_id="temporal-input-stream",
            )
        )
    return pulses


def make_episode(
    *,
    seed: int,
    index: int,
    motif: MotifDefinition | None,
    condition: str = "motif",
    start_ms: float = 0.0,
    config: MotifWorldConfig | None = None,
) -> MotifEpisode:
    cfg = config or MotifWorldConfig()
    rng = random.Random((seed + 1) * 100_003 + index * 997 + len(condition) * 17)
    pulses: list[SignalPulse] = []
    total_noise = cfg.noise_events + cfg.distractor_events
    for noise_index in range(total_noise):
        pulses.append(
            SignalPulse(
                time_ms=start_ms + rng.uniform(0.0, cfg.duration_ms),
                channel=rng.choice(cfg.noise_channels),
                magnitude=cfg.noise_magnitude,
                novelty=0.05,
                source_id="background-noise",
                metadata={"noise_index": noise_index},
            )
        )
    if motif is not None and condition != "pure_noise":
        pulses.extend(
            _motif_pulses(
                motif,
                start_ms=start_ms + 8.0,
                rng=rng,
                config=cfg,
                condition=condition,
            )
        )
    return MotifEpisode(
        episode_id=f"seed-{seed}-episode-{index}-{condition}",
        condition=condition,
        motif_name=motif.name if motif is not None else None,
        pulses=tuple(sorted(pulses, key=lambda row: (row.time_ms, row.channel))),
        future_event=motif.future_event if motif is not None else None,
        rewarded_action=motif.rewarded_action if motif is not None else "withhold",
    )


def training_episodes(
    *,
    seed: int,
    count: int = 32,
    start_ms: float = 0.0,
) -> tuple[MotifEpisode, ...]:
    episodes: list[MotifEpisode] = []
    cursor = start_ms
    for index in range(count):
        motif = MOTIF_X if index % 2 == 0 else MOTIF_Y
        episodes.append(
            make_episode(seed=seed, index=index, motif=motif, start_ms=cursor)
        )
        cursor += 220.0
    return tuple(episodes)


def held_out_episodes(
    *,
    seed: int,
    count: int = 16,
    condition: str = "jitter",
    start_ms: float = 10_000.0,
) -> tuple[MotifEpisode, ...]:
    if condition == "jitter":
        cfg = MotifWorldConfig(jitter_ms=0.8, distractor_events=2)
        world_condition = "motif"
    elif condition == "distractor":
        cfg = MotifWorldConfig(jitter_ms=0.35, distractor_events=5)
        world_condition = "motif"
    elif condition == "one_event_omission":
        cfg = MotifWorldConfig(jitter_ms=0.35, distractor_events=2)
        world_condition = "one_event_omission"
    elif condition in {"order_shuffle", "timing_shuffle"}:
        cfg = MotifWorldConfig(jitter_ms=0.0, distractor_events=2)
        world_condition = condition
    elif condition == "pure_noise":
        cfg = MotifWorldConfig(noise_events=10, distractor_events=0)
        world_condition = "pure_noise"
    else:
        raise ValueError(f"unknown held-out condition: {condition}")
    episodes: list[MotifEpisode] = []
    cursor = start_ms
    for index in range(count):
        motif = None if condition == "pure_noise" else (MOTIF_X if index % 2 == 0 else MOTIF_Y)
        episodes.append(
            make_episode(
                seed=seed + 10_000,
                index=index,
                motif=motif,
                condition=world_condition,
                start_ms=cursor,
                config=cfg,
            )
        )
        cursor += 220.0
    return tuple(episodes)
