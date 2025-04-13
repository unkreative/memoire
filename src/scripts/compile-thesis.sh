#!/bin/bash

# Enhanced script to compile the LaTeX thesis with organized directories
echo "Compiling LaTeX thesis..."

# Set working directory to the project root
cd "$(dirname "$0")/../.."

# Set the PATH to include TeX binaries
export PATH="/Library/TeX/texbin:$PATH"

# Create build directory if it doesn't exist
mkdir -p build

# Create a symlink to the bibliography file in the build directory
if [ ! -L "build/bibliography.bib" ]; then
  ln -sf "$(pwd)/src/bibliography/bibliography.bib" "build/bibliography.bib"
fi

# Run pdflatex on main.tex with output directory set to build
echo "Running first pdflatex pass..."
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error -output-directory=build main.tex

# Run biber for bibliography
echo "Running biber for bibliography..."
biber --output-directory build build/main

# Run pdflatex twice more to resolve references
echo "Running second pdflatex pass..."
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error -output-directory=build main.tex
echo "Running final pdflatex pass..."
pdflatex -synctex=1 -interaction=nonstopmode -file-line-error -output-directory=build main.tex

# Copy the final PDF to the main directory for convenience
echo "Copying PDF to main directory..."
cp build/main.pdf . 2>/dev/null || echo "Warning: No PDF was generated"

echo "Compilation complete. Check for main.pdf in the output."