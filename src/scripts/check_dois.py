#!/usr/bin/env python3
import bibtexparser
import requests
import sys
import os
import argparse
from urllib.parse import urlparse, urlunparse
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import time

# --- Configuration ---
BIB_DIRECTORY = "src/bibliography/" # Directory containing .bib files
POTENTIAL_CATCH_ALL_HOSTS = {"doi.org"}
REQUEST_TIMEOUT = 15
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
}
CHECK_DELAY = 0.5
DEFAULT_OUTPUT_FILENAME = "consolidated_checked.bib"
CLEANED_SUFFIX = "_cleaned" # Suffix used by previous version

# Define return codes for validation
DOI_VALID = 0
DOI_NOT_FOUND = 404
DOI_FORBIDDEN = 403
DOI_TIMEOUT = -1
DOI_REQUEST_ERROR = -2
DOI_OTHER_ERROR = -3
DOI_RESOLVER_LANDING = 1

URL_VALID = 100
URL_UNREACHABLE = 101
URL_NOT_FOUND = 104
URL_FORBIDDEN = 103
URL_INVALID_FORMAT = 105
URL_OTHER_HTTP_ERROR = 106

# --- Helper Functions ---

def normalize_doi(doi_str):
    """Normalizes DOI string for comparison.
       Removes leading/trailing whitespace, converts to lowercase, removes 'doi:' prefix.
    """
    if not doi_str or not isinstance(doi_str, str):
        return None
    doi_str = doi_str.strip().lower()
    if doi_str.startswith("doi:"):
        doi_str = doi_str[4:].strip()
    # Add more aggressive normalization if needed (e.g., remove http proxy prefixes)
    if doi_str.startswith("https://doi.org/"):
        doi_str = doi_str[len("https://doi.org/"):]
    elif doi_str.startswith("http://doi.org/"):
         doi_str = doi_str[len("http://doi.org/"):]
    return doi_str or None

def validate_doi(doi, entry_key, bib_filename="consolidated"):
    """
    Validates a DOI by attempting to resolve it via doi.org.
    Now defaults bib_filename for consolidated context.
    """
    normalized_doi = normalize_doi(doi)
    if not normalized_doi:
        return DOI_VALID # Treat missing/empty as valid for validation purposes

    original_url = f"https://doi.org/{normalized_doi}"
    print(f"[D] Entry '{entry_key}': Checking DOI {normalized_doi} -> {original_url}")

    try:
        time.sleep(CHECK_DELAY)
        response = requests.get(
            original_url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True
        )
        final_url = response.url
        status_code = response.status_code

        if status_code != 200:
            print(f"[!] Entry '{entry_key}': Invalid DOI '{normalized_doi}'. HTTP Status Code: {status_code}", file=sys.stderr)
            if status_code == 404: return DOI_NOT_FOUND
            if status_code == 403: return DOI_FORBIDDEN
            return status_code

        final_parsed = urlparse(final_url)
        original_parsed = urlparse(original_url)
        if final_parsed.netloc in POTENTIAL_CATCH_ALL_HOSTS and final_parsed.path == original_parsed.path:
             print(f"[?] Entry '{entry_key}': Potentially unresolved DOI '{normalized_doi}'. Final URL still on resolver: {final_url}", file=sys.stderr)
             return DOI_VALID

        print(f"[+] Entry '{entry_key}': DOI '{normalized_doi}' seems valid. Resolved to: {final_url}")
        return DOI_VALID

    except requests.exceptions.Timeout:
        print(f"[!] Entry '{entry_key}': Invalid DOI '{normalized_doi}'. Request timed out.", file=sys.stderr)
        return DOI_TIMEOUT
    except requests.exceptions.RequestException as e:
        print(f"[!] Entry '{entry_key}': Invalid DOI '{normalized_doi}'. Request failed: {e}", file=sys.stderr)
        return DOI_REQUEST_ERROR
    except Exception as e:
        print(f"[!] Entry '{entry_key}': Error checking DOI '{normalized_doi}': {e}", file=sys.stderr)
        return DOI_OTHER_ERROR

def validate_url(url, entry_key, bib_filename="consolidated"):
    """
    Validates a URL by attempting to make a GET request.
    Now defaults bib_filename for consolidated context.
    """
    if not url or not isinstance(url, str):
        return URL_VALID

    url = url.strip()
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        parsed_url = parsed_url._replace(scheme="https")
        url = urlunparse(parsed_url)
    if not parsed_url.netloc:
         print(f"[-] Entry '{entry_key}': Skipping invalid URL format: '{url}'", file=sys.stderr)
         return URL_INVALID_FORMAT

    print(f"[U] Entry '{entry_key}': Checking URL {url}")

    try:
        time.sleep(CHECK_DELAY)
        response = requests.get(
            url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True
        )
        status_code = response.status_code

        if status_code >= 200 and status_code < 400:
            print(f"[+] Entry '{entry_key}': URL '{url}' seems reachable (Final status: {status_code}). Final URL: {response.url}")
            return URL_VALID
        else:
            print(f"[!] Entry '{entry_key}': URL '{url}' unreachable. HTTP Status Code: {status_code}", file=sys.stderr)
            if status_code == 404: return URL_NOT_FOUND
            if status_code == 403: return URL_FORBIDDEN
            return URL_OTHER_HTTP_ERROR

    except requests.exceptions.Timeout:
        print(f"[!] Entry '{entry_key}': URL '{url}'. Request timed out.", file=sys.stderr)
        return URL_UNREACHABLE
    except requests.exceptions.RequestException as e:
        print(f"[!] Entry '{entry_key}': URL '{url}'. Request failed: {e}", file=sys.stderr)
        return URL_UNREACHABLE
    except Exception as e:
        print(f"[!] Entry '{entry_key}': Error checking URL '{url}': {e}", file=sys.stderr)
        return URL_UNREACHABLE


def main():
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="Consolidate, deduplicate, and validate DOIs/URLs in .bib files.")
    parser.add_argument(
        "--remove-404", action="store_true",
        help="Remove entries with DOIs resolving to 404 Not Found."
    )
    parser.add_argument(
        "--remove-unreachable-url", action="store_true",
        help="Remove entries with unreachable URLs (404, timeout, connection error, etc.)."
    )
    parser.add_argument(
        "--force-originals", action="store_true",
        help=f"Force processing of original .bib files even if {CLEANED_SUFFIX}.bib files exist."
    )
    parser.add_argument(
        "--output-file", default=os.path.join(BIB_DIRECTORY, DEFAULT_OUTPUT_FILENAME),
        help=f"Path for the final consolidated output file (default: {os.path.join(BIB_DIRECTORY, DEFAULT_OUTPUT_FILENAME)})."
    )
    args = parser.parse_args()

    perform_removal = args.remove_404 or args.remove_unreachable_url
    output_filepath = args.output_file

    # --- Script Start ---
    print(f"--- Consolidating, Deduplicating, and Checking BibTeX files in {BIB_DIRECTORY} ---")
    if perform_removal:
        print("*** WARNING: Removal flag(s) active. Entries with specified errors will be removed from the final output. ***")
        if args.remove_404: print("          --remove-404: Active")
        if args.remove_unreachable_url: print("          --remove-unreachable-url: Active")
    print(f"--- Final output will be written to: {output_filepath} ---")
    print("Ensure you have installed required libraries: pip install bibtexparser requests")

    # --- Find and Select Input Bib Files ---
    all_files = []
    try:
        all_files = os.listdir(BIB_DIRECTORY)
    except FileNotFoundError:
        print(f"Error: Directory not found at {BIB_DIRECTORY}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error listing directory {BIB_DIRECTORY}: {e}", file=sys.stderr)
        sys.exit(1)

    # Find cleaned files (using the specific suffix from previous runs)
    cleaned_files = {f for f in all_files if f.lower().endswith(f"{CLEANED_SUFFIX}.bib") and os.path.isfile(os.path.join(BIB_DIRECTORY, f))}
    # Find original files (don't end with the cleaned suffix)
    original_files = {f for f in all_files if f.lower().endswith(".bib") and not f.lower().endswith(f"{CLEANED_SUFFIX}.bib") and os.path.isfile(os.path.join(BIB_DIRECTORY, f))}

    bib_files_to_process = []
    if cleaned_files and not args.force_originals:
        print(f"Found existing '{CLEANED_SUFFIX}.bib' files, processing these.")
        bib_files_to_process = sorted(list(cleaned_files))
    elif original_files:
        print(f"Processing original .bib files (or --force-originals was used).")
        bib_files_to_process = sorted(list(original_files))
    else:
        print(f"No suitable .bib files found in {BIB_DIRECTORY} to process.")
        sys.exit(0)

    print(f"Input files: {', '.join(bib_files_to_process)}")

    # --- Load, Consolidate, and Deduplicate --- 
    consolidated_db = BibDatabase()
    seen_ids = set()
    seen_dois = set() # Store normalized DOIs
    duplicates_found = {"id": 0, "doi": 0}
    all_comments = []
    all_preambles = []
    all_strings = {} # Simple merge, later keys overwrite earlier

    print("\n--- Loading and Deduplicating entries ---")
    for bib_filename in bib_files_to_process:
        input_filepath = os.path.join(BIB_DIRECTORY, bib_filename)
        print(f"Reading file: {input_filepath}")
        try:
            with open(input_filepath, 'r', encoding='utf-8') as bibtex_file:
                parser = bibtexparser.bparser.BibTexParser(common_strings=True)
                parser.ignore_comments = False
                db = bibtexparser.load(bibtex_file, parser=parser)

                # Merge metadata (simple merge for strings)
                all_comments.extend(db.comments)
                all_preambles.extend(db.preambles)
                all_strings.update(db.strings)

                # Process entries for deduplication
                for entry in db.entries:
                    entry_id = entry['ID']
                    normalized_doi = normalize_doi(entry.get('doi'))

                    is_duplicate = False
                    if entry_id in seen_ids:
                        print(f"    Duplicate ID found: '{entry_id}' (from {bib_filename}). Skipping.", file=sys.stderr)
                        duplicates_found["id"] += 1
                        is_duplicate = True
                    elif normalized_doi and normalized_doi in seen_dois:
                         print(f"    Duplicate DOI found: '{normalized_doi}' (ID: '{entry_id}' from {bib_filename}). Skipping.", file=sys.stderr)
                         duplicates_found["doi"] += 1
                         is_duplicate = True

                    if not is_duplicate:
                        consolidated_db.entries.append(entry)
                        seen_ids.add(entry_id)
                        if normalized_doi:
                            seen_dois.add(normalized_doi)

        except Exception as e:
            print(f"Error parsing BibTeX file {input_filepath}: {e}. Skipping this file.", file=sys.stderr)
            continue

    # Assign merged metadata to the consolidated DB
    consolidated_db.comments = all_comments # May contain duplicates, but preserves info
    consolidated_db.preambles = all_preambles
    consolidated_db.strings = all_strings

    print(f"--- Deduplication complete: {len(consolidated_db.entries)} unique entries loaded.")
    print(f"    Skipped {duplicates_found['id']} duplicates by ID.")
    print(f"    Skipped {duplicates_found['doi']} duplicates by DOI.")

    # --- Validate Unique Entries --- 
    print("\n--- Validating DOIs and URLs for unique entries ---")
    entries_to_remove_keys = set()
    grand_total_dois_checked = 0
    grand_total_dois_invalid = 0
    grand_total_urls_checked = 0
    grand_total_urls_invalid = 0

    for entry in consolidated_db.entries:
        entry_key = entry['ID']
        remove_this_entry = False

        # 1. Check DOI
        if 'doi' in entry:
            grand_total_dois_checked += 1
            doi_status = validate_doi(entry.get('doi', ''), entry_key)
            if doi_status != DOI_VALID:
                grand_total_dois_invalid += 1
                if doi_status == DOI_NOT_FOUND and args.remove_404:
                    print(f"    -> Marking entry '{entry_key}' for removal (DOI 404).")
                    remove_this_entry = True

        # 2. Check URL (only if not already marked for removal)
        if not remove_this_entry and 'url' in entry:
            grand_total_urls_checked += 1
            url_status = validate_url(entry.get('url', ''), entry_key)
            if url_status != URL_VALID:
                grand_total_urls_invalid += 1
                if args.remove_unreachable_url and url_status != URL_INVALID_FORMAT:
                     print(f"    -> Marking entry '{entry_key}' for removal (Unreachable URL, status: {url_status}).")
                     remove_this_entry = True

        if remove_this_entry:
            entries_to_remove_keys.add(entry_key)

    print("--- Validation complete ---")

    # --- Filter and Write Output File ---
    final_entries = [entry for entry in consolidated_db.entries if entry['ID'] not in entries_to_remove_keys]
    consolidated_db.entries = final_entries
    grand_total_removed_count = len(entries_to_remove_keys)

    print(f"\n--- Writing final output to: {output_filepath} ---")
    print(f"    Entries to write: {len(consolidated_db.entries)}")
    print(f"    Entries removed: {grand_total_removed_count}")

    try:
        writer = BibTexWriter()
        writer.indent = '    '
        writer.comma_first = False
        # Ensure parent directory exists
        output_dir = os.path.dirname(output_filepath)
        if output_dir and not os.path.exists(output_dir):
             os.makedirs(output_dir)
             print(f"Created output directory: {output_dir}")

        with open(output_filepath, 'w', encoding='utf-8') as bibfile:
            bibfile.write(writer.write(consolidated_db))
        print(f"+++ Successfully wrote consolidated data to: {output_filepath} +++")
    except Exception as e:
        print(f"!!! Error writing consolidated file {output_filepath}: {e} !!!", file=sys.stderr)
        sys.exit(1) # Exit if writing failed

    # --- Overall Summary ---
    print(f"\n--- Final Summary ---")
    print(f"Input files processed: {len(bib_files_to_process)}")
    print(f"Unique entries loaded: {len(seen_ids)}")
    print(f"DOIs: Checked={grand_total_dois_checked}, Invalid={grand_total_dois_invalid}")
    print(f"URLs: Checked={grand_total_urls_checked}, Invalid={grand_total_urls_invalid}")
    print(f"Entries removed due to flags: {grand_total_removed_count}")
    print(f"Final entries written to {output_filepath}: {len(consolidated_db.entries)}")

    total_issues_found = grand_total_dois_invalid + grand_total_urls_invalid
    if total_issues_found > 0:
        print(f"\nReview suggested: {total_issues_found} potential DOI/URL issues identified (before removals).", file=sys.stderr)
        sys.exit(1) # Exit with error if any issues were *identified*, even if removed
    elif grand_total_removed_count > 0:
        print("\nValidation passed after removing entries with specified errors.")
        sys.exit(0)
    else:
        print("\nValidation passed. All checked DOIs and URLs appear valid.")
        sys.exit(0)


if __name__ == "__main__":
    main() 