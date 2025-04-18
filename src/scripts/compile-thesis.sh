#!/bin/bash

# Script to compile the LaTeX thesis, now with organized directories for clarity
echo "Starting LaTeX thesis compilation..."

# Move to the project root directory for consistent operations
cd "$(dirname "$0")/../.."

# Ensure TeX binaries are in the PATH for pdflatex and biber
export PATH="/Library/TeX/texbin:$PATH"

# Create the build directory if it's not already there - keeps things tidy
mkdir -p build

# Create a symbolic link to the bibliography in the build directory if it doesn't exist
if [ ! -L "build/bibliography.bib" ]; then
  ln -sf "$(pwd)/src/bibliography/bibliography.bib" "build/bibliography.bib"
fi

# First pass of pdflatex: compile main.tex, output to build directory
echo "Running pdflatex (pass 1)..."
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error -output-directory=build main.tex

# Run biber to process the bibliography for citations
echo "Running biber..."
biber --output-directory build build/main

# Second and third pdflatex passes to resolve references and citations
echo "Running pdflatex (pass 2)..."
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error -output-directory=build main.tex
echo "Running pdflatex (final pass)..."
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error -output-directory=build main.tex

# Copy the generated PDF to the main directory for easy access
echo "Copying PDF to main directory..."
cp build/main.pdf . 2>/dev/null || echo "Warning: PDF generation might have failed"

echo "LaTeX thesis compilation is complete. Look for main.pdf in the output."