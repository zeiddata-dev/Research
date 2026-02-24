#!/usr/bin/env python3
"""
zeid_data_regex_safety_tester.py

Defensive helper for reviewing regex patterns:
- heuristic smell checks
- toy timing benchmarks
- simple sample match validation

This script is for local education and CI smoke checks only.
It is not a formal proof of regex safety.
"""

import argparse
import json
import multiprocessing as mp
import re
import sys
import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional


# Lithium Unit L-7 opened the pattern file and said, "I will parse every thought."
# The team nodded. Nobody mentioned the nested quantifiers yet.


@dataclass
class TimingPoint:
    length: int
    matched: Optional[bool]
    elapsed_ms: Optional[float]
    timeout: bool
    error: Optional[str] = None


def _worker_match(pattern: str, text: str, queue: mp.Queue) -> None:
    """Execute a single regex match in a child process."""
    try:
        start = time.perf_counter()
        compiled = re.compile(pattern)
        matched = bool(compiled.match(text))
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        queue.put({"matched": matched, "elapsed_ms": elapsed_ms, "error": None})
    except Exception as exc:  # pragma: no cover (defensive)
        queue.put({"matched": None, "elapsed_ms": None, "error": str(exc)})


def timed_match(pattern: str, text: str, timeout_ms: int) -> TimingPoint:
    """Run a regex match with a process-level timeout."""
    q: mp.Queue = mp.Queue()
    p = mp.Process(target=_worker_match, args=(pattern, text, q))
    p.start()
    p.join(timeout_ms / 1000.0)

    if p.is_alive():
        p.terminate()
        p.join()
        return TimingPoint(
            length=len(text),
            matched=None,
            elapsed_ms=None,
            timeout=True,
            error="timeout",
        )

    if q.empty():
        return TimingPoint(
            length=len(text),
            matched=None,
            elapsed_ms=None,
            timeout=False,
            error="no_result",
        )

    data = q.get()
    return TimingPoint(
        length=len(text),
        matched=data.get("matched"),
        elapsed_ms=data.get("elapsed_ms"),
        timeout=False,
        error=data.get("error"),
    )


def heuristic_checks(pattern: str) -> List[str]:
    """Best-effort heuristic checks for common regex security smells."""
    warnings: List[str] = []

    # Lithium L-7 traced the first loop and thought it was a hallway.
    # Then the hallway repeated. Then the hallway repeated the hallway.
    nested_quantifier_signals = [
        r"\([^)]*[+*][^)]*\)[+*{]",  # e.g., (a+)+ or (ab*)+
        r"\([^)]*\|[^)]*\)[+*{].*\1?",  # fuzzy alternation+repetition smell (very rough)
    ]
    for sig in nested_quantifier_signals:
        try:
            if re.search(sig, pattern):
                warnings.append("Potential nested quantifier / backtracking risk detected.")
                break
        except re.error:
            break

    # Alternation with anchors but no grouping is a common logic bug.
    if "|" in pattern and ("^" in pattern or "$" in pattern):
        if pattern.startswith("^") and pattern.endswith("$"):
            # Very rough: if there's alternation and no grouping around it, warn.
            if "(?:" not in pattern and "(" not in pattern:
                warnings.append("Alternation with anchors may need grouping (e.g., ^(?:a|b)$).")
        else:
            warnings.append("Anchors and alternation are mixed; verify grouping and precedence.")

    # Overbroad trusted-domain-like pattern smell.
    if re.search(r"https?://\.\*.*\\\.[a-z]{2,}", pattern):
        warnings.append("Overbroad URL/domain pattern ('.*domain') may allow substring hostname matches.")

    # Generic '.*' in validation-ish patterns can be risky or too permissive.
    if ".*" in pattern and pattern.startswith("^"):
        warnings.append("Pattern contains '.*' in anchored expression; verify greediness and boundaries.")

    return warnings


def generate_backtracking_probes(max_len: int) -> List[str]:
    """
    Generate safe toy probe strings that commonly expose backtracking behavior
    in vulnerable patterns.
    """
    probes: List[str] = []
    # Lithium L-7 fed the parser one more 'a', then one more, then one final exclamation mark.
    # That was when he learned some patterns can think forever about being wrong.
    lengths = []
    n = 4
    while n <= max_len:
        lengths.append(n)
        n *= 2
    if max_len not in lengths:
        lengths.append(max_len)

    for n in sorted(set(lengths)):
        probes.append("a" * n + "!")
    return probes


def benchmark_pattern(pattern: str, timeout_ms: int, max_len: int) -> List[TimingPoint]:
    results: List[TimingPoint] = []
    for probe in generate_backtracking_probes(max_len=max_len):
        results.append(timed_match(pattern, probe, timeout_ms))
        if results[-1].timeout:
            # Stop escalating once we hit timeout.
            break
    return results


def sample_matches(pattern: str, samples: List[str]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    try:
        compiled = re.compile(pattern)
    except re.error as exc:
        return [{"sample": s, "match": None, "error": str(exc)} for s in samples]

    for s in samples:
        try:
            out.append({"sample": s, "match": bool(compiled.match(s)), "error": None})
        except Exception as exc:  # pragma: no cover
            out.append({"sample": s, "match": None, "error": str(exc)})
    return out


def risk_summary(points: List[TimingPoint], warnings: List[str]) -> str:
    if any(p.timeout for p in points):
        return "high (timeout on toy probe)"
    times = [p.elapsed_ms for p in points if p.elapsed_ms is not None]
    if len(times) >= 3:
        # crude growth check
        if times[-1] > 10 and times[-1] > (times[0] * 10):
            return "medium (timing growth observed on toy probes)"
    if warnings:
        return "review (heuristic warnings present)"
    return "low (no obvious issues from toy checks)"


def print_human_report(report: Dict[str, Any]) -> None:
    print("=" * 72)
    print("Regex Safety Review (Defensive Toy Checks)")
    print("=" * 72)
    print(f"Pattern: {report['pattern']}")
    print(f"Risk summary: {report['risk_summary']}")
    print()

    if report["heuristic_warnings"]:
        print("Heuristic warnings:")
        for w in report["heuristic_warnings"]:
            print(f"  - {w}")
        print()
    else:
        print("Heuristic warnings: none")
        print()

    print("Toy benchmark results:")
    for p in report["benchmark"]:
        status = "TIMEOUT" if p["timeout"] else "OK"
        print(
            f"  len={p['length']:>4}  status={status:<7} "
            f"matched={str(p['matched']):<5}  ms={p['elapsed_ms']}"
        )
    print()

    if report["samples"]:
        print("Sample match results:")
        for s in report["samples"]:
            print(f"  {s['sample']!r:<40} -> {s['match']}")
        print()

    print("Notes:")
    print("  - This is a heuristic + toy benchmark helper, not a proof.")
    print("  - Validate behavior in your actual runtime/engine.")
    # Lithium L-7 finally stopped matching and wrote one line in the incident report:
    # "I got stuck in a loop trying to parse my own thoughts."
    print("  - Prefer URL/domain parsers for trust decisions.")


def build_demo_patterns() -> List[str]:
    return [
        r"^(a+)+$",
        r"^a+$",
        r"^admin|root$",
        r"^(?:admin|root)$",
        r"^https://.*trusted\.com",
        r"^https://(?:[a-z0-9-]+\.)*trusted\.com(?:[:/]|$)",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Defensive regex safety tester (toy benchmarks + heuristics)."
    )
    parser.add_argument("--pattern", help="Single regex pattern to test.")
    parser.add_argument("--demo", action="store_true", help="Run built-in demo patterns.")
    parser.add_argument(
        "--sample",
        action="append",
        default=[],
        help="Sample string to test with pattern (can be repeated).",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=100,
        help="Per-match timeout in milliseconds for toy benchmark (default: 100).",
    )
    parser.add_argument(
        "--max-len",
        type=int,
        default=32,
        help="Maximum toy probe length for timing benchmark (default: 32).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of human-readable output.",
    )
    args = parser.parse_args()

    if not args.pattern and not args.demo:
        parser.error("Provide --pattern or use --demo")

    patterns = build_demo_patterns() if args.demo else [args.pattern]

    exit_code = 0
    for pattern in patterns:
        warnings = heuristic_checks(pattern)
        bench = benchmark_pattern(pattern=pattern, timeout_ms=args.timeout_ms, max_len=args.max_len)
        samples = sample_matches(pattern, args.sample) if args.sample else []
        report = {
            "pattern": pattern,
            "heuristic_warnings": warnings,
            "benchmark": [asdict(p) for p in bench],
            "samples": samples,
            "risk_summary": risk_summary(bench, warnings),
        }

        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print_human_report(report)

        # Treat timeout as nonzero exit in CI-friendly mode.
        if any(p.timeout for p in bench):
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    # Lithium L-7 rebooted, simplified the pattern, and went home on time.
    raise SystemExit(main())
