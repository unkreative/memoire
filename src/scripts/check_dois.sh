#!/bin/bash

# Script to check DOI validity in .bib files

BIB_DIR="src/bibliography"
INVALID_DOIS=()

echo "Scanning .bib files in $BIB_DIR for DOIs..."

# Find all .bib files and extract DOIs
# Using rg (ripgrep) for efficient searching
# Regex captures the DOI value from lines like 'doi = {10.xxxx/xxxxx}'
rg --no-filename --no-line-number -o -e 'doi\s*=\s*[\"{]([^\"}]+)[\"}]' "$BIB_DIR"/*.bib | while IFS= read -r doi; do
    # Clean up potential surrounding braces or quotes if regex wasn't perfect (though it should be)
    doi=$(echo "$doi" | sed -e 's/^[ \"{]*//' -e 's/[ \"}]*$//')
    DOI_URL="https://doi.org/$doi"

    echo "Checking DOI: $doi -> $DOI_URL"

    # Use curl to follow redirects (-L), get only headers (-I), silently (-s), fail fast (--fail)
    # Check if the final location header still points to doi.org (indicating an error page) or if curl fails
    final_url=$(curl -sLI --fail "$DOI_URL" | grep -i '^location:' | tail -n 1 | awk '{print $2}')

    # Check curl's exit status
    curl_status=$?

    if [ $curl_status -ne 0 ]; then
        echo "  [INVALID] Failed to resolve: $DOI_URL (curl exit status: $curl_status)"
        INVALID_DOIS+=("$doi")
    # Check if the final redirect URL still contains 'doi.org', suggesting it didn't resolve to a publisher page
    # Or handle.net/is/invalid pattern sometimes seen
    elif [[ "$final_url" == *doi.org* || "$final_url" == *handle.net/is/invalid* ]]; then
        echo "  [INVALID] Did not redirect properly. Final URL: $final_url"
        INVALID_DOIS+=("$doi")
    else
        echo "  [VALID] Resolved successfully to: $final_url"
    fi

    # Add a small delay to avoid overwhelming doi.org
    sleep 0.2
done

echo ""
echo "-------------------------------------"
if [ ${#INVALID_DOIS[@]} -eq 0 ]; then
    echo "All checked DOIs appear valid."
else
    echo "Found ${#INVALID_DOIS[@]} potentially invalid DOIs:"
    for invalid_doi in "${INVALID_DOIS[@]}"; do
        echo "- $invalid_doi"
    done
fi
echo "-------------------------------------"

exit 0 