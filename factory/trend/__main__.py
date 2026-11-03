from __future__ import annotations

import argparse

from factory.console import utf8_console

from .benchmark import evaluate_benchmark, render_benchmark
from .cluster import cluster_db
from .report import write_report
from .scan import scan_sources


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only trend scanner")
    parser.add_argument("command", choices=("scan", "report", "run", "benchmark"))
    parser.add_argument("benchmark_path", nargs="?", help="fixed benchmark JSON for the benchmark command")
    args = parser.parse_args()
    if args.command == "benchmark":
        if not args.benchmark_path:
            parser.error("benchmark requires a benchmark JSON path")
        print(render_benchmark(evaluate_benchmark(args.benchmark_path)))
        return 0
    if args.command in {"scan", "run"}:
        result = scan_sources(); print(f"scan: {result['sources']} sources, {result['articles']} articles, {result['signals']} signals, {result['errors']} errors")
    if args.command == "run": print(f"cluster: {cluster_db()} events")
    if args.command in {"report", "run"}: print(f"report: {write_report()}")
    return 0


if __name__ == "__main__":
    utf8_console()
    raise SystemExit(main())
