#!/bin/bash

# Simple wrapper script to run the compilation script from the root directory
echo "Running thesis compilation..."
echo "Starting LaTeX thesis compilation..."
echo "Running pdflatex (pass 1)..."
pdflatex -output-directory=build main
echo "Running biber..."
biber build/main
echo "Running makeglossaries..."
makeglossaries -d build main
echo "Running pdflatex (pass 2)..."
pdflatex -output-directory=build main
echo "Running pdflatex (final pass)..."
pdflatex -output-directory=build main
echo "Copying PDF to main directory..."
cp build/main.pdf .
echo "LaTeX thesis compilation is complete. Look for main.pdf in the output."