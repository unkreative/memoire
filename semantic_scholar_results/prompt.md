Objective:
Automate finding and verifying relevant citations for thesis chapters using pre-selected context segments. Prioritize sources from the provided Semantic Scholar and Web Search segments. Output identified BibTeX entries and citation placement instructions to **temporary, chapter- and segment-specific files** to avoid parallelism conflicts during analysis. Explicitly handle Semantic Scholar URLs by first checking local results across all cache files. Use helper scripts 'src/scripts/fetch_bibtex.py' (for DOIs) and 'src/scripts/scrape_metadata.py' (for general/fallback URL scraping).

Prerequisite:
The context for analysis MUST be provided by running the `src/scripts/context_selector.py` script first. The script's output includes:
1.  The full text of the target chapter (`--chapter`).
2.  A specific segment (`--segment`, `--segment_size`) of Semantic Scholar results (`.jsonl`).
3.  A specific segment (`--segment`, `--segment_size`) of Web Search results (`.jsonl`).
Command example: `python src/scripts/context_selector.py --chapter 5 --segment 1 --segment_size 10`

Context Files/Tools Used in this Process:
- Context Provider Script: `src/scripts/context_selector.py` (Run by user before starting this process)
- Target Bibliography File: `src/bibliography/references.bib` (Used for checking key uniqueness)
- Helper Script (DOI->BibTeX): `src/scripts/fetch_bibtex.py`
- Helper Script (URL->Metadata): `src/scripts/scrape_metadata.py`
- Full Semantic Scholar Cache Dir: `semantic_scholar_results/` (Used for checking `paperId` cache in step 3d)
- **Temporary Output Dir:** `src/scripts/temp_citation_outputs/` (Assumed location for temporary files)

Process:
1.  **Receive Context:** Acknowledge the input provided by the `context_selector.py` run (Chapter Text, Semantic Scholar Segment, Web Search Segment). Note the target chapter number (`ChapNum`) and segment number (`SegNum`). Define temporary output filenames:
    *   `TempBibFile = f"src/scripts/temp_citation_outputs/temp_bib_ch{ChapNum}_seg{SegNum}.bib"`
    *   `TempCiteFile = f"src/scripts/temp_citation_outputs/temp_cites_ch{ChapNum}_seg{SegNum}.txt"`
2.  **Identify Citation Needs:** Scan the provided Chapter Text paragraph by paragraph for specific, unsupported factual claims needing citation. Let the target sentence be `S`.
3.  **For each location (`S`) needing citation:**
    a.  **Formulate Keywords:** Extract key terms from `S` to aid relevance assessment.
    b.  **Evaluate Provided Semantic Scholar Segment:** Iterate through the JSON entries in the *provided* Semantic Scholar Segment.
        i.  Check 'title'/'abstract' against `S`. Evaluate relevance/credibility.
        ii. **If Useful (`ss_entry`):**
            *   Check for 'citationStyles.bibtex'. If present and valid, extract `bibtex_text`, proceed to step 3h (Generate/Check Key from Full BibTeX). Mark found. Stop *for this S*.
            *   Else, check for 'DOI'. If present, extract `doi`, proceed to step 3f (Fetch BibTeX via DOI). Mark found. Stop *for this S*.
            *   Else (useful but no BibTeX/DOI): Note the `ss_entry['url']` (Semantic Scholar URL). Proceed to step 3d (Handle Specific Semantic Scholar URL). Mark found. Stop *for this S*.
    c.  **Evaluate Provided Web Search Segment (If Needed):** *If no useful source found in step 3b:* Iterate through the JSON entries in the *provided* Web Search Segment.
        i.  Check 'title'/'content' against `S`. Evaluate relevance/credibility. Check the `web_entry['url']`.
        ii. **If Useful (`web_entry`):**
            *   If the URL points to `semanticscholar.org/paper/`: Proceed to step 3d (Handle Specific Semantic Scholar URL) with this URL. Mark found. Stop *for this S*.
            *   Else, check if `web_entry` has a 'DOI'. If yes, extract `doi`, proceed to step 3f. Mark found. Stop *for this S*.
            *   Else (useful, not Semantic Scholar, no DOI): Note the `web_entry['url']`. Proceed to step 3e (Scrape Generic URL). Mark found. Stop *for this S*.
    d.  **Handle Specific Semantic Scholar URL:**
        i.  Input: `ss_url` (from 3.b.ii or 3.c.ii).
        ii. Extract `paperId` (the hex string) from `ss_url`.
        iii. **Check Full Local Cache:** Search *all* `.jsonl` files in `semantic_scholar_results/` for an entry where `entry['paperId'] == paperId`.
        iv. **If Found in Cache (`cached_entry`):**
            *   Check `cached_entry['citationStyles.bibtex']`. If valid, extract `bibtex_text`, proceed to 3h. Mark found. Stop *for this S*.
            *   Else, check `cached_entry['DOI']`. If present, extract `doi`, proceed to 3f. Mark found. Stop *for this S*.
            *   Else (useful entry found, but no BibTeX/DOI in cache): Proceed to step 3e (Scrape Generic URL) using the `ss_url`. Mark found. Stop *for this S*.
        v.  **If Not Found in Cache:** Proceed to step 3e (Scrape Generic URL) using the `ss_url`.
    e.  **Scrape Generic URL Metadata (If No DOI/Cache):**
        i.  Input: `url` (from 3.c.ii, 3d.iv, or 3d.v).
        ii. Run `run_terminal_cmd`: `python src/scripts/scrape_metadata.py --url "{url}"`. Capture JSON output (`scraped_data`). Check for success/error.
        iii. If Failure: Log error. Mark unfulfilled for `S`. (*Consider next candidate or stop for S*).
        iv. **If Success & URL was Semantic Scholar:** Check if `scraped_data` contains a DOI (e.g., look for `<meta name="citation_doi">`). If DOI found, extract `doi`, proceed to 3f.
        v. **If Success (and no DOI found or not a Semantic Scholar URL):** Proceed to 3g (AI Evaluation).
    f.  **Fetch BibTeX via DOI (If DOI Available):**
        i.  Input: `doi` (from 3.b.ii, 3.c.ii, 3d.iv, or 3e.iv).
        ii. Run `run_terminal_cmd`: `python src/scripts/fetch_bibtex.py --doi "{doi}"`. Capture `bibtex_text` from stdout. Check success.
        iii. If Success: Proceed to 3h.
        iv. If Failure: Log error. Mark unfulfilled for `S`. (*Consider next candidate or stop for S*).
    g.  **AI Evaluation (for Scraped Content):**
        i.  Input: `scraped_data` (JSON from 3e), original sentence `S`.
        ii. AI Task: "Based *only* on this scraped metadata: `json.dumps(scraped_data)`, is this source sufficiently relevant, credible, and specific to support the statement `S`?"
        iii. If AI approves: Proceed to step 3i (Generate @online/@misc BibTeX).
        iv. If AI rejects: Log rejection. Mark unfulfilled for `S`. (*Consider next candidate or stop for S*).
    h.  **Generate/Check Key (from Full BibTeX):**
        i.  Input: `bibtex_text` (from 3.b.ii or 3f).
        ii. Extract/Generate key. Ensure uniqueness against `references.bib` *and* entries already added to `TempBibFile` in this run. Let final key be `final_key`. Proceed to 3j.
    i.  **Generate & Add Formatted BibTeX Entry (from Scraped/Approved):**
        i.  Input: `scraped_data` (from 3e), AI approval.
        ii. Determine BibTeX type: If `scraped_data['url']` was a Semantic Scholar URL, use `@article` or `@misc`. Otherwise use `@online`.
        iii. Construct Key: Generate unique key (`final_key`). Ensure uniqueness against `references.bib` *and* entries already added to `TempBibFile`.
        iv. Format Entry: Populate fields (title, author, year/date, url, urldate, potentially journal/publisher if scraped) based on `scraped_data` and chosen type.
        v. **Append to Temp Bib File:** Use `edit_file` to append the fully formatted BibTeX entry (using `final_key`) to `TempBibFile`. Add a newline before/after for clarity. Proceed to 3k.
    j.  **Add Full BibTeX Entry to Bibliography:**
        i.  Input: `final_key`, `bibtex_text` (from 3h).
        ii. **Append to Temp Bib File:** Use `edit_file` to append the `bibtex_text` (using `final_key`) to `TempBibFile`. Add a newline before/after. Check for duplicates *within `TempBibFile`* before appending if desired.
    k.  **Log Citation Placement:**
        i.  Input: `final_key` (determined in 3h or 3i). The original sentence `S`.
        ii. **Append to Temp Cite File:** Use `edit_file` to append the citation details to `TempCiteFile`. Format clearly, e.g.:
            ```
            Sentence: [Full text of sentence S]
            Key: [final_key]
            ---
            ```
4.  **Continue:** Move to the next location identified in step 2 within the provided Chapter Text.
5.  **Segment Completion & Next Steps:** Once all citation needs in the current Chapter Text have been addressed *using the provided source segments*, report completion for this segment and state that outputs were written to `TempBibFile` and `TempCiteFile`.
    *   Instruct the user that to process more sources for this chapter, they should run `context_selector.py` again with the *next* segment number (e.g., `--segment N+1`).
    *   **Crucially, remind the user that after processing all desired segments, they MUST manually (or via a separate script) consolidate the contents of all `temp_bib_ch[ChapNum]_seg*.bib` files into `src/bibliography/references.bib` (handling duplicates) and use the information in `temp_cites_ch[ChapNum]_seg*.txt` files to insert the `\parencite{key}` commands into the actual `src/chapters/[ChapterFile].tex`.**

Constraints:
- The process starts *after* `context_selector.py` provides the context.
- Operate primarily on the source segments provided in the context.
- **Output BibTeX entries and citation instructions EXCLUSIVELY to the temporary files (`TempBibFile`, `TempCiteFile`) defined in Step 1.** Do NOT directly modify `references.bib` or chapter `.tex` files during this process.
- Use helper scripts (`fetch_bibtex.py`, `scrape_metadata.py`) via `run_terminal_cmd`.
- Prioritize information hierarchy: Pre-computed BibTeX > DOI > Scraped/Cached Semantic Scholar URL > Scraped Generic URL > AI Eval.
- Explicitly check the *full* local cache (`semantic_scholar_results/*.jsonl`) when handling Semantic Scholar URLs (step 3d).
- Handle script failures and AI rejections gracefully for each citation need (`S`).
- Ensure BibTeX key uniqueness against `references.bib` and the current `TempBibFile`.

Execution Guidance:
When instructed to perform this citation task for a chapter and segment:
1. Confirm you have received the context from `context_selector.py`.
2. Determine and state the `TempBibFile` and `TempCiteFile` paths based on the chapter/segment number.
3. Follow the Process steps meticulously, using the provided Chapter Text and Source Segments.
4. **Use the `edit_file` tool ONLY to append content to the temporary files `TempBibFile` and `TempCiteFile`.**
5. Upon completing step 4 for the given context, execute step 5, including the reminder about final consolidation.