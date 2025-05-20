#!/usr/bin/env python3
import requests
import time
import json
import urllib.parse
import argparse # Import argparse for command-line arguments
import os

# === Keyword Lists ===
KEYWORDS_CH01_INTRODUCTION = {
    "filename_suffix": "ch01_introduction",
    "keywords": [
        "Quantum Computing Introduction",
        "Quantum Computing Impact Cryptography",
        "Quantum Computing Vulnerabilities Cryptography",
        "Quantum-Resistant Cryptography Introduction",
        "Quantum Computing vs Classical Computing Cryptography",
        "Shor's Algorithm Impact Public Key Cryptography",
        "Grover's Algorithm Impact Symmetric Key Cryptography",
        "Post-Quantum Cryptography PQC Transition Introduction",
        "Quantum Key Distribution QKD Overview",
        "Quantum Computing Paradigm Shift",
        "Store Now Decrypt Later SNDL Introduction",
    ]
}

KEYWORDS_CH02_FUNDAMENTALS = {
    "filename_suffix": "ch02_fundamentals",
    "keywords": [
        "Quantum Mechanics Principles",
        "Superposition in Quantum Computing",
        "Quantum Entanglement",
        "Qubit Definition and Properties",
        "Bloch Sphere Representation",
        "Physical Implementations of Qubits Superconducting",
        "Physical Implementations of Qubits Trapped Ion",
        "Physical Implementations of Qubits Photonic",
        "Quantum Coherence",
        "Quantum Decoherence",
        "Quantum Gates Pauli",
        "Quantum Gates Hadamard",
        "Quantum Gates CNOT",
        "Quantum Gates Toffoli",
        "Unitary Transformations Quantum Computing",
        "Quantum Circuits Design",
        "Bell State Generation",
        "Quantum Fourier Transform QFT",
        "Quantum Phase Estimation QPE",
        "Amplitude Amplification Quantum",
        "Grover's Search Algorithm",
        "Shor's Algorithm Factoring",
        "Shor's Algorithm Discrete Logarithm",
        "Quantum Cryptanalysis",
        "Quantum Impact RSA",
        "Quantum Impact Diffie-Hellman",
        "Quantum Impact Elliptic Curve Cryptography ECC",
        "Grover Algorithm Impact AES",
        "Grover Algorithm Impact Hash Functions",
        "Noisy Intermediate-Scale Quantum NISQ",
        "Quantum Error Correction QEC",
        "Fault-Tolerant Quantum Computing",
        "Quantum Advantage",
    ]
}

KEYWORDS_CH03_CLASSICAL_CRYPTO = {
    "filename_suffix": "ch03_classical_crypto",
    "keywords": [
        "History of Cryptography Ancient",
        "History of Cryptography Classical",
        "History of Cryptography Mechanical",
        "History of Cryptography Modern",
        "Caesar Cipher",
        "Vigenere Cipher",
        "Enigma Machine Cryptanalysis",
        "Shannon Information Theory Cryptography",
        "Kerckhoffs Principle",
        "Cryptographic Security Goals Confidentiality",
        "Cryptographic Security Goals Integrity",
        "Cryptographic Security Goals Authentication",
        "Cryptographic Security Goals Non-repudiation",
        "Computational Hardness Assumptions Cryptography",
        "One-way Functions Cryptography",
        "Trapdoor Functions Cryptography",
        "Symmetric Key Cryptography",
        "Secret Key Distribution Problem",
        "Substitution-Permutation Network SPN",
        "S-box Substitution Box",
        "Confusion and Diffusion Cryptography",
        "Key Scheduling Algorithm",
        "Side-Channel Attack Timing",
        "Side-Channel Attack Power Analysis",
        "Block Cipher AES",
        "Block Cipher Modes of Operation ECB CBC GCM",
        "Grover Algorithm Impact Symmetric Keys",
        "Public Key Cryptography Asymmetric",
        "RSA Algorithm Key Generation",
        "RSA Algorithm Encryption Decryption",
        "Integer Factorization Problem IFP",
        "Euler Totient Function",
        "RSA Quantum Threat Shor Algorithm",
        "RSA Implementation Attack Padding Oracle Bleichenbacher",
        "Elliptic Curve Cryptography ECC",
        "Elliptic Curve Discrete Logarithm Problem ECDLP",
        "ECC Key Size Advantage",
        "Elliptic Curve Point Addition Scalar Multiplication",
        "ECC Quantum Threat Shor Algorithm",
        "Diffie-Hellman Key Exchange DH",
        "Discrete Logarithm Problem DLP",
        "Man-in-the-Middle Attack MitM Cryptography",
        "Cryptographic Hash Functions",
        "Hash Function Properties Pre-image Resistance",
        "Hash Function Properties Second Pre-image Resistance",
        "Hash Function Properties Collision Resistance",
        "MD5 SHA-1 Collision Attack",
        "SHA-2 Hash Family",
        "SHA-3 Hash Family Keccak",
        "Merkle-Damgard Construction",
        "Sponge Construction Cryptography",
        "Hash Function Quantum Impact Grover Birthday Attack",
        "Digital Signatures Authentication Integrity Non-repudiation",
        "Public Key Infrastructure PKI",
        "Certificate Authority CA PKI",
        "Digital Certificates X.509",
        "Certificate Revocation List CRL OCSP",
        "Digital Signature Quantum Threat Shor Algorithm",
        "Cryptographic Protocol Design Security",
        "Cryptographic Implementation Vulnerabilities",
    ]
}

KEYWORDS_CH04_CLASSICAL_VS_QUANTUM = {
    "filename_suffix": "ch04_classical_vs_quantum",
    "keywords": [
        "Classical vs Quantum Computing Comparison",
        "Bit vs Qubit Information Representation",
        "Quantum Superposition Principle",
        "Quantum Entanglement Resource",
        "No-Cloning Theorem Implications",
        "Classical Computation Model Turing Machine",
        "Classical Computation Model Von Neumann",
        "Quantum Computation Model Quantum Circuit",
        "Unitary Transformations Quantum Computing",
        "Hilbert Space Representation Quantum State",
        "Quantum Parallelism Concept",
        "Quantum Interference Role",
        "Computational Complexity Theory",
        "Complexity Class P Polynomial Time",
        "Complexity Class NP Nondeterministic Polynomial",
        "Complexity Class BPP Bounded-error Probabilistic Polynomial",
        "Complexity Class BQP Bounded-error Quantum Polynomial",
        "Relationship P BPP BQP NP Complexity Classes",
        "Shor Algorithm Complexity Impact Factoring DLP",
        "Grover Algorithm Complexity Impact Search",
    ]
}

KEYWORDS_CH05_QUANTUM_IMPACT = {
    "filename_suffix": "ch05_quantum_impact",
    "keywords": [
        "Quantum Impact on Cryptography",
        "Shor's Algorithm Cryptographic Impact",
        "Shor's Algorithm Integer Factorization Impact",
        "Shor's Algorithm Discrete Logarithm Impact",
        "Quantum Threat to RSA",
        "Quantum Threat to Diffie-Hellman DH DSA",
        "Quantum Threat to Elliptic Curve Cryptography ECC ECDH ECDSA",
        "Classical vs Quantum Factoring Complexity",
        "Cryptographically Relevant Quantum Computer CRQC",
        "Quantum Threat to TLS HTTPS SSH",
        "Quantum Threat to Public Key Infrastructure PKI",
        "Grover's Algorithm Cryptographic Impact",
        "Quantum Amplitude Amplification Mechanism",
        "Grover's Algorithm Impact Symmetric Key Search",
        "Quantum Impact on AES Security Levels",
        "Grover's Algorithm Impact Hash Pre-image Resistance",
        "Grover's Algorithm Impact Hash Collision Resistance",
        "Quantum Security Levels Adjustment",
        "NIST Security Levels Post-Quantum",
        "Post-Quantum Cryptography PQC Necessity",
        "Classical vs Quantum Security Comparison",
        "Quantum Computing Timeline Estimates",
        "Quantum Error Correction QEC Requirement",
        "NISQ Era vs Fault-Tolerant Quantum Computing",
        "Store Now Decrypt Later SNDL Threat",
        "Mosca's Inequality X+Y > Z",
        "Security Shelf Life Cryptography",
        "Cryptographic Migration Time",
    ]
}

KEYWORDS_CH06_QUANTUM_RESISTANT = {
    "filename_suffix": "ch06_quantum_resistant",
    "keywords": [
        "Post-Quantum Cryptography PQC",
        "Quantum-Resistant Cryptography",
        "Lattice-Based Cryptography",
        "Mathematical Lattices Definition",
        "Shortest Vector Problem SVP",
        "Closest Vector Problem CVP",
        "Learning With Errors LWE Problem",
        "Quantum Resistance LWE",
        "Ring-LWE RLWE",
        "Module-LWE MLWE",
        "Lattice Cryptography Efficiency",
        "Lattice Cryptography Key Size",
        "CRYSTALS-Kyber KEM",
        "CRYSTALS-Dilithium Signature",
        "Falcon Signature",
        "NTRU Lattice Problem",
        "Hash-Based Cryptography Signatures",
        "One-Time Signatures OTS Lamport",
        "Merkle Tree Signatures",
        "Stateful Hash-Based Signatures XMSS LMS",
        "Stateless Hash-Based Signatures SPHINCS+",
        "Code-Based Cryptography",
        "McEliece Cryptosystem",
        "Goppa Codes Cryptography",
        "Niederreiter Cryptosystem",
        "Code-Based Cryptography Key Size",
        "Classic McEliece KEM",
        "Multivariate Cryptography",
        "Multivariate Polynomial Equations MQ Problem",
        "Multivariate Signatures",
        "NIST PQC Standardization Process",
        "NIST PQC Finalists Candidates",
        "PQC Implementation Considerations",
        "PQC Performance Trade-offs",
        "PQC Side-Channel Attacks",
        "PQC Integration Complexity",
        "Hybrid Cryptography PQC Classical",
        "Hybrid Key Exchange",
        "Hybrid Signatures",
    ]
}

KEYWORDS_CH07_CHALLENGES = {
    "filename_suffix": "ch07_challenges",
    "keywords": [
        "Post-Quantum Cryptography PQC Transition Challenges",
        "PQC Performance Overhead Speed Size",
        "PQC Computational Speed Comparison",
        "PQC Key Size Signature Size Impact",
        "PQC Ciphertext Size Impact",
        "PQC Implementation Challenges",
        "PQC System Integration Complexity",
        "PQC Legacy System Compatibility",
        "PQC Protocol Modifications TLS SSH",
        "PQC Hardware Constraints IoT Smart Cards",
        "PQC Software Ecosystem Updates Libraries OS",
        "PQC Infrastructure Updates KMS HSM PKI",
        "PQC Certificate Size Validation",
        "PQC Implementation Security",
        "PQC Side-Channel Attack Vulnerabilities",
        "PQC Constant-Time Implementation",
        "PQC Algorithmic Complexity Bugs",
        "PQC Development Tooling Testing",
        "PQC Migration Strategy Challenges",
        "Cryptographic Agility",
        "PQC Hybrid Mode Deployment Classical PQC",
        "PQC Backward Compatibility Interoperability",
        "PQC Downgrade Attacks",
        "Crypto-Inventory Dependency Analysis",
        "PQC Migration Prioritization",
        "PQC Resource Constraints Hardware Software",
        "PQC Memory Usage RAM Cache",
        "PQC Processing Power Requirements",
        "PQC Bandwidth Consumption",
        "PQC Expertise Personnel Shortage",
        "PQC Training Needs",
        "PQC Vendor Support",
        "PQC Security Confidence Risk Management",
        "Trust in New PQC Algorithms",
        "PQC Mathematical Assumptions Hardness",
        "PQC Parameter Selection Security",
        "PQC Standardization Challenges",
        "NIST PQC Process Timeline Status",
        "International PQC Standards Harmonization ISO ETSI IETF",
        "PQC Conformance Testing Validation",
        "PQC Cost Economic Impact",
        "PQC Direct Costs Hardware Software Testing",
        "PQC Indirect Costs Training Operations",
    ]
}

KEYWORDS_CH08_CONCLUSION = {
    "filename_suffix": "ch08_conclusion",
    "keywords": [
        "Quantum Computing Cryptography Thesis Summary",
        "Quantum Threat Summary Shor Grover",
        "Post-Quantum Cryptography PQC Solutions Review",
        "PQC Algorithm Families Comparison Lattice Hash Code",
        "PQC Transition Challenges Summary",
        "PQC Migration Planning Importance",
        "Hybrid Cryptography Role Conclusion",
        "PQC Societal Implications",
        "PQC Economic Impact Costs",
        "PQC Privacy Implications SNDL",
        "PQC National Security Geopolitics",
        "Future Research PQC Algorithm Refinement",
        "Future Research PQC Implementation Security",
        "Future Research PQC Standardization Interoperability",
        "Future Research Hybrid Systems PQC",
        "Quantum Hardware Progress Monitoring",
        "Quantum Key Distribution QKD Future Prospects",
        "Cryptographic Agility Importance Conclusion",
        "Post-Quantum Future Preparedness",
    ]
}

# Add more keyword lists here as needed
AVAILABLE_KEYWORD_SETS = {
    'ch1': KEYWORDS_CH01_INTRODUCTION,
    'ch2': KEYWORDS_CH02_FUNDAMENTALS,
    'ch3': KEYWORDS_CH03_CLASSICAL_CRYPTO,
    'ch4': KEYWORDS_CH04_CLASSICAL_VS_QUANTUM,
    'ch5': KEYWORDS_CH05_QUANTUM_IMPACT,
    'ch6': KEYWORDS_CH06_QUANTUM_RESISTANT,
    'ch7': KEYWORDS_CH07_CHALLENGES,
    'ch8': KEYWORDS_CH08_CONCLUSION,
    # Add keys for future chapters, e.g., 'ch9': KEYWORDS_CH09_... 
}

# === Configuration === (Default values, can be overridden by command line args)
DEFAULT_OUTPUT_DIR = "semantic_scholar_results"
BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
LIMIT = 5
FIELDS = "paperId,title,year,authors,abstract,url,citationStyles" # Added paperId for potential future use
MAX_RETRIES = 5
INITIAL_BACKOFF = 2  # Initial wait time in seconds for 429 error (increased slightly)
REQUEST_DELAY = 1.5  # Delay between different keyword searches in seconds (increased slightly)
TIMEOUT = 30 # Request timeout in seconds
# === End Configuration ===

def search_semantic_scholar(keyword, base_url, limit, fields, max_retries, initial_backoff, timeout):
    """Searches Semantic Scholar for a keyword with retry logic for 429 errors."""
    encoded_keyword = urllib.parse.quote(keyword)
    api_url = f"{base_url}?query={encoded_keyword}&limit={limit}&fields={fields}"
    
    retries = 0
    backoff_time = initial_backoff
    
    while retries < max_retries:
        try:
            print(f"    Attempting request for '{keyword}' (try {retries + 1}/{max_retries})...", flush=True)
            response = requests.get(api_url, timeout=timeout)
            
            if response.status_code == 200:
                print(f"    Success for '{keyword}'.")
                try:
                    return response.json()
                except json.JSONDecodeError:
                    print(f"    Error: Could not decode JSON response for '{keyword}'. Response text: {response.text}")
                    return None # Indicate JSON decode failure
            elif response.status_code == 429:
                wait_time = backoff_time + (time.time() % 1) # Add jitter
                print(f"    Received 429 (Too Many Requests) for '{keyword}'. Waiting {wait_time:.2f} seconds...")
                time.sleep(wait_time)
                # Exponential backoff: double the wait time for the next retry
                backoff_time = min(backoff_time * 2, 60) # Cap backoff at 60s
                retries += 1
            else:
                print(f"    Error: Received status code {response.status_code} for '{keyword}'. Response: {response.text}")
                return None # Indicate non-429 error
                
        except requests.exceptions.RequestException as e:
            print(f"    Error: Request failed for '{keyword}': {e}")
            # Consider adding backoff for transient network errors too
            # For now, just retry immediately up to max_retries
            retries += 1 
            if retries < max_retries:
                 print(f"    Retrying after request error...")
                 time.sleep(1) # Small delay before retry on general error
            else:
                 print(f"    Max retries reached after request error for '{keyword}'.")
                 return None # Indicate request exception after retries
            
    print(f"    Error: Max retries reached for '{keyword}' after 429 responses. Giving up.")
    return None # Indicate max retries exceeded

def main():
    parser = argparse.ArgumentParser(description="Search Semantic Scholar for predefined keyword sets.")
    parser.add_argument(
        'keyword_set', 
        choices=AVAILABLE_KEYWORD_SETS.keys(), 
        help=f"Which set of keywords to use ({', '.join(AVAILABLE_KEYWORD_SETS.keys())})"
    )
    parser.add_argument(
        '--output-dir', 
        default=DEFAULT_OUTPUT_DIR, 
        help=f"Directory to save the output JSONL file (default: {DEFAULT_OUTPUT_DIR})"
    )
    parser.add_argument(
        '--limit', 
        type=int, 
        default=LIMIT, 
        help=f"Number of results per keyword (default: {LIMIT})"
    )
    parser.add_argument(
        '--max-retries', 
        type=int, 
        default=MAX_RETRIES, 
        help=f"Maximum retries on 429 error (default: {MAX_RETRIES})"
    )
    parser.add_argument(
        '--initial-backoff', 
        type=float, 
        default=INITIAL_BACKOFF, 
        help=f"Initial backoff delay in seconds for 429 error (default: {INITIAL_BACKOFF})"
    )
    parser.add_argument(
        '--request-delay', 
        type=float, 
        default=REQUEST_DELAY, 
        help=f"Delay between keyword searches in seconds (default: {REQUEST_DELAY})"
    )

    args = parser.parse_args()

    selected_set = AVAILABLE_KEYWORD_SETS[args.keyword_set]
    keywords_to_search = selected_set['keywords']
    filename_suffix = selected_set['filename_suffix']
    
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    output_file = os.path.join(args.output_dir, f"results_{filename_suffix}.jsonl")

    # Clear the output file
    with open(output_file, 'w') as f:
        pass
    print(f"Cleared output file: {output_file}")

    print(f"Starting search for keyword set: {args.keyword_set}")
    print(f"Output will be saved to: {output_file}")
    print(f"Limit per keyword: {args.limit}")
    print(f"Max retries on 429: {args.max_retries}")
    print(f"Request delay: {args.request_delay}s")

    total_keywords = len(keywords_to_search)
    successful_keywords = 0
    failed_keywords = []

    for i, keyword in enumerate(keywords_to_search):
        print(f"\n[{i+1}/{total_keywords}] Processing keyword: {keyword}")
        
        result_data = search_semantic_scholar(
            keyword,
            BASE_URL,
            args.limit,
            FIELDS,
            args.max_retries,
            args.initial_backoff,
            TIMEOUT
        )

        if result_data and 'data' in result_data:
            num_papers = len(result_data.get('data', []))
            if num_papers > 0:
                with open(output_file, 'a', encoding='utf-8') as f:
                    for paper in result_data['data']:
                        # Add the search keyword that found this paper
                        paper['search_keyword'] = keyword 
                        json.dump(paper, f, ensure_ascii=False)
                        f.write('\n')
                print(f"  -> Successfully wrote {num_papers} results for '{keyword}' to {output_file}")
                successful_keywords += 1
            else:
                 print(f"  -> No papers found for '{keyword}'.")
                 successful_keywords += 1 # Count as success if API call worked but returned 0 results
        elif result_data: # Response received but no 'data' field
             print(f"  -> Warning: No paper data found in response for '{keyword}'. Response: {result_data}")
             failed_keywords.append(keyword)
        else:
             print(f"  -> Error: Failed to retrieve or process data for '{keyword}' after retries.")
             failed_keywords.append(keyword)

        # Add a delay between keywords
        if i < total_keywords - 1:
             print(f"  Waiting {args.request_delay:.1f} second(s) before next keyword...")
             time.sleep(args.request_delay)

    print(f"\nSearch complete for set '{args.keyword_set}'.")
    print(f"Results saved to: {output_file}")
    print(f"Successfully processed keywords: {successful_keywords}/{total_keywords}")
    if failed_keywords:
        print(f"Failed keywords ({len(failed_keywords)}):")
        for fk in failed_keywords:
            print(f"  - {fk}")

if __name__ == "__main__":
    main() 