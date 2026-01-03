import json
import urllib.request

from src.models import ProcessFlow
from src.simulate import simulate_lot


github_raw_url = "https://raw.githubusercontent.com/lawalmichael/fabflow-yield-simulator/refs/heads/main/process_flow.json"

with urllib.request.urlopen(github_raw_url) as url:
    flow_config = json.loads(url.read().decode())

process_flow = ProcessFlow.from_config(flow_config)

df = simulate_lot(
    num_wafers=25,
    num_dies_per_wafer=614,
    process_flow=process_flow,
    seed=7,
)

print(process_flow.flow_name)
print(df.head(10))
print("Avg final die yield:", df.groupby("wafer_id")["final_die_yield"].first().mean())
print("Avg expected good dies:", df.groupby("wafer_id")["expected_good_dies"].first().mean())
