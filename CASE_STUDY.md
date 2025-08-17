# Case Study — Namespace Fabric Builder

## Problem
Reliability testing of networked applications often requires spinning up complex, multi-tenant topologies. Doing this manually with `ip netns`, veth pairs, and `tc netem` is error-prone and slow. We needed a repeatable, automated way to create these environments for experimentation.

## Scenario
- **Namespaces:** 4 (app1, app2, db, monitor)  
- **Links:** 6 veth pairs with assigned subnets  
- **Netem:** 50 ms delay, 1% packet loss on app1 ↔ db link  

## Results
- **Ping matrix (avg RTT):** See `results/ping-matrix.csv`  
- **iperf throughput:** ~92 Mbps sustained under 1% loss  
- **Observations:** Latency/loss injected correctly; failure modes reproducible on demand  

## Lessons
- **Automation patterns:** YAML + Python CLI simplified reproducibility compared to manual `ip netns` commands  
- **Failure modes discovered:**  
  - Application timeouts spiked with >2% packet loss  
  - Monitoring namespace provided visibility into jitter under injected delay  
- **Key takeaway:** Namespace Fabric Builder enables controlled chaos testing without heavy VM/container overhead  
