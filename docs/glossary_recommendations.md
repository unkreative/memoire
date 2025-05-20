# Recommended Glossary Entries

This document contains suggestions for additional terms that would benefit from glossary entries in the thesis.

## Quantum Computing Concepts

1. **Quantum Phase Estimation (QPE)**
   - Critical component in Shor's algorithm
   - Used for finding eigenvalues of unitary operators
   - Direct application in period-finding for cryptanalysis

2. **Quantum Fourier Transform (QFT)**
   - Fundamental quantum algorithm used in Shor's algorithm
   - Transforms quantum states similar to classical Fourier transform
   - Key to achieving exponential speedup in certain algorithms

3. **NISQ (Noisy Intermediate-Scale Quantum)**
   - Describes current era of quantum computing
   - Characterized by 50-1000 noisy qubits
   - Important for understanding near-term quantum threats

4. **Quantum Error Correction (QEC)**
   - Essential for fault-tolerant quantum computing
   - Uses multiple physical qubits to create logical qubits
   - Critical for practical implementation of quantum algorithms

## Cryptographic Concepts

5. **Learning With Errors (LWE)**
   - Fundamental problem in lattice-based cryptography
   - Basis for CRYSTALS-Kyber and other PQC schemes
   - Presumed quantum-resistant

6. **Side-Channel Attack**
   - Non-cryptanalytic attack exploiting implementation characteristics
   - Important consideration in PQC implementations
   - Examples include timing and power analysis attacks

7. **Cryptographic Agility**
   - Ability to quickly replace cryptographic algorithms
   - Critical for post-quantum transition
   - Important design principle for modern systems

8. **Store Now, Decrypt Later (SNDL)**
   - Attack strategy storing encrypted data for future quantum decryption
   - Immediate threat even before quantum computers exist
   - Drives urgency for PQC adoption

## Post-Quantum Cryptography Categories

9. **Module-LWE**
   - Variant of Learning With Errors
   - Used in CRYSTALS-Kyber
   - Provides good balance of security and efficiency

10. **Merkle-Damgård Construction**
    - Design principle for hash functions
    - Relevant to hash-based signatures
    - Important for understanding SPHINCS+

11. **Multivariate Cryptography**
    - PQC category based on polynomial equations
    - Security based on MQ problem
    - Historical examples include Rainbow (broken)

12. **Code-Based Cryptography**
    - PQC category using error-correcting codes
    - Example: Classic McEliece
    - Based on hardness of decoding problems

## Implementation Concepts

13. **Quantum Circuit**
    - Basic model of quantum computation
    - Composed of quantum gates and measurements
    - Important for understanding quantum algorithms

14. **Hybrid Cryptography**
    - Combined use of classical and post-quantum algorithms
    - Common transition strategy
    - Provides defense in depth

15. **NIST Security Levels**
    - Standardized security strength categories for PQC
    - Ranges from Level 1 to Level 5
    - Important for algorithm selection

Each of these terms appears in the thesis and would benefit from formal definition in the glossary to aid reader understanding and maintain consistency throughout the document.