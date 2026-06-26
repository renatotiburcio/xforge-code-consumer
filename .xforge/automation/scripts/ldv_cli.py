"""
LDV CLI - Simple command-line interface for LDV Engine.
Usage: python ldv_cli.py "your request" [--analyze-only] [--output file.json]
"""
import sys, json
from ldv_engine import analyze_request, run_loop, decompose_tasks

def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python ldv_cli.py 'your request' [--analyze-only] [--output file.json]")
        sys.exit(1)
    analyze_only = "--analyze-only" in args
    output_file = None
    if "--output" in args:
        idx = args.index("--output")
        output_file = args[idx + 1]
        args = args[:idx] + args[idx+2:]
    if analyze_only:
        args.remove("--analyze-only")
    request = " ".join(args)
    if analyze_only:
        result = analyze_request(request)
    else:
        result = run_loop(request)
    out = json.dumps(result, indent=2, ensure_ascii=False)
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f: f.write(out)
        print(f"Result saved to {output_file}")
    else:
        print(out)

if __name__ == "__main__":
    main()
