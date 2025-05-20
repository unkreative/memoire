#!/usr/bin/env python3
import requests
import time
import json
import os
import argparse

# === Keyword Dictionary ===
# Using the expanded keywords generated previously
EXPANDED_KEYWORDS_ALL_CHAPTERS = {
    "ch1_introduction": [
        "Quantum Computing Introduction", "Quantum Computing Impact Cryptography", "Quantum Computing Vulnerabilities Cryptography",
        "Quantum-Resistant Cryptography Introduction", "Quantum Computing vs Classical Computing Cryptography",
        "Shor's Algorithm Impact Public Key Cryptography", "Grover's Algorithm Impact Symmetric Key Cryptography",
        "Post-Quantum Cryptography PQC Transition Introduction", "Quantum Key Distribution QKD Overview",
        "Quantum Computing Paradigm Shift", "Store Now Decrypt Later SNDL Introduction",
    ],
    "ch2_fundamentals": [
        "Quantum Mechanics Principles", "Superposition in Quantum Computing", "Quantum Entanglement",
        "Qubit Definition and Properties", "Bloch Sphere Representation", "Physical Implementations of Qubits Superconducting",
        "Physical Implementations of Qubits Trapped Ion", "Physical Implementations of Qubits Photonic", "Quantum Coherence",
        "Quantum Decoherence", "Quantum Gates Pauli", "Quantum Gates Hadamard", "Quantum Gates CNOT", "Quantum Gates Toffoli",
        "Unitary Transformations Quantum Computing", "Quantum Circuits Design", "Bell State Generation",
        "Quantum Fourier Transform QFT", "Quantum Phase Estimation QPE", "Amplitude Amplification Quantum",
        "Grover's Search Algorithm", "Shor's Algorithm Factoring", "Shor's Algorithm Discrete Logarithm", "Quantum Cryptanalysis",
        "Quantum Impact RSA", "Quantum Impact Diffie-Hellman", "Quantum Impact Elliptic Curve Cryptography ECC",
        "Grover Algorithm Impact AES", "Grover Algorithm Impact Hash Functions", "Noisy Intermediate-Scale Quantum NISQ",
        "Quantum Error Correction QEC", "Fault-Tolerant Quantum Computing", "Quantum Advantage",
    ],
    "ch3_classical_crypto": [
        "History of Cryptography Ancient", "History of Cryptography Classical", "History of Cryptography Mechanical",
        "History of Cryptography Modern", "Caesar Cipher", "Vigenere Cipher", "Enigma Machine Cryptanalysis",
        "Shannon Information Theory Cryptography", "Kerckhoffs Principle", "Cryptographic Security Goals Confidentiality",
        "Cryptographic Security Goals Integrity", "Cryptographic Security Goals Authentication", "Cryptographic Security Goals Non-repudiation",
        "Computational Hardness Assumptions Cryptography", "One-way Functions Cryptography", "Trapdoor Functions Cryptography",
        "Symmetric Key Cryptography", "Secret Key Distribution Problem", "Substitution-Permutation Network SPN",
        "S-box Substitution Box", "Confusion and Diffusion Cryptography", "Key Scheduling Algorithm",
        "Side-Channel Attack Timing", "Side-Channel Attack Power Analysis", "Block Cipher AES",
        "Block Cipher Modes of Operation ECB CBC GCM", "Grover Algorithm Impact Symmetric Keys",
        "Public Key Cryptography Asymmetric", "RSA Algorithm Key Generation", "RSA Algorithm Encryption Decryption",
        "Integer Factorization Problem IFP", "Euler Totient Function", "RSA Quantum Threat Shor Algorithm",
        "RSA Implementation Attack Padding Oracle Bleichenbacher", "Elliptic Curve Cryptography ECC",
        "Elliptic Curve Discrete Logarithm Problem ECDLP", "ECC Key Size Advantage", "Elliptic Curve Point Addition Scalar Multiplication",
        "ECC Quantum Threat Shor Algorithm", "Diffie-Hellman Key Exchange DH", "Discrete Logarithm Problem DLP",
        "Man-in-the-Middle Attack MitM Cryptography", "Cryptographic Hash Functions", "Hash Function Properties Pre-image Resistance",
        "Hash Function Properties Second Pre-image Resistance", "Hash Function Properties Collision Resistance",
        "MD5 SHA-1 Collision Attack", "SHA-2 Hash Family", "SHA-3 Hash Family Keccak", "Merkle-Damgard Construction",
        "Sponge Construction Cryptography", "Hash Function Quantum Impact Grover Birthday Attack",
        "Digital Signatures Authentication Integrity Non-repudiation", "Public Key Infrastructure PKI",
        "Certificate Authority CA PKI", "Digital Certificates X.509", "Certificate Revocation List CRL OCSP",
        "Digital Signature Quantum Threat Shor Algorithm", "Cryptographic Protocol Design Security",
        "Cryptographic Implementation Vulnerabilities",
    ],
    "ch4_classical_vs_quantum": [
        "Classical vs Quantum Computing Comparison", "Bit vs Qubit Information Representation", "Quantum Superposition Principle",
        "Quantum Entanglement Resource", "No-Cloning Theorem Implications", "Classical Computation Model Turing Machine",
        "Classical Computation Model Von Neumann", "Quantum Computation Model Quantum Circuit", "Unitary Transformations Quantum Computing",
        "Hilbert Space Representation Quantum State", "Quantum Parallelism Concept", "Quantum Interference Role",
        "Computational Complexity Theory", "Complexity Class P Polynomial Time", "Complexity Class NP Nondeterministic Polynomial",
        "Complexity Class BPP Bounded-error Probabilistic Polynomial", "Complexity Class BQP Bounded-error Quantum Polynomial",
        "Relationship P BPP BQP NP Complexity Classes", "Shor Algorithm Complexity Impact Factoring DLP",
        "Grover Algorithm Complexity Impact Search",
    ],
    "ch5_quantum_impact": [
        "Quantum Impact on Cryptography Review", "Shor's Algorithm Cryptographic Impact",
        "Shor's Algorithm Integer Factorization Impact", "Shor's Algorithm Integer Factorization Mechanism QFT QPE",
        "Shor's Algorithm Discrete Logarithm Impact", "Shor's Algorithm Discrete Logarithm Mechanism",
        "Quantum Threat to RSA", "Quantum Threat RSA Cryptanalysis", "Quantum Threat to Diffie-Hellman DH DSA",
        "Quantum Threat Diffie-Hellman DSA Cryptanalysis", "Quantum Threat to Elliptic Curve Cryptography ECC ECDH ECDSA",
        "Classical vs Quantum Factoring Complexity", "Cryptographically Relevant Quantum Computer CRQC",
        "Shor Algorithm Resource Estimation CRQC", "Quantum Threat to TLS HTTPS SSH", "Quantum Threat TLS SSH PKI",
        "Quantum Threat to Public Key Infrastructure PKI", "Grover's Algorithm Cryptographic Impact",
        "Grover's Algorithm Cryptographic Impact Review", "Quantum Amplitude Amplification Mechanism",
        "Grover's Algorithm Impact Symmetric Key Search", "Grover's Algorithm Symmetric Key Search Complexity",
        "Quantum Impact on AES Security Levels", "Quantum Attack AES Security Level Reduction",
        "Grover's Algorithm Impact Hash Pre-image Resistance", "Grover's Algorithm Impact Hash Collision Resistance",
        "Quantum vs Classical Birthday Attack Collision Finding", "Quantum Security Levels Adjustment",
        "NIST Security Levels Post-Quantum", "Quantum Security Level Definition NIST",
        "Security Adjustments Symmetric Keys Quantum Attack", "Security Adjustments Hash Functions Quantum Attack",
        "AES-128 vs AES-256 Quantum Security", "SHA-256 Quantum Security Collision Preimage",
        "Post-Quantum Cryptography PQC Necessity", "PQC Necessity Threat Analysis",
        "Classical vs Quantum Security Comparison", "Quantum Computing Timeline Estimates",
        "Quantum Computing Timeline CRQC Development", "Quantum Error Correction QEC Requirement",
        "Fault-Tolerant Quantum Computing Challenges QEC", "NISQ Era vs Fault-Tolerant Quantum Computing",
        "Store Now Decrypt Later SNDL Threat", "Mosca's Inequality X+Y > Z", "Mosca's Inequality Cryptographic Migration",
        "Security Shelf Life Cryptography", "Security Shelf Life Data Encryption", "Cryptographic Migration Time",
        "Post-Quantum Cryptography Migration Urgency", "Peter Shor 1994 Algorithms Paper",
        "Grover 1996 Fast Quantum Mechanical Algorithm Paper", "Nielsen Chuang Quantum Computation Book",
        "Bernstein 2017 Post-Quantum Cryptography Report", "Gidney 2021 Factor RSA-2048 Quantum Resources",
        "Mosca 2018 Cybersecurity Quantum Era", "Preskill 2018 Quantum Computing NISQ Fault-Tolerant",
        "NIST PQC Status Report IR 8413", "NIST PQC Timeline", "Quantum Resource Requirements Cryptanalysis",
        "Quantum Mitigation Framework",
    ],
    "ch6_quantum_resistant": [
        "Post-Quantum Cryptography PQC", "Quantum-Resistant Cryptography", "Lattice-Based Cryptography",
        "Mathematical Lattices Definition", "Shortest Vector Problem SVP", "Closest Vector Problem CVP",
        "Learning With Errors LWE Problem", "Quantum Resistance LWE", "Ring-LWE RLWE", "Module-LWE MLWE",
        "Lattice Cryptography Efficiency", "Lattice Cryptography Key Size", "CRYSTALS-Kyber KEM",
        "CRYSTALS-Dilithium Signature", "Falcon Signature", "NTRU Lattice Problem", "Hash-Based Cryptography Signatures",
        "One-Time Signatures OTS Lamport", "Merkle Tree Signatures", "Stateful Hash-Based Signatures XMSS LMS",
        "Stateless Hash-Based Signatures SPHINCS+", "Code-Based Cryptography", "McEliece Cryptosystem",
        "Goppa Codes Cryptography", "Niederreiter Cryptosystem", "Code-Based Cryptography Key Size",
        "Classic McEliece KEM", "Multivariate Cryptography", "Multivariate Polynomial Equations MQ Problem",
        "Multivariate Signatures", "Isogeny-Based Cryptography", "NIST PQC Standardization Process",
        "NIST PQC Finalists Candidates", "PQC Implementation Considerations", "PQC Performance Trade-offs",
        "PQC Side-Channel Attacks", "PQC Integration Complexity", "Hybrid Cryptography PQC Classical",
        "Hybrid Key Exchange", "Hybrid Signatures",
    ],
    "ch7_challenges": [
        "Post-Quantum Cryptography PQC Transition Challenges", "PQC Performance Overhead Speed Size",
        "PQC Computational Speed Comparison", "PQC Key Size Signature Size Impact", "PQC Ciphertext Size Impact",
        "PQC Implementation Challenges", "PQC System Integration Complexity", "PQC Legacy System Compatibility",
        "PQC Protocol Modifications TLS SSH", "PQC Hardware Constraints IoT Smart Cards",
        "PQC Software Ecosystem Updates Libraries OS", "PQC Infrastructure Updates KMS HSM PKI",
        "PQC Certificate Size Validation", "PQC Implementation Security", "PQC Side-Channel Attack Vulnerabilities",
        "PQC Constant-Time Implementation", "PQC Algorithmic Complexity Bugs", "PQC Development Tooling Testing",
        "PQC Migration Strategy Challenges", "Cryptographic Agility", "PQC Hybrid Mode Deployment Classical PQC",
        "PQC Backward Compatibility Interoperability", "PQC Downgrade Attacks", "Crypto-Inventory Dependency Analysis",
        "PQC Migration Prioritization", "PQC Resource Constraints Hardware Software", "PQC Memory Usage RAM Cache",
        "PQC Processing Power Requirements", "PQC Bandwidth Consumption", "PQC Expertise Personnel Shortage",
        "PQC Training Needs", "PQC Vendor Support", "PQC Security Confidence Risk Management",
        "Trust in New PQC Algorithms", "PQC Mathematical Assumptions Hardness", "PQC Parameter Selection Security",
        "PQC Standardization Challenges", "NIST PQC Process Timeline Status",
        "International PQC Standards Harmonization ISO ETSI IETF", "PQC Conformance Testing Validation",
        "PQC Cost Economic Impact", "PQC Direct Costs Hardware Software Testing", "PQC Indirect Costs Training Operations",
    ],
    "ch8_conclusion": [
        "Quantum Computing Cryptography Thesis Summary", "Quantum Threat Summary Shor Grover",
        "Post-Quantum Cryptography PQC Solutions Review", "PQC Algorithm Families Comparison Lattice Hash Code Multivariate Isogeny",
        "PQC Transition Challenges Summary", "PQC Migration Planning Importance", "Hybrid Cryptography Role Conclusion",
        "PQC Societal Implications", "PQC Economic Impact Costs", "PQC Privacy Implications SNDL",
        "PQC National Security Geopolitics", "Future Research PQC Algorithm Refinement",
        "Future Research PQC Implementation Security", "Future Research PQC Standardization Interoperability",
        "Future Research Hybrid Systems PQC", "Quantum Hardware Progress Monitoring",
        "Quantum Key Distribution QKD Future Prospects", "Cryptographic Agility Importance Conclusion",
        "Post-Quantum Future Preparedness",
    ]
}

# === Configuration ===
DEFAULT_OUTPUT_DIR = "web_search_results"
TAVILY_API_URL = "https://api.tavily.com/search"
LIMIT = 5 # Number of results per keyword
SEARCH_DEPTH = "basic" # Or "advanced" for more in-depth results (consumes more credits)
MAX_RETRIES = 3
INITIAL_BACKOFF = 2  # Initial wait time in seconds for rate limiting
REQUEST_DELAY = 2.0  # Delay between different keyword searches in seconds
TIMEOUT = 45 # Request timeout in seconds

# === Helper Functions ===

def get_tavily_api_key():
    """Gets the Tavily API key from environment variables."""
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        print("Error: TAVILY_API_KEY environment variable not set.")
        print("Please set the variable, e.g., export TAVILY_API_KEY='your_key'")
        return None
    return api_key

def search_tavily(api_key, keyword, limit, search_depth, max_retries, initial_backoff, timeout):
    """Searches Tavily API for a keyword with retry logic."""
    payload = json.dumps({
        "api_key": api_key,
        "query": keyword,
        "search_depth": search_depth,
        "include_answer": False, # We primarily want the sources/links
        "include_images": False,
        "include_raw_content": False, # Set to True if you want page content (more credits)
        "max_results": limit,
        # "include_domains": ["example.com"], # Optional: Filter by specific domains
        # "exclude_domains": ["wikipedia.org"] # Optional: Exclude domains
    })
    headers = {'Content-Type': 'application/json'}

    retries = 0
    backoff_time = initial_backoff

    while retries < max_retries:
        try:
            print(f"    Attempting request for '{keyword}' (try {retries + 1}/{max_retries})...", flush=True)
            response = requests.post(TAVILY_API_URL, headers=headers, data=payload, timeout=timeout)

            if response.status_code == 200:
                print(f"    Success for '{keyword}'.")
                try:
                    return response.json()
                except json.JSONDecodeError:
                    print(f"    Error: Could not decode JSON response for '{keyword}'. Status: {response.status_code}, Text: {response.text}")
                    return None # Indicate JSON decode failure
            elif response.status_code == 429: # Rate limited
                wait_time = backoff_time + (time.time() % 1) # Add jitter
                print(f"    Received 429 (Rate Limit) for '{keyword}'. Waiting {wait_time:.2f} seconds...")
                time.sleep(wait_time)
                backoff_time = min(backoff_time * 2, 60) # Exponential backoff, capped
                retries += 1
            elif response.status_code == 400: # Bad request (e.g., invalid API key)
                 print(f"    Error: Received 400 (Bad Request) for '{keyword}'. Check API key or query. Response: {response.text}")
                 return None # Indicate fatal error
            elif response.status_code == 401: # Unauthorized
                 print(f"    Error: Received 401 (Unauthorized) for '{keyword}'. Check API key. Response: {response.text}")
                 return None # Indicate fatal error
            else:
                print(f"    Error: Received status code {response.status_code} for '{keyword}'. Response: {response.text}")
                # Potentially retry for 5xx errors
                if 500 <= response.status_code < 600 and retries < max_retries -1 :
                     print(f"    Retrying after server error...")
                     time.sleep(backoff_time)
                     backoff_time = min(backoff_time * 2, 60)
                     retries += 1
                else:
                    return None # Indicate other non-retryable error or max retries on 5xx

        except requests.exceptions.RequestException as e:
            print(f"    Error: Request failed for '{keyword}': {e}")
            retries += 1
            if retries < max_retries:
                 print(f"    Retrying after request error...")
                 time.sleep(backoff_time) # Wait before retrying on network errors too
                 backoff_time = min(backoff_time * 2, 60)
            else:
                 print(f"    Max retries reached after request error for '{keyword}'.")
                 return None # Indicate request exception after retries

    print(f"    Error: Max retries reached for '{keyword}' after rate limiting or errors. Giving up.")
    return None # Indicate max retries exceeded

# === Main Execution ===

def main():
    parser = argparse.ArgumentParser(description="Search Tavily for web sources based on thesis keywords.")
    parser.add_argument(
        'chapters',
        nargs='*', # 0 or more arguments
        choices=list(EXPANDED_KEYWORDS_ALL_CHAPTERS.keys()) + ['all'],
        default=['all'],
        help=f"Which chapter keyword sets to use (e.g., ch1 ch5 ch6). Use 'all' to search all chapters. (default: all)"
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
        '--search-depth',
        choices=['basic', 'advanced'],
        default=SEARCH_DEPTH,
        help=f"Tavily search depth ('basic' or 'advanced') (default: {SEARCH_DEPTH})"
    )
    parser.add_argument(
        '--max-retries',
        type=int,
        default=MAX_RETRIES,
        help=f"Maximum retries on rate limit/server error (default: {MAX_RETRIES})"
    )
    parser.add_argument(
        '--request-delay',
        type=float,
        default=REQUEST_DELAY,
        help=f"Delay between keyword searches in seconds (default: {REQUEST_DELAY})"
    )

    args = parser.parse_args()

    api_key = get_tavily_api_key()
    if not api_key:
        return # Exit if API key is not found

    # Determine which keywords to search
    keywords_to_search_map = {}
    if 'all' in args.chapters or not args.chapters:
        keywords_to_search_map = EXPANDED_KEYWORDS_ALL_CHAPTERS
        print("Selected chapters: all")
    else:
        for ch_key in args.chapters:
            if ch_key in EXPANDED_KEYWORDS_ALL_CHAPTERS:
                keywords_to_search_map[ch_key] = EXPANDED_KEYWORDS_ALL_CHAPTERS[ch_key]
        print(f"Selected chapters: {', '.join(keywords_to_search_map.keys())}")

    if not keywords_to_search_map:
        print("Error: No valid chapters selected.")
        return

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    # Create a unique filename based on selected chapters or 'all'
    chapters_suffix = "_".join(sorted(keywords_to_search_map.keys())) if len(keywords_to_search_map) < len(EXPANDED_KEYWORDS_ALL_CHAPTERS) else "all_chapters"
    output_file = os.path.join(args.output_dir, f"web_results_{chapters_suffix}.jsonl")

    # Clear or create the output file
    with open(output_file, 'w') as f:
        pass
    print(f"Output will be saved to: {output_file}")
    print(f"Limit per keyword: {args.limit}")
    print(f"Search depth: {args.search_depth}")
    print(f"Max retries: {args.max_retries}")
    print(f"Request delay: {args.request_delay}s")

    total_keywords = sum(len(v) for v in keywords_to_search_map.values())
    processed_keywords = 0
    successful_keywords = 0
    failed_keywords = []

    print(f"Starting web search for {total_keywords} keywords...")

    for chapter_key, keywords in keywords_to_search_map.items():
        print(f"--- Processing Chapter: {chapter_key} ---")
        for i, keyword in enumerate(keywords):
            processed_keywords += 1
            print(f"[{processed_keywords}/{total_keywords}] Processing keyword: '{keyword}' (Chapter: {chapter_key})")

            result_data = search_tavily(
                api_key,
                keyword,
                args.limit,
                args.search_depth,
                args.max_retries,
                INITIAL_BACKOFF,
                TIMEOUT
            )

            if result_data and 'results' in result_data:
                num_results = len(result_data.get('results', []))
                if num_results > 0:
                    with open(output_file, 'a', encoding='utf-8') as f:
                        for result in result_data['results']:
                            # Add context to the result
                            output_record = {
                                "search_keyword": keyword,
                                "chapter": chapter_key,
                                "title": result.get("title"),
                                "url": result.get("url"),
                                "content": result.get("content"), # Snippet/summary from Tavily
                                "score": result.get("score"),
                                # "raw_content": result.get("raw_content") # Include if requested
                            }
                            json.dump(output_record, f, ensure_ascii=False)
                            f.write('\n')
                    print(f"  -> Successfully wrote {num_results} results for '{keyword}' to {output_file}")
                    successful_keywords += 1
                else:
                     print(f"  -> No web results found for '{keyword}'.")
                     successful_keywords += 1 # Count as success if API call worked but returned 0 results
            elif result_data: # Response received but no 'results' field or other issue
                 print(f"  -> Warning: No results found or unexpected format in response for '{keyword}'. Response: {result_data}")
                 failed_keywords.append(f"{chapter_key}: {keyword}")
            else:
                 print(f"  -> Error: Failed to retrieve or process data for '{keyword}' after retries.")
                 failed_keywords.append(f"{chapter_key}: {keyword}")

            # Add a delay between keywords
            if processed_keywords < total_keywords:
                 print(f"  Waiting {args.request_delay:.1f} second(s) before next keyword...")
                 time.sleep(args.request_delay)

    print(f"Web search complete.")
    print(f"Results saved to: {output_file}")
    print(f"Successfully processed keywords: {successful_keywords}/{total_keywords}")
    if failed_keywords:
        print(f"Failed keywords ({len(failed_keywords)}):")
        for fk in failed_keywords:
            print(f"  - {fk}")

if __name__ == "__main__":
    main() 