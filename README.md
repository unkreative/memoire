# Quantum Computing and Its Impact on Cryptography

## Thesis Project Overview

This repository contains the LaTeX source for a thesis on quantum computing and its implications for cryptography. The thesis explores the fundamental principles of quantum computing, its potential impact on classical cryptographic systems, and the development of quantum-resistant cryptographic algorithms.

## Author
- Lou Sergonne
- 2024-2025

## Repository Structure

- `main.tex` - Main LaTeX document that includes all chapter files
- `preamble.tex` - Document preamble with package imports and settings
- `compile.sh` - Simple wrapper script to compile the thesis
- `src/` - Source directory containing all content
  - `bibliography/bibliography.bib` - BibTeX bibliography file
  - `chapters/` - Directory containing individual chapter files
  - `images/` - Directory for images and figures
  - `scripts/compile-thesis.sh` - Main compilation script
- `build/` - Directory for compilation outputs and auxiliary files

## Chapters

1. Introduction
2. Fundamentals of Quantum Computing
3. Classical vs. Quantum Computing
4. Classical Cryptography
5. Quantum Impact on Cryptography
6. Quantum-Resistant Cryptographic Methods
7. Challenges in Implementation
8. Future Prospects
9. Societal Implications

## Compilation

To compile the thesis, run:

```bash
./compile.sh
```

or directly:

```bash
./src/scripts/compile-thesis.sh
```

This script will:
1. Check for required LaTeX packages
2. Run pdflatex on the main document
3. Process the bibliography with biber
4. Run pdflatex twice more to resolve references
5. Copy the final PDF to the main directory

## Required LaTeX Packages

- biblatex (with biber backend)
- amsmath, amssymb
- graphicx
- hyperref
- and others specified in preamble.tex

## Content Overview

### Introduction
Overview of quantum computing, its importance in cryptography, and comparison with classical computing.

### Fundamentals of Quantum Computing
Covers quantum mechanics principles (wave-particle duality, superposition, entanglement, uncertainty principle), qubits, quantum gates, quantum states, and key quantum algorithms.

### Classical vs. Quantum Computing
Direct comparison of bits vs. qubits, deterministic vs. probabilistic computation, computational capabilities, and practical applications and limitations.

### Classical Cryptography
Reviews current cryptographic methods including symmetric and asymmetric encryption, hash functions, and digital signatures.

### Quantum Computing's Impact on Cryptography
Details how quantum algorithms like Shor's and Grover's threaten current cryptographic systems, with timeline predictions and risk assessment.

### Quantum-Resistant Cryptography
Explores post-quantum cryptography approaches, standardization efforts, and implementation considerations.

### Challenges
Examines technical hurdles in quantum computing development and practical implementation issues for quantum-safe cryptography.

### Future Prospects
Looks at anticipated developments in quantum hardware, algorithms, networks, and integration with other technologies.

### Societal Implications
Analyzes broader impacts on security paradigms, privacy, economics, national security, and geopolitics.

## Progress Tracking
See `progress_tracker.md` for detailed progress on each chapter and section.

## Citation
If you use content from this memoir, please cite:
```
Sergonne, L. (2025). Quantum Computing and Its Impact on Cryptography [Memoir].
```

## License
All rights reserved, 2024-2025.

# Source Tracking and Bibliography System

This document explains how to use the source tracking and bibliography system for the "Quantum Computing and Its Impact on Cryptography" thesis.

## Overview

Your bibliography system consists of:

1. **bibliography.bib** - The main BibTeX file containing all your references
2. **Source tracking tables** in progress_tracker.md to monitor which sources are used in each chapter
3. **Citation commands** in your LaTeX documents to reference sources

## How to Use the Bibliography System

### Adding New Sources

1. Open `bibliography.bib` and add your new reference in BibTeX format
2. Use the appropriate entry type (@book, @article, @online, etc.)
3. Assign a unique citation key (e.g., `author2025title`) that follows the pattern
4. Include all required fields for that entry type

Example:
```bibtex
@article{new_author2025title,
  title={Article Title},
  author={New, Author},
  journal={Journal Name},
  volume={5},
  number={2},
  pages={123--145},
  year={2025},
  publisher={Publisher Name},
  note={Relevant note about this source}
}
```

### Citing Sources in Your LaTeX Documents

Use standard biblatex citation commands in your .tex files:

- `\cite{key}` - Basic citation (produces [ABC12] with alphabetic style)
- `\textcite{key}` - Author name in text (produces "Author et al. [ABC12]")
- `\parencite{key}` - Citation in parentheses (recommended for most cases)
- `\footcite{key}` - Citation as footnote
- `\autocite{key}` - Context-sensitive citation (recommended)

Examples:
```latex
According to \textcite{nielsen2010quantum}, quantum gates are...

The superposition principle allows qubits to exist in multiple states simultaneously \parencite{feynman1965feynman}.

Shor's algorithm poses a significant threat to RSA encryption\autocite{shor1997polynomial}.
```

### Multiple Citations
```latex
Several researchers have investigated this phenomenon \parencite{nielsen2010quantum,shor1997polynomial,grover1997quantum}.
```

### Adding Page Numbers
```latex
This concept is explained in detail by \textcite[p.~123]{nielsen2010quantum}.
```

### Tracking Sources in Your Thesis

1. Update the "Source Tracking System" table in progress_tracker.md whenever you use a new source
2. Record which chapters use the source and the approximate citation count
3. Update the "Primary Sources" column in the detailed chapter tracking tables

## Compiling Your Document with Bibliography

1. Compile your main TeX file with your LaTeX compiler (pdflatex)
2. Run biber to process the bibliography
3. Compile your TeX file again (twice) to update references

Example compilation sequence:
```
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

## Tips for Effective Source Management

1. **Be consistent** with citation keys (author+year+word format)
2. **Add notes** to your BibTeX entries to remind yourself of important content
3. **Group sources** by topic using comments in the .bib file
4. **Update the tracking system** regularly as you work on each chapter
5. **Verify your citations** with the original sources before final submission

## Adding the Bibliography to Your Document

Add these commands at the end of your document where you want the bibliography to appear:

```latex
\printbibliography[title=References]
```

Or use sections for a more organized bibliography:

```latex
\printbibliography[type=book,title=Books]
\printbibliography[type=article,title=Articles]
\printbibliography[type=online,title=Online Resources]
```