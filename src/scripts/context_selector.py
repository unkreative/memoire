#!/usr/bin/env python3

import argparse
import os
import re
import sys
import json
import glob
from itertools import islice

# --- Configuration ---
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DEFAULT_CHAPTERS_DIR = os.path.join(WORKSPACE_ROOT, 'src', 'chapters')
DEFAULT_SS_RESULTS_DIR = os.path.join(WORKSPACE_ROOT, 'semantic_scholar_results')
DEFAULT_WEB_RESULTS_DIR = os.path.join(WORKSPACE_ROOT, 'web_search_results')
DEFAULT_SEGMENT_SIZE = 10

# --- Helper Functions ---

def find_file_by_chapter(chapter_number: int, directory: str, prefix: str, suffix: str, use_leading_zero: bool = False) -> str | None:
    """Finds a file in a directory based on chapter number and naming convention."""
    # Format chapter number based on the flag
    chap_num_str = f"{chapter_number:02d}" if use_leading_zero else str(chapter_number)

    # Pattern specifically for files starting with the given prefix and chapter number
    # Allows for optional descriptive text after the chapter number (e.g., prefix1.suffix or prefix1_description.suffix)
    # Handles leading zeros based on chap_num_str
    pattern = re.compile(rf"^{prefix}{chap_num_str}(?:_.*)?\{suffix}$", re.IGNORECASE)
    # Fallback pattern for chapter files (no prefix, e.g., 1_Introduction.tex or 01_Introduction.tex)
    # Handles leading zeros based on chap_num_str
    pattern_prefix_only = re.compile(rf"^{chap_num_str}_.*\{suffix}$", re.IGNORECASE)

    target_pattern = pattern if prefix else pattern_prefix_only

    try:
        filenames = os.listdir(directory)
        for filename in filenames:
            if target_pattern.match(filename):
                # Return the first match found
                return os.path.join(directory, filename)
    except FileNotFoundError:
        print(f"Warning: Directory not found at {directory}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error listing directory {directory}: {e}", file=sys.stderr)
        return None

    # Specific check for prefix-based search failing if fallback might be intended (though unlikely with current usage)
    # If a prefix was provided but the primary pattern failed, we don't fallback to the prefix_only pattern here.
    # If no prefix was provided (chapters) and the prefix_only pattern failed, we also reach here.
    return None # No match found

def read_jsonl_segment(filepath: str, start_line: int, end_line: int) -> list[dict]:
    """Reads a specific segment (line range) from a JSONL file."""
    entries = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # islice uses 0-based indexing, lines are 1-based
            segment_lines = islice(f, start_line - 1, end_line)
            for i, line in enumerate(segment_lines, start=start_line):
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode JSON on line {i} in {filepath}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Warning: File not found: {filepath}", file=sys.stderr)
    except Exception as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
    return entries

def read_file_content(filepath: str) -> str | None:
    """Reads the entire content of a text file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: File not found: {filepath}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        return None

# --- Main Execution ---

def main():
    parser = argparse.ArgumentParser(
        description="Selects and outputs chapter content and segments of source results.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--chapter", type=int, required=True, help="The chapter number.")
    parser.add_argument("--segment", type=int, required=True, help="The segment number (1-based).")
    parser.add_argument("--segment_size", type=int, default=DEFAULT_SEGMENT_SIZE, help="Number of entries per segment.")
    parser.add_argument("--chap_dir", default=DEFAULT_CHAPTERS_DIR, help="Directory containing chapter .tex files.")
    parser.add_argument("--ss_dir", default=DEFAULT_SS_RESULTS_DIR, help="Directory containing Semantic Scholar .jsonl results.")
    parser.add_argument("--web_dir", default=DEFAULT_WEB_RESULTS_DIR, help="Directory containing Web Search .jsonl results.")

    args = parser.parse_args()

    if args.segment < 1:
        print("Error: Segment number must be 1 or greater.", file=sys.stderr)
        sys.exit(1)

    # --- Find Files ---
    # Chapters and SS use leading zeros (01, 02, ...)
    chapter_file = find_file_by_chapter(args.chapter, args.chap_dir, prefix="", suffix=".tex", use_leading_zero=True)
    ss_file = find_file_by_chapter(args.chapter, args.ss_dir, prefix="results_ch", suffix=".jsonl", use_leading_zero=True)
    # Web results do not use leading zeros (1, 2, ...)
    web_file = find_file_by_chapter(args.chapter, args.web_dir, prefix="web_results_ch", suffix=".jsonl", use_leading_zero=False)

    # --- Read Chapter Content ---
    chapter_content = None
    if chapter_file:
        chapter_content = read_file_content(chapter_file)
    else:
        print(f"Warning: Could not find .tex file for chapter {args.chapter} in {args.chap_dir}", file=sys.stderr)

    # --- Calculate Segment Range ---
    start_line = (args.segment - 1) * args.segment_size + 1
    end_line = start_line + args.segment_size - 1 # Inclusive end line for reading range

    # --- Read Source Segments ---
    ss_segment_data = []
    if ss_file:
        ss_segment_data = read_jsonl_segment(ss_file, start_line, end_line)
    else:
        print(f"Warning: Could not find Semantic Scholar results file for chapter {args.chapter} in {args.ss_dir}", file=sys.stderr)

    web_segment_data = []
    if web_file:
        web_segment_data = read_jsonl_segment(web_file, start_line, end_line)
    else:
        print(f"Warning: Could not find Web Search results file for chapter {args.chapter} in {args.web_dir}", file=sys.stderr)

    # --- Output Combined Context ---
    print("--- CHAPTER CONTENT ---")
    if chapter_content:
        print(chapter_content)
    else:
        print("Chapter content not found.")
    print("\n--- END CHAPTER CONTENT ---\n")

    print(f"--- SEMANTIC SCHOLAR RESULTS (Segment {args.segment}, Lines {start_line}-{end_line}) ---")
    if ss_segment_data:
        print(json.dumps(ss_segment_data, indent=2))
    else:
        print("No Semantic Scholar results found for this segment.")
    print("\n--- END SEMANTIC SCHOLAR RESULTS ---\n")

    print(f"--- WEB SEARCH RESULTS (Segment {args.segment}, Lines {start_line}-{end_line}) ---")
    if web_segment_data:
        print(json.dumps(web_segment_data, indent=2))
    else:
        print("No Web Search results found for this segment.")
    print("\n--- END WEB SEARCH RESULTS ---")


if __name__ == "__main__":
    main() 