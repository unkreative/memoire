# Thesis Workflow Guide

This document provides guidelines for effectively working on your thesis project.

## Working with Images

To add new images to your thesis:

1. Place all image files in the `src/images/` directory
2. You don't need to specify the path in your LaTeX files, as the preamble already sets up the correct path with:
   ```latex
   \graphicspath{{src/images/}}
   ```
3. Make sure the image references in your TeX files match the filenames

## Compilation Workflow

For regular compilation, you can either:

1. Run the main compile script: `./compile.sh`
2. Or run the detailed script directly: `./src/scripts/compile-thesis.sh`
3. Check the generated PDF: `open main.pdf`

## Editing Workflow

1. Edit the content in respective chapter files in the `src/chapters/` directory
2. Update references in `src/bibliography/bibliography.bib` as needed
3. Compile to see changes

## Recommendations for Daily Work

1. **Morning Session**:
   - Review progress from previous day
   - Set goals for the current day
   - Work on content creation for 2-3 hours

2. **Afternoon Session**:
   - Review and edit morning work
   - Add citations and references
   - Create or refine figures and diagrams

3. **End of Day**:
   - Compile the full document
   - Update progress tracker
   - Plan for the next day

## Version Control Recommendations

1. Commit changes at the end of each day
2. Use clear commit messages describing what was changed
3. Consider creating branches for major revisions or experimental sections
4. Push changes to a remote repository for backup

## Managing Bibliography

1. Add new references to `bibliography.bib` as you discover them
2. Use consistent citation keys (e.g., `authorYearKeyword`)
3. Include complete information for each reference

## Handling Large Images

For large or high-resolution images:
1. Consider using vector formats (PDF, SVG) when possible
2. For raster images, use PNG for diagrams/screenshots and JPG for photos
3. Keep original high-resolution versions in a separate backup location
4. Optimize images before including them in the thesis

## Daily Writing Workflow

### 1. Planning Your Writing Session

1. **Check your progress tracker**
   - Open `progress_tracker.md`
   - Identify which chapter/section you'll be working on today
   - Note which sources are suggested for that section

2. **Gather source materials**
   - Open relevant PDFs/books from your collection
   - Check the citation keys in `bibliography.bib` for these sources
   - Have these materials ready for reference

### 2. Writing Process

1. **Start with an outline**
   - For new sections, begin with a clear outline
   - List key points to cover and which sources support each point

2. **Write in manageable segments**
   - Focus on one subsection at a time
   - Aim for 500-1000 words per writing session

3. **Cite as you write**
   - Add citations directly as you write using LaTeX commands:
     ```latex
     According to \textcite{nielsen2010quantum}, quantum entanglement...
     
     This principle underlies quantum teleportation \parencite{bennett1984quantum}.
     
     \textcite[p.~125]{griffiths2018introduction} explains this concept clearly...
     ```

4. **Save frequently**
   - Save your chapter file after completing each subsection

### 3. End-of-Session Documentation

1. **Update progress tracker**
   - Mark section progress (Planned → In Progress → Completed)
   - Update completion percentage
   - Add newly used sources to the Source Tracking table
   - Note any challenges or next steps

2. **Compile and check**
   - Run the compilation sequence to verify your work:
     ```
     pdflatex main.tex
     biber main
     pdflatex main.tex
     pdflatex main.tex
     ```
   - Check the PDF for formatting issues and citation appearance

## Weekly Research and Organization Tasks

### Source Management (Weekly)

1. **Add new sources**
   - When you discover a new useful source:
     - Add it to `bibliography.bib` in appropriate section with proper BibTeX format
     - Add a note about its relevance to your project
     - Ensure the citation key follows your naming convention (author+year+keyword)

2. **Source review**
   - Weekly, scan through your Source Tracking table
   - Check for underutilized important sources
   - Identify gaps in your research

### Chapter Development (Bi-weekly)

1. **Chapter review**
   - Read through complete chapters to ensure flow and consistency
   - Check for balanced use of sources (avoid over-reliance on one source)
   - Identify areas needing more evidence or explanation

2. **Cross-chapter integration**
   - Look for connections between chapters
   - Ensure consistent terminology across the thesis
   - Add forward/backward references where appropriate

## Monthly Comprehensive Review

1. **Bibliography audit**
   - Verify all sources in your Source Tracking table appear in your bibliography.bib
   - Check that key information fields are complete
   - Ensure consistent formatting across entries

2. **Citation verification**
   - Randomly sample 5-10 citations in your text
   - Check the original source for accuracy of information
   - Verify page numbers and direct quotes

3. **Overall progress assessment**
   - Update completion percentages in the Progress Overview
   - Adjust priorities if needed
   - Set targets for the next month

## Practical Example Workflow

### Monday: Research Day
1. Research post-quantum cryptography standards
2. Add 2-3 new sources to bibliography.bib
3. Update Source Tracking table with new sources
4. Read and take notes from these sources

### Tuesday-Thursday: Writing Days
1. Work on "Quantum-Resistant Cryptography" chapter
2. Write subsections on lattice-based approaches, using appropriate citations
3. Update progress tracker after each session
4. Compile document daily to check progress

### Friday: Review Day
1. Review the week's writing for clarity and academic rigor
2. Check all new citations are properly formatted
3. Update Progress Overview table
4. Plan next week's research and writing focus

## Tips for Efficient Writing

1. **Set realistic daily goals**
   - Aim for consistent progress rather than marathon sessions
   - Target completing one subsection per writing session

2. **Citation efficiency**
   - Keep a list of frequently used citation keys handy
   - Use citation keys consistently across chapters

3. **Regular backups**
   - Commit changes to version control if using git
   - Or create date-stamped backups of your workspace weekly

4. **Visual breaks**
   - For complex topics, draft figures or diagrams to include
   - Note placement of figures in your text with `\includegraphics` commands

5. **Iterative improvement**
   - First draft: focus on content and structure
   - Second pass: improve clarity and flow
   - Third pass: perfect citations and technical accuracy

## LaTeX Compilation Troubleshooting

If you encounter issues with citations or bibliography:

1. **Check for typos in citation keys**
   - Common error: Citation `nielson2010quantum` won't work if the key is `nielsen2010quantum`

2. **Verify biber is running**
   - Look for a .bbl file in your directory after running biber
   - If missing, there might be a configuration issue

3. **Check for syntax errors**
   - Ensure your .bib entries have all required fields
   - Verify closing braces and commas in bibliography entries

4. **Clean auxiliary files**
   - If strange errors persist, delete auxiliary files (.aux, .bbl, .bcf, etc.)
   - Run the complete compilation sequence again

## Final Preparation Workflow (Last Month)

1. **Citation audit**
   - Verify every citation appears in bibliography
   - Check every bibliography entry is cited in the text
   - Verify all figures and tables are properly cited

2. **Consistency check**
   - Ensure consistent terminology throughout
   - Check formatting of equations, figures, and tables
   - Verify chapter structure is balanced

3. **Final compilation**
   - Clean all auxiliary files
   - Run full compilation sequence
   - Verify bibliography is complete and properly formatted

4. **PDF review**
   - Check hyperlinks work properly
   - Verify table of contents and page numbers
   - Review final PDF in its entirety

Remember that consistent, regular progress is more effective than occasional intensive writing sessions. By following this workflow and updating your tracking systems as you go, you'll maintain better control over your thesis development and create a well-documented, thoroughly researched final product.