"""XForge Engine Benchmark (v1.1.0).

Measures throughput of key engine operations to establish a performance
baseline and detect regressions.

Usage:
    python .xforge/engine/bench.py
    python .xforge/engine/bench.py --iterations 100 --json
"""
import argparse
import json
import statistics
import sys
import time
from pathlib import Path

# Add engine to path
ROOT = Path(r"D:\\dev\\XForge-Development-New")
sys.path.insert(0, str(ROOT / ".xforge" / "engine"))


def time_call(fn, iterations):
    """Run fn N times, return median ms and calls/sec."""
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        fn()
        elapsed = (time.perf_counter() - start) * 1000
        times.append(elapsed)
    times.sort()
    median = statistics.median(times)
    p95 = times[int(0.95 * len(times))]
    return {"median_ms": round(median, 3), "p95_ms": round(p95, 3), "iterations": iterations}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--iterations", type=int, default=5)
    p.add_argument("--skip-heavy", action="store_true", help="skip validate_all (85s+)")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    import xforge_engine

    results = {}

    # 1) xforge_doctor
    results["xforge_doctor"] = time_call(
        lambda: xforge_engine.tool_doctor_run({}), args.iterations
    )

    # 2) xforge_knowledge_search (small query)
    results["xforge_knowledge_search"] = time_call(
        lambda: xforge_engine.tool_knowledge_search({"q": "pix", "topK": 3}), args.iterations
    )

    # 3) xforge_workflow_list
    results["xforge_workflow_list"] = time_call(
        lambda: xforge_engine.tool_workflow_list({}), args.iterations
    )

    # 4) xforge_pack_list
    results["xforge_pack_list"] = time_call(
        lambda: xforge_engine.tool_pack_list({}), args.iterations
    )

    # 5) xforge_validate_all (heaviest - ~85s per call, skip by default)
    if not args.skip_heavy:
        results["xforge_validate_all"] = time_call(
            lambda: xforge_engine.tool_validate_all({}), 1
        )

    # 6) _measure_sandbox_xfs (hot path)
    sandbox = ROOT / ".xforge" / "autoresearch" / "sandbox" / "knowledge"
    if sandbox.exists():
        results["_measure_sandbox_xfs"] = time_call(
            lambda: xforge_engine._measure_sandbox_xfs(sandbox), args.iterations
        )

    # Summary
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("XForge Engine Benchmark (v1.1.0)")
        print("=" * 60)
        print(f"Iterations per op: {args.iterations}")
        print()
        for op, m in results.items():
            print("  " + op.ljust(35) + "  median=" + str(m["median_ms"]).rjust(7) + "ms  p95=" + str(m["p95_ms"]).rjust(7) + "ms")
        # Find slowest
        slowest = max(results.items(), key=lambda kv: kv[1]["median_ms"])
        print()
        print("Slowest: " + slowest[0] + " at " + str(slowest[1]["median_ms"]) + "ms median")
        print("=" * 60)


if __name__ == "__main__":
    main()