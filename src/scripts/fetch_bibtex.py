#!/usr/bin/env python3
import requests
import argparse
import sys
import json

CROSSREF_API_URL = "https://api.crossref.org/works/"

def fetch_bibtex_from_doi(doi):
    """Fetches BibTeX data from CrossRef API using a DOI."""
    headers = {
        'Accept': 'application/x-bibtex'
    }
    # Properly escape the DOI for the URL, though requests usually handles this
    safe_doi = requests.utils.quote(doi)
    url = f"{CROSSREF_API_URL}{safe_doi}"
    try:
        print(f"Attempting to fetch BibTeX from: {url}", file=sys.stderr)
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        # Check if the content type looks like BibTeX
        content_type = response.headers.get('Content-Type', '').lower()
        print(f"Received Content-Type: {content_type}", file=sys.stderr)

        if 'x-bibtex' in content_type:
            # The response IS the BibTeX entry
            bibtex_entry = response.text
            # Basic cleanup: Remove potential leading/trailing whitespace
            bibtex_entry = bibtex_entry.strip()
            # Check if it actually looks like a BibTeX entry
            if bibtex_entry.startswith('@'):
                print("Successfully received BibTeX format directly.", file=sys.stderr)
                return bibtex_entry
            else:
                print(f"Error: Response from {url} with content-type {content_type} did not start with '@'. Content: {bibtex_entry[:200]}...", file=sys.stderr)
                return None
        else:
            # Sometimes CrossRef might return JSON even when BibTeX is requested, try to parse DOI from it
            print("Response was not BibTeX, attempting fallback to JSON check and transform request.", file=sys.stderr)
            try:
                data = response.json()
                # Check if it looks like a valid CrossRef response containing the DOI
                if data.get('message') and data['message'].get('DOI') == doi:
                    # It seems we got JSON, maybe the DOI redirect worked differently.
                    # Attempt another request specifically asking for BibTeX transform
                    transform_url = f"{url}/transform/application/x-bibtex"
                    print(f"Attempting transform request: {transform_url}", file=sys.stderr)
                    response_transform = requests.get(transform_url, timeout=20)
                    response_transform.raise_for_status()
                    if response_transform.text.strip().startswith('@'):
                         print("Successfully received BibTeX via transform request.", file=sys.stderr)
                         return response_transform.text.strip()
                    else:
                        print(f"Error: Transform request to {transform_url} did not return valid BibTeX. Content: {response_transform.text[:200]}...", file=sys.stderr)
                        return None
                else:
                    print(f"Error: Received non-BibTeX content-type '{content_type}' from {url}. JSON content did not seem to match expected format or DOI. Content: {response.text[:200]}...", file=sys.stderr)
                    return None
            except json.JSONDecodeError:
                 print(f"Error: Received non-BibTeX content-type '{content_type}' and response is not valid JSON from {url}. Content: {response.text[:200]}...", file=sys.stderr)
                 return None

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - URL: {url}", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err} - URL: {url}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description='Fetch BibTeX entry using DOI from CrossRef.')
    parser.add_argument('--doi', required=True, help='Document Object Identifier (DOI) to fetch.')

    args = parser.parse_args()

    bibtex_data = fetch_bibtex_from_doi(args.doi)

    if bibtex_data:
        # Ensure no extra debugging output is mixed with the BibTeX
        print(bibtex_data) # Print BibTeX to stdout
        sys.exit(0) # Success
    else:
        # Error messages were already printed to stderr in the function
        print(f"Failed to retrieve BibTeX for DOI: {args.doi}", file=sys.stderr)
        sys.exit(1) # Failure

if __name__ == "__main__":
    main() 