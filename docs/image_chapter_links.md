# Image Usage Mapping
[[thesis_overview|← Back to Overview]]

#figures #documentation #cross-reference

## Direct Image Usage by Chapter

### Chapter 1: Introduction
- [[src/images/01_Introduction/quantum_vs_classical.png|quantum_vs_classical]]
  - **Usage**: Section 1.2 (Quantum Computing: A Paradigm Shift)
  - **Purpose**: Illustrates fundamental differences between classical and quantum computing
  - **Related Concepts**: Quantum paradigm shift, computational models

### Chapter 2: Fundamentals
- [[src/images/02_Fundamentals_of_Quantum_Computing/bloch_sphere.png|bloch_sphere]]
  - **Usage**: Section 2.1.3 (Quantum Bits)
  - **Purpose**: Visualizes qubit states on the Bloch sphere
  - **Caption**: "The Bloch sphere representation of a single qubit state |ψ⟩"

- [[src/images/02_Fundamentals_of_Quantum_Computing/quantum_gates.png|quantum_gates]]
  - **Usage**: Section 2.2 (Quantum Gates and Circuits)
  - **Purpose**: Shows basic quantum gate operations

- [[src/images/02_Fundamentals_of_Quantum_Computing/qft_circuit.png|qft_circuit]]
  - **Usage**: Section 2.3.1 (Quantum Fourier Transform)
  - **Reference**: Figure 2.2 in text
  - **Related to**: Shor's algorithm implementation

- [[src/images/02_Fundamentals_of_Quantum_Computing/amplitude_amplification.png|amplitude_amplification]]
  - **Usage**: Section 2.3.3 (Amplitude Amplification)
  - **Purpose**: Geometric visualization of amplitude amplification
  - **Related to**: Grover's algorithm fundamentals

### Chapter 3: Classical Cryptography
- [[src/images/03_Classical_Cryptography/enigma_rotors.jpg|enigma]]
  - **Usage**: Section 3.1 (Historical Development)
  - **Reference**: Figure 3.1 in text
  - **Caption**: "Internal mechanism of the Enigma machine"

- [[src/images/03_Classical_Cryptography/aes_gcm_workflow.png|aes_gcm]]
  - **Usage**: Section 3.3.2 (Block Ciphers and Modes)
  - **Reference**: Figure 3.3
  - **Caption**: "AES-GCM authenticated encryption workflow"

- [[src/images/03_Classical_Cryptography/rsa_encryption.png|rsa]]
  - **Usage**: Section 3.4.1 (RSA Algorithm)
  - **Links to**: Chapter 5's discussion of Shor's algorithm impact

### Chapter 4: Classical vs Quantum
(No direct image usage, but references images from Chapters 2 and 3)

### Chapter 5: Quantum Impact
- [[src/images/05_Quantum_Impact_on_Cryptography/shor_algorithm.png|shors]]
  - **Usage**: Section 5.2 (Shor's Algorithm: The Mechanism)
  - **References**: RSA and ECC from Chapter 3
  - **Impact Flow**: Classical Cryptography → Quantum Attack

- [[src/images/05_Quantum_Impact_on_Cryptography/grovers_algorithm.png|grovers]]
  - **Usage**: Section 5.4 (Grover's Algorithm)
  - **Links back to**: Amplitude amplification (Chapter 2)

### Chapter 6: Challenges
- [[src/images/06_Challenges_in_Transition/nist_timeline.png|nist]]
  - **Usage**: Section 5.8.1 (NIST Standardization)
  - **Purpose**: Timeline visualization of PQC standardization

- [[src/images/06_Challenges_in_Transition/quantum_key_distribution.png|qkd]]
  - **Usage**: Section 6.3 (Digital Trust)
  - **Links to**: Future security solutions

## Image Relationship Map
```mermaid
graph TD
    subgraph CH1[Introduction]
        qvc[quantum_vs_classical.png]
    end
    
    subgraph CH2[Quantum Fundamentals]
        bs[Bloch Sphere]
        qft[QFT Circuit]
        qpe[QPE Circuit]
        qg[Quantum Gates]
        aa[Amplitude Amplification]
    end
    
    subgraph CH3[Classical Crypto]
        en[Enigma]
        aes[AES-GCM]
        rsa[RSA]
        ecc[ECC]
    end
    
    subgraph CH5[Quantum Impact]
        shor[Shor's Algorithm]
        grover[Grover's Algorithm]
    end
    
    subgraph CH6[Challenges]
        nist[NIST Timeline]
        qkd[QKD]
        lat[Lattice]
    end
    
    % Core concept flows
    qvc --> bs
    bs --> qg
    qg --> qft
    qft --> shor
    aa --> grover
    
    % Attack relationships
    rsa --> shor
    ecc --> shor
    
    % Solution flows
    shor --> lat
    grover --> qkd
    lat --> nist
```

## Usage Analysis
- **Most Referenced**: quantum_gates.png (used in multiple sections)
- **Key Visualization**: bloch_sphere.png (fundamental quantum concept)
- **Historical Context**: enigma_rotors.jpg
- **Critical Impact**: shor_algorithm.png (shows threat to classical crypto)
- **Future Direction**: nist_timeline.png (standardization roadmap)

## LaTeX Cross-References
All images are properly referenced using:
```latex
\includegraphics[width=0.8\textwidth]{chapter_name/image_name}
```
And are labeled with:
```latex
\label{fig:unique_label}
```

## Related Documentation
- [[docs/concept_map|Concept Map]] for theoretical relationships
- [[docs/chapter_dependencies|Chapter Dependencies]] for structural flow
- [[docs/image_metadata|Image Metadata]] for file details