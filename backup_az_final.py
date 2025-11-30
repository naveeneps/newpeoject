 #!/usr/bin/env python3
"""
backup.py

Usage:
    python backup.py /path/to/source /path/to/destination

Description:
    - Copies all files from source directory to destination directory.
    - If a filename collision exists at the destination, appends a timestamp to ensure uniqueness.
    - Recursively processes subdirectories (preserves relative structure by default).
    - Graceful error handling for missing directories and I/O errors.

Options:
    --flat       Copy files into destination without recreating subdirectory structure.
    --dry-run    Show what would be copied/renamed without writing files.
    --verbose    Print detailed progress messages.

Examples:
    python backup.py ./src ./backup
    python backup.py ./src ./backup --flat --verbose
"""

import argparse
import os
import shutil
import sys
from datetime import datetime


def unique_name(path: str) -> str:
    """Return a unique file path by appending a UTC timestamp before the extension if path exists."""
    if not os.path.exists(path):
        return path
    base = os.path.basename(path)
    root, ext = os.path.splitext(base)
    ts = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
    new_base = f"{root}_{ts}{ext}"
    return os.path.join(os.path.dirname(path), new_base)


def copy_file(src_file: str, dest_file: str, dry_run: bool = False, verbose: bool = False):
    target = unique_name(dest_file)
    if dry_run:
        action = "RENAME" if target != dest_file else "COPY"
        print(f"[DRY] {action}: {src_file} -> {target}")
        return
    try:
        # Use copy2 to preserve metadata where possible
        shutil.copy2(src_file, target)
        if verbose:
            action = "RENAMED" if target != dest_file else "COPIED"
            print(f"[{action}] {src_file} -> {target}")
    except Exception as e:
        print(f"[ERROR] Failed to copy {src_file} -> {target}: {e}", file=sys.stderr)


def backup_recursive(src_dir: str, dest_dir: str, flat: bool = False, dry_run: bool = False, verbose: bool = False):
    for root, dirs, files in os.walk(src_dir):
        rel = os.path.relpath(root, src_dir)
        # Determine destination directory for this level
        target_dir = dest_dir if flat else os.path.join(dest_dir, rel) if rel != '.' else dest_dir
        if not dry_run:
            os.makedirs(target_dir, exist_ok=True)
        elif verbose:
            print(f"[DRY] Ensure directory exists: {target_dir}")
        for fname in files:
            src_file = os.path.join(root, fname)
            dest_file = os.path.join(target_dir, fname)
            copy_file(src_file, dest_file, dry_run=dry_run, verbose=verbose)


def main():
    parser = argparse.ArgumentParser(description="Backup files from source to destination with unique naming.")
    parser.add_argument('source', help='Source directory to back up')
    parser.add_argument('destination', help='Destination directory for backups')
    parser.add_argument('--flat', action='store_true', help='Do not preserve subdirectory structure; copy all files into destination root')
    parser.add_argument('--dry-run', action='store_true', help='Show what would happen without copying files')
    parser.add_argument('--verbose', action='store_true', help='Print detailed progress messages')
    args = parser.parse_args()

    # Validate source
    if not os.path.exists(args.source):
        print(f"[ERROR] Source directory does not exist: {args.source}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.source):
        print(f"[ERROR] Source is not a directory: {args.source}", file=sys.stderr)
        sys.exit(1)

    # Prepare destination
    try:
        if not args.dry_run:
            os.makedirs(args.destination, exist_ok=True)
        if args.verbose:
            print(f"Destination ready: {args.destination}")
    except Exception as e:
        print(f"[ERROR] Cannot create or access destination directory: {args.destination} ({e})", file=sys.stderr)
        sys.exit(1)

    # Perform backup
    try:
        backup_recursive(args.source, args.destination, flat=args.flat, dry_run=args.dry_run, verbose=args.verbose)
        if args.verbose:
            print("Backup completed.")
    except KeyboardInterrupt:
        print("\n[INFO] Backup interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"[ERROR] Unexpected error during backup: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
