# Image Reference Guide for Thesis

This document provides guidance on using the images in your thesis, organized by chapter.

## Image Inventory

Your `src/images/` directory contains the following files:
- bloch_sphere.png - Representation of qubits on the Bloch sphere
- grovers_algorithm.png - Diagram of Grover's search algorithm
- lattice_cryptography.png - Illustration of lattice-based cryptography
- nist_timeline.png - NIST's post-quantum cryptography standardization timeline
- post_quantum_comparison.png - Comparison of post-quantum cryptography approaches
- quantum_gates.png - Common quantum logic gates
- quantum_key_distribution.png - Quantum key distribution (BB84) protocol
- quantum_vs_classical.png - Comparison of quantum vs. classical computing
- rsa_encryption.png - RSA encryption process diagram
- shor_algorithm.png - Diagram of Shor's factorization algorithm
- wave-particle-duality1.png - Double-slit experiment illustration

## Suggested Image Usage by Chapter

### Chapter 1: Introduction
- quantum_vs_classical.png
  - Caption: "Figure 1.1: Comparison of classical and quantum computing paradigms"
  - Usage: Section 1.3 "Comparison with Classical Computing"

### Chapter 2: Fundamentals
- wave-particle-duality1.png
  - Caption: "Figure 2.1: The double-slit experiment demonstrating wave-particle duality"
  - Usage: Section on Quantum Mechanics Principles

- bloch_sphere.png
  - Caption: "Figure 2.2: The Bloch sphere representation of a qubit"
  - Usage: Section on Qubits and Quantum States

- quantum_gates.png
  - Caption: "Figure 2.3: Common quantum logic gates and their matrix representations"
  - Usage: Section on Quantum Gates and Circuits

### Chapter 3: Classical vs. Quantum Computing
- quantum_vs_classical.png
  - Caption: "Figure 3.1: Comparison of classical logic circuits and quantum circuits"
  - Usage: Section on Bits vs. Qubits

### Chapter 4: Classical Cryptography
- rsa_encryption.png
  - Caption: "Figure 4.1: The RSA encryption and decryption process"
  - Usage: Section on Public-Key Cryptography

### Chapter 5: Quantum Impact on Cryptography
- shor_algorithm.png
  - Caption: "Figure 5.1: Shor's algorithm for integer factorization"
  - Usage: Section on Threats to Public-Key Cryptography

- grovers_algorithm.png
  - Caption: "Figure 5.2: Grover's search algorithm and its impact on symmetric cryptography"
  - Usage: Section on Threats to Symmetric Cryptography

### Chapter 6: Quantum-Resistant Cryptographic Methods
- post_quantum_comparison.png
  - Caption: "Figure 6.1: Comparison of post-quantum cryptographic approaches"
  - Usage: Section on Overview of Post-Quantum Approaches

- lattice_cryptography.png
  - Caption: "Figure 6.2: Lattice-based cryptography principles"
  - Usage: Section on Lattice-Based Cryptography

- quantum_key_distribution.png
  - Caption: "Figure 6.3: Quantum Key Distribution (BB84) protocol"
  - Usage: Section on Quantum Cryptography

- nist_timeline.png
  - Caption: "Figure 6.4: NIST's post-quantum cryptography standardization timeline"
  - Usage: Section on Standardization Efforts

## How to Include Images in LaTeX

To include an image in your LaTeX document, use the following template:

```latex
\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\textwidth]{filename.png}
    \caption{Your caption text here}
    \label{fig:unique-label}
\end{figure}
```

Note that you don't need to include the `src/images/` path in the \includegraphics command because the preamble already sets up the correct path with:
```latex
\graphicspath{{src/images/}}
```

You can reference the figure elsewhere in your text using:

```latex
As shown in Figure~\ref{fig:unique-label}, the quantum gate...
```

## Tips for Working with Images

1. **Image Placement**: The `[h]` parameter attempts to place the figure "here". Other options include `[t]` (top), `[b]` (bottom), and `[p]` (separate page).

2. **Image Sizing**: Adjust the `width=0.8\textwidth` parameter as needed. You can use percentages of `\textwidth` or specific dimensions like `width=10cm`.

3. **Multi-Part Figures**: For complex comparisons, use the `subfigure` environment:

```latex
\begin{figure}[h]
    \centering
    \begin{subfigure}[b]{0.45\textwidth}
        \includegraphics[width=\textwidth]{images/first-image.png}
        \caption{First part}
        \label{fig:first}
    \end{subfigure}
    \hfill
    \begin{subfigure}[b]{0.45\textwidth}
        \includegraphics[width=\textwidth]{images/second-image.png}
        \caption{Second part}
        \label{fig:second}
    \end{subfigure}
    \caption{Overall caption for both images}
    \label{fig:overall}
\end{figure}
```