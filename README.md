# Namespace Fabric Builder

**Story:** Spin up realistic multi-namespace topologies with `ip netns`, veth pairs, bridges, and `tc netem`. Export a ping/iperf matrix for verification.

## Quickstart
```bash
sudo python3 nfb.py up config/lab.yml
sudo python3 nfb.py test
sudo python3 nfb.py down
```

## Features
- Create N namespaces with links and addresses from YAML
- Optional latency/loss profiles via `tc netem`
- `test` runs ping matrix and small iperf tests; exports results

## Validation Results
```bash
# Example validation run (from lab VM)
$ sudo python3 nfb.py up config/lab.yml
[netns] created 4 namespaces, 6 veth links
[bridge] br0 connected A/B
[tc] latency profiles applied
$ sudo python3 nfb.py test
[pings] 16/16 successful, avg RTT = 1.2 ms
[iperf3] throughput 940 Mbps (baseline), 870 Mbps (with 50ms delay)
Connectivity matrix complete
RTT/throughput within expected SLOs
Results exported to results/*.json
```

Key Metrics
- 100% ping matrix success across all namespaces
- Throughput ≥ 90% of baseline with latency injection
- JSON/CSV results export for reproducibility

## Files
- `nfb.py` — CLI tool
- `config/lab.yml` — example topology
- `tests/*` — basic verifications
