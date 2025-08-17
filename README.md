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

## Files
- `nfb.py` — CLI tool
- `config/lab.yml` — example topology
- `tests/*` — basic verifications
