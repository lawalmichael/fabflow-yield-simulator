# Yield Model (Baseline)

## Selected primary model
We use the Poisson yield model, a standard semiconductor yield approximation:

Y_die = exp(-D * A)

Where:
- D = defect density (defects per cm^2)
- A = die area (cm^2)

## Simulator mapping (defects/wafer -> defect density)
The simulator produces defect counts per wafer (and per step). We convert to defect density using wafer area:

D = defects_per_wafer / wafer_area_cm2

For a 300 mm wafer:
- radius = 150 mm = 15 cm
- wafer_area_cm2 = pi * 15^2 ≈ 706.86 cm^2

So:
D ≈ defects_per_wafer / 706.86

## Step-level yield
If a step introduces defects_i on a wafer:

D_i = defects_i / 706.86
Y_die_step_i = exp(-D_i * A)

## Overall die yield across the process flow
Final die yield is the product of step yields:

Y_die_total = Π Y_die_step_i
Equivalently:
Y_die_total = exp(-(Σ D_i) * A)

## Baseline assumptions (v1)
- Wafer diameter: 300 mm
- Edge exclusion: 3 mm (effective diameter: 294 mm)
- Die area: 100 mm^2 = 1.0 cm^2
- Dies per wafer (approx): 614

## Reported outputs per wafer (v1)
- totalDefects
- defectsByStep
- dieYieldByStep
- finalDieYield
- expectedGoodDies = finalDieYield * diesPerWafer
