from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CreateRunRequest(StrictModel):
    seed: int = 7
    blind: bool = False


class InjectEventRequest(StrictModel):
    target: str
    label: str
    strength: float = Field(default=1.0, ge=-10.0, le=10.0)
    time: float | None = Field(default=None, ge=0.0)


class InterventionRequest(StrictModel):
    kind: Literal[
        "ablate_edge",
        "edit_edge",
        "clamp_spark",
        "ablate_spark",
        "suppress_organ",
        "set_threshold",
    ]
    source: str | None = None
    target: str | None = None
    spark_id: str | None = None
    organ: str | None = None
    value: float | None = None

    @model_validator(mode="after")
    def validate_target(self) -> InterventionRequest:
        if self.kind in {"ablate_edge", "edit_edge"} and not (self.source and self.target):
            raise ValueError("edge interventions require source and target")
        if self.kind in {"clamp_spark", "ablate_spark", "set_threshold"} and not self.spark_id:
            raise ValueError("Spark intervention requires spark_id")
        if self.kind == "suppress_organ" and not self.organ:
            raise ValueError("organ intervention requires organ")
        if self.kind in {"edit_edge", "clamp_spark", "set_threshold"} and self.value is None:
            raise ValueError("intervention requires value")
        return self


class ComparisonRequest(StrictModel):
    left_run_id: str
    right_run_id: str
    cursor: int = Field(default=0, ge=0)


class ImportRunRequest(StrictModel):
    bundle: dict
