# Fab Process Flow (v1)

This document defines the 5-step wafer process flow used by the simulator.
Each step includes baseline parameters for defects, variability, rework, cycle time,
and tool availability (uptime). Values are realistic starting assumptions for a
teaching-focused fab model and can be tuned for experiments.

## Step 1 — Lithography
- Base defect rate (defects/wafer): 0.35
- Process variation (sigma): 0.65
- Rework probability: 0.12
- Cycle time (min/wafer): 70
- Tool uptime: 0.85

## Step 2 — Etch (Plasma)
- Base defect rate (defects/wafer): 0.30
- Process variation (sigma): 0.60
- Rework probability: 0.08
- Cycle time (min/wafer): 50
- Tool uptime: 0.90

## Step 3 — Deposition (CVD/PVD/ALD)
- Base defect rate (defects/wafer): 0.22
- Process variation (sigma): 0.50
- Rework probability: 0.05
- Cycle time (min/wafer): 80
- Tool uptime: 0.92

## Step 4 — CMP
- Base defect rate (defects/wafer): 0.28
- Process variation (sigma): 0.55
- Rework probability: 0.07
- Cycle time (min/wafer): 60
- Tool uptime: 0.88

## Step 5 — Metrology / Inspection
- Base defect rate (defects/wafer): 0.06
- Process variation (sigma): 0.30
- Rework probability: 0.03
- Cycle time (min/wafer): 25
- Tool uptime: 0.95
