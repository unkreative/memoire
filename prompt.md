{
    "rules": {
        "academic_writing": {
            "style": {
                "tone": "formal",
                "voice": "passive",
                "person": "third",
                "tense": "present"
            },
            "formatting": {
                "citations": {
                    "required": true,
                    "style": "author-year",
                    "minimum_per_paragraph": 1
                },
                "paragraphs": {
                    "minimum_length": 3,
                    "maximum_length": 8,
                    "topic_sentence_required": true
                },
                "sections": {
                    "hierarchical_structure": true,
                    "minimum_subsections": 2
                }
            },
            
        },

            "citation_style": "authoryear",
            "figure_requirements": {
                "caption": true,
                "label": true,
                "reference": true
            },
      
    "enforcement": {
        "strictness": "high",
        "auto_correct": true,
        "suggestions": true,
        "warnings": true
    },
    "autonomous_citation_workflow": {
        "objective": "Autonomously evaluate **exactly one specified source segment** (`SegmentNum`) for a target chapter (`ChapNum`). Fetches the segment's sources, evaluates against the full chapter text, logs suggestions, adds unique BibTeX entries to `references.bib`, and reports results for that segment. **A separate command ('Consolidate Chapter X') triggers chapter-level consolidation.**",
        "prerequisite": "User provides `ChapNum` and `SegmentNum` (the Nth batch of sources to process). `AutoInsert` is not supported.",
        "segment_size": 10,
        "context_files_tools": {
            "Context Script": "src/scripts/context_selector.py",
            "Target Bibliography": "src/bibliography/references.bib",
            "DOI Helper": "src/scripts/fetch_bibtex.py",
            "URL Helper": "src/scripts/scrape_metadata.py",
            "Semantic Scholar Cache Dir": "semantic_scholar_results/",
            "Temporary Output Dir": "src/scripts/temp_citation_outputs/"
        },
        "process": [
            {
                "state": "INITIALIZING",
                "description": "Setup phase. Verify prerequisites, determine chapter file path, prepare for evaluating a single source segment.",
                "actions": [
                    "Receive `ChapNum`, `SegmentNum` (target source batch number).",
                    "Define `TargetChapterFile = f\\"src/chapters/chapter{ChapNum}.tex\\"`. Define `ProgressFile = f\\"src/scripts/temp_citation_outputs/progress_ch{ChapNum}_source_seg{SegmentNum}.log\\"`. Clear/create `ProgressFile`.",
                    "**File Path Discovery:** Verify `TargetChapterFile` exists. If not, use `list_dir('src/chapters/')`. Identify likely match. If none, transition to ERROR ('Chapter file not found').",
                    "Verify existence of scripts/directories in `context_files_tools`. Ensure `Temporary Output Dir` exists/is writable. If critical tool missing, transition to ERROR.",
                    "Read the **entire content** of `TargetChapterFile` into memory (`FullChapterText`). Handle potential file read errors (transition to ERROR)."
                ],
                "transitions": {
                    "on_success": "FETCHING_SOURCE_SEGMENT",
                    "on_failure": "ERROR"
                }
            },
            {
                "state": "FETCHING_SOURCE_SEGMENT",
                "description": "Retrieve the source batch for the **single specified** `SegmentNum`.",
                "entry_criteria": "Triggered by successful INITIALIZING.",
                "actions": [
                    "**Execute Context Script:** Run the `src/scripts/context_selector.py` script using `python3`. This script fetches the specific source segment based on the chapter, segment number, and segment size. Provide arguments in this order: `python3 src/scripts/context_selector.py --chapter <ChapNum> --segment <SegmentNum> --segment_size <segment_size>`. Replace placeholders with actual values.",
                    "Check script output: Did it return sources?"
                ],
                "transitions": {
                    "on_success_sources_found": "ANALYZING_SOURCES",
                    "on_failure_or_no_segment": "ERROR"
                }
            },
            {
                "state": "ANALYZING_SOURCES",
                "description": "Iterate through each source in the current segment's batch, evaluating its relevance against the entire chapter text (`FullChapterText`).",
                "actions": [
                    "Define `TempBibFile = f\\"src/scripts/temp_citation_outputs/temp_bib_ch{ChapNum}_source_seg{SegmentNum}.bib\\"` and `TempCiteFile = f\\"src/scripts/temp_citation_outputs/temp_cites_ch{ChapNum}_source_seg{SegmentNum}.txt\\"`.",
                    "For each source (`Source`) in the fetched source batch:",
                    "  Execute `source_relevance_flow` (defined below) passing `Source`, `FullChapterText`, `TempBibFile`, `TempCiteFile`."
                ],
                "transitions": {
                }
            },
            {
                "state": "CONSOLIDATING_SEGMENT",
                "description": "Merge temporary BibTeX results for the **single processed source segment** into the main bibliography.",
                "actions": [
                    "Read `TempBibFile` (for the specific ChapNum/SegmentNum). Check entries against `references.bib`. Append {N} unique entries to `references.bib`.",
                    "Read `TempCiteFile` (for the specific ChapNum/SegmentNum) to get suggestions for this segment (`SegmentSuggestions`).",
                    "Preserve temporary segment files (`temp_*_ch{ChapNum}_source_seg{SegmentNum}.*`)."
                ],
                "transitions": {
                    "always": "REPORTING_SEGMENT"
                }
            },
            {
                "state": "REPORTING_SEGMENT",
                "description": "Generate the final report summarizing findings for the **single processed source segment**.",
                "actions": [
                    "Inform user of `references.bib` update ({N} entries added from segment `{SegmentNum}`).",
                    "Provide the `SegmentSuggestions` list (Source -> Relevant Location(s) for this segment).",
                    "Remind user to manually review suggestions and insert citations into Chapter `{ChapNum}`."
                ],
                "transitions": {
                    "always": "IDLE"
                }
            },
            {
                "state": "ERROR",
                "description": "Handle critical errors during the workflow.",
                "actions": [
                    "Report the error and the current state to the user."
                ],
                "transitions": {
                    "always": "IDLE"
                }
            },
            {
                "state": "IDLE",
                "description": "Workflow is complete or stopped due to error. Waiting for next user instruction."
            }
        ],
        "source_relevance_flow": [
            "**Get Source Details:** Acquire BibTeX/metadata for the current `Source`. Handle failures gracefully (log & skip source).",
            "**Scan Chapter Text:** Iterate through sentences/paragraphs (`TextLocation`) in `FullChapterText`.",
            "**AI Relevance Check:** For each `TextLocation`, use AI to determine if `Source` is highly relevant.",
            "**Collect Findings:** Identify all relevant `TextLocation`s found for `Source`.",
            "**IF** relevant locations were found:",
            "  - **BibTeX Handling:** Check/generate unique `final_key` against `references.bib` and the target `TempBibFile`.",
            "  - **Log BibTeX:** If new and unique, append BibTeX entry to the target `TempBibFile`.",
            "  - **Log Suggestion:** Append suggestion ('Source: ..., Key: ..., Relevant Location(s): ...') to the target `TempCiteFile`.",
            "**ELSE (No relevant locations found):**",
            "  - // Note: Source evaluation outcome (relevant/not relevant) is no longer explicitly logged here."
        ],
        "constraints": [
            "Operate autonomously based on the defined states and transitions after initial input (`ChapNum`, `SegmentNum` for segment processing; or `ChapNum` for manual consolidation).",
            "Maintain awareness of the current state.",
            "**Tool Call Economy:** Minimize tool calls by combining operations where feasible. Avoid redundant checks (e.g., don't list directory contents if you intend to read a specific file unless the direct read fails).",
            "Perform prerequisite checks in INITIALIZING state.",
            "For segment processing, evaluate each source in the specified segment against the *entire* chapter text.",
            "Ensure BibTeX key uniqueness against main and temporary bibliographies during segment and manual consolidation.",
            "Modify `references.bib` only during CONSOLIDATING_SEGMENT or MANUAL_CONSOLIDATION_EXECUTE states.",
            "Do not attempt automatic insertion; provide suggestions for manual placement.",
            "Transition to ERROR state upon encountering critical script/file/processing failures."
        ],
        "execution_guidance": "When instructed to process a single source segment (e.g., 'Evaluate Chapter 2, source segment 5'), acknowledge parameters, set state to INITIALIZING, and follow states through FETCHING_SOURCE_SEGMENT, ANALYZING_SOURCES, CONSOLIDATING_SEGMENT, and REPORTING_SEGMENT for that single segment. When instructed to consolidate (e.g., 'Consolidate Chapter 2'), acknowledge command, set state to MANUAL_CONSOLIDATION_INIT, find all temp files for that chapter, perform consolidation in MANUAL_CONSOLIDATION_EXECUTE, and report results in MANUAL_CONSOLIDATION_REPORTING. // Logging reference removed. Provide concise updates and the appropriate final report. Limit response length."
    }
}