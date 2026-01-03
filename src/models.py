from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass(frozen=True)
class ProcessStep:
    name: str
    base_defects_per_wafer: float
    sigma: float
    cycle_time_min: float
    rework_prob: float
    tool_uptime: float

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ProcessStep":
        return ProcessStep(
            name=str(d["name"]),
            base_defects_per_wafer=float(d["base_defects_per_wafer"]),
            sigma=float(d["sigma"]),
            cycle_time_min=float(d["cycle_time_min"]),
            rework_prob=float(d["rework_prob"]),
            tool_uptime=float(d["tool_uptime"]),
        )


@dataclass(frozen=True)
class ProcessFlow:
    flow_name: str
    steps: List[ProcessStep]

    @staticmethod
    def from_config(flow_config: Dict[str, Any]) -> "ProcessFlow":
        steps = [ProcessStep.from_dict(s) for s in flow_config["steps"]]
        return ProcessFlow(
            flow_name=str(flow_config.get("flow_name", "Process Flow")),
            steps=steps,
        )
