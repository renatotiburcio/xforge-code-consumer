#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# genius-learn.py - Wrapper CLI para /genius-learn (DR-0136)
import argparse, sys, subprocess
from pathlib import Path
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--force', action='store_true')
    p.add_argument('--stats', action='store_true')
    args = p.parse_args()
    if args.stats:
        sys.path.insert(0, '.kilo/mcp/compliance-intelligence/tools')
        from knowledge_query import stats
        for d in sorted(Path('.xforge/memory/genius').iterdir()):
            if d.is_dir():
                s = stats(d.name)
                print(d.name, 'entradas:', s.get('total_entries', 0))
        return 0
    cmd = ['python', '.kilo/mcp/compliance-intelligence/tools/post_mcp_hook.py']
    if args.dry_run: cmd.append('--dry-run')
    if args.force:
        pf = Path('.kilo/mcp/queue/.processed.json')
        if pf.exists(): pf.unlink()
    return subprocess.call(cmd)
if __name__ == '__main__': sys.exit(main())
