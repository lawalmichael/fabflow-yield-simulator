import math
from typing import Dict, Any, List

import numpy as np
import pandas as pd

from .models import ProcessFlow


def poisson_die_yield(defects: float, wafer_area_cm2: float, die_area_cm2: float) -> float:
    d = defects / wafer_area_cm2
    return math.exp(-d * die_area_cm2)


def compute_yield_metrics(
    defects_by_step: Dict[str, float],
    wafer_area_cm2: float,
    die_area_cm2: float,
    dies_per_wafer: int,
) -> Dict[str, Any]:
    die_yield_by_step: Dict[str, float] = {}
    yield_loss_by_step: Dict[str, float] = {}

    for step_name, defects in defects_by_step.items():
        y = poisson_die_yield(defects, wafer_area_cm2, die_area_cm2)
        die_yield_by_step[step_name] = y
        yield_loss_by_step[step_name] = 1.0 - y

    final_die_yield = 1.0
    for y in die_yield_by_step.values():
        final_die_yield *= y

    expected_good_dies = final_die_yield * dies_per_wafer
    total_defects = float(sum(defects_by_step.values()))

    return {
        "totalDefects": total_defects,
        "defectsByStep": defects_by_step,
        "dieYieldByStep": die_yield_by_step,
        "yieldLossByStep": yield_loss_by_step,
        "finalDieYield": final_die_yield,
        "expectedGoodDies": expected_good_dies,
        "diesPerWafer": dies_per_wafer,
    }


def simulate_lot(
    num_wafers: int,
    num_dies_per_wafer: int,
    process_flow: ProcessFlow,
    seed: int = 42,
    wafer_diameter_mm: float = 300.0,
    edge_exclusion_mm: float = 3.0,
    die_area_mm2: float = 100.0,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    effective_diameter_mm = wafer_diameter_mm - 2.0 * edge_exclusion_mm
    wafer_radius_cm = (effective_diameter_mm / 2.0) / 10.0
    wafer_area_cm2 = math.pi * (wafer_radius_cm ** 2)

    die_area_cm2 = die_area_mm2 / 100.0

    rows: List[Dict[str, Any]] = []

    for wafer_id in range(1, num_wafers + 1):
        cumulative_defects = 0.0
        cumulative_time = 0.0

        defects_by_step: Dict[str, float] = {}

        for step_idx, step in enumerate(process_flow.steps, start=1):
            tool_up = rng.random() < step.tool_uptime

            wait_time = 0.0
            if not tool_up:
                wait_time = float(rng.integers(10, 61))

            variability_multiplier = float(np.exp(rng.normal(0.0, step.sigma)))
            lam = max(step.base_defects_per_wafer * variability_multiplier, 0.0001)
            defects_added = float(rng.poisson(lam))

            did_rework = rng.random() < step.rework_prob
            rework_defects = 0.0
            rework_time = 0.0
            if did_rework:
                rework_time = float(step.cycle_time_min * 0.6)
                rework_defects = float(rng.poisson(max(0.3 * lam, 0.0001)))

            step_time = float(step.cycle_time_min + wait_time + rework_time)
            cumulative_time += step_time

            cumulative_defects += defects_added + rework_defects
            step_total_defects = defects_added + rework_defects
            defects_by_step[step.name] = float(step_total_defects)

            rows.append(
                {
                    "wafer_id": wafer_id,
                    "step_number": step_idx,
                    "step_name": step.name,
                    "tool_up": bool(tool_up),
                    "wait_time_min": float(wait_time),
                    "cycle_time_min": float(step.cycle_time_min),
                    "rework": bool(did_rework),
                    "defects_added": float(defects_added),
                    "rework_defects": float(rework_defects),
                    "step_time_min": float(step_time),
                    "cumulative_time_min": float(cumulative_time),
                    "cumulative_defects": float(cumulative_defects),
                }
            )

        yield_metrics = compute_yield_metrics(
            defects_by_step=defects_by_step,
            wafer_area_cm2=wafer_area_cm2,
            die_area_cm2=die_area_cm2,
            dies_per_wafer=int(num_dies_per_wafer),
        )

        for r in rows:
            if r["wafer_id"] == wafer_id:
                r["final_die_yield"] = float(yield_metrics["finalDieYield"])
                r["expected_good_dies"] = float(yield_metrics["expectedGoodDies"])

    return pd.DataFrame(rows)
