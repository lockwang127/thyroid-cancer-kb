#!/usr/bin/env python3
"""Sync thyroid cancer knowledge base to GitHub repository."""

import os
import subprocess
import sys

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_cmd(cmd, check=True):
    """Run a shell command."""
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=REPO_DIR, capture_output=True, text=True)
    if result.stdout:
        print(f"  {result.stdout.strip()}")
    if result.stderr:
        print(f"  [stderr] {result.stderr.strip()}")
    if check and result.returncode != 0:
        print(f"Error: command failed with exit code {result.returncode}")
        sys.exit(1)
    return result


def sync():
    """Sync to GitHub."""
    print("=" * 60)
    print("Thyroid Cancer KB - GitHub Sync")
    print("=" * 60)

    # Check git status
    print("\n[CHECK] Git status...")
    run_cmd("git status --short")

    # Check if remote is set
    print("\n[CHECK] Remote origin...")
    result = run_cmd("git remote get-url origin", check=False)
    if result.returncode != 0:
        print("\n[INFO] No remote origin set. To connect to GitHub:")
        print("  1. Create repository at https://github.com/new")
        print("  2. Run: git remote add origin git@github.com:lockwang127/thyroid-cancer-kb.git")
        print("  3. Run: git push -u origin main")
        return

    print(f"  Remote: {result.stdout.strip()}")

    # Build knowledge base first
    print("\n[BUILD] Building knowledge base...")
    build_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_kb.py")
    run_cmd(f"python3 {build_script}")

    # Add all changes
    print("\n[ADD] Staging changes...")
    run_cmd("git add -A")

    # Check if there are changes to commit
    result = run_cmd("git status --porcelain", check=False)
    if not result.stdout.strip():
        print("\n[INFO] No changes to commit. Repository is up to date.")
        return

    # Commit
    timestamp = __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M")
    run_cmd(f'git commit -m "Update knowledge base - {timestamp}"')

    # Push
    print("\n[PUSH] Pushing to GitHub...")
    run_cmd("git push origin main")

    print("\n[DONE] Sync complete!")


if __name__ == "__main__":
    sync()
