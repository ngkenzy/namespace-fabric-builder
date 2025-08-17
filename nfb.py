#!/usr/bin/env python3
import sys, os, subprocess, yaml, time, itertools, csv

def sh(cmd):
    print("+", cmd)
    return subprocess.run(cmd, shell=True, check=True, text=True, capture_output=False)

def up(cfg):
    # create namespaces
    for ns in cfg['namespaces']:
        sh(f"ip netns add {ns['name']} || true")
    # create veth pairs
    for i,link in enumerate(cfg['links'], start=1):
        a, b = link['a'], link['b']
        va, vb = f"veth{i}a", f"veth{i}b"
        sh(f"ip link add {va} type veth peer name {vb}")
        sh(f"ip link set {va} netns {a}")
        sh(f"ip link set {vb} netns {b}")
        sh(f"ip netns exec {a} ip addr add {cfg['namespaces'][0]['addr']} dev {va} || true")
        sh(f"ip netns exec {b} ip addr add {cfg['namespaces'][1]['addr']} dev {vb} || true")
        sh(f"ip netns exec {a} ip link set {va} up")
        sh(f"ip netns exec {b} ip link set {vb} up")
        # tc profiles (optional)
        delay = link.get('delay_ms')
        loss = link.get('loss_pct')
        if delay or loss:
            netem = " ".join([f"delay {delay}ms" if delay else "", f"loss {loss}%" if loss else ""]).strip()
            sh(f"ip netns exec {a} tc qdisc add dev {va} root netem {netem}")
            sh(f"ip netns exec {b} tc qdisc add dev {vb} root netem {netem}")
    print("[+] up complete")

def down(cfg):
    for ns in cfg['namespaces']:
        try:
            sh(f"ip netns del {ns['name']}")
        except subprocess.CalledProcessError:
            pass
    # clean stray veths
    subprocess.run("ip -br link | awk '/veth/ {print $1}' | xargs -r -n1 ip link del", shell=True)
    print("[+] down complete")

def test(cfg):
    nsA = cfg['namespaces'][0]['name']
    nsB = cfg['namespaces'][1]['name']
    # ping matrix
    os.makedirs("results", exist_ok=True)
    with open("results/ping_matrix.csv","w",newline="") as f:
        w = csv.writer(f); w.writerow(["src","dst","avg_rtt_ms"])
        for src,dst in [(nsA,nsB),(nsB,nsA)]:
            out = subprocess.check_output(f"ip netns exec {src} ping -c3 -w3 $(ip -br addr show dev veth1{'b' if src==nsA else 'a'} | awk '{{print $3}}' | cut -d/ -f1)", shell=True, text=True, stderr=subprocess.DEVNULL)
            # naive parse
            line = [l for l in out.splitlines() if 'rtt min/avg' in l]
            avg = line[0].split('/')[4] if line else ""
            w.writerow([src,dst,avg])
    print("[+] wrote results/ping_matrix.csv")

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ["up","down","test"]:
        print("Usage: sudo python3 nfb.py [up|down|test] config/lab.yml")
        sys.exit(1)
    action = sys.argv[1]
    import yaml as _yaml  # lazy import name
    cfg = _yaml.safe_load(open(sys.argv[2]))
    {'up':up, 'down':down, 'test':test}[action](cfg)

if __name__ == "__main__":
    main()
