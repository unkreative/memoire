#!/usr/bin/env python3
import os
import re
from collections import Counter
import matplotlib.pyplot as plt
import textstat

def explain_readability_score(score_type, score):
    explanations = {
        'flesch_ease': {
            'description': "Flesch Reading Ease Score (0-100):",
            'interpretation': {
                90: "Very easy to read (5th grade)",
                80: "Easy to read (6th grade)",
                70: "Fairly easy to read (7th grade)",
                60: "Plain English (8th-9th grade)",
                50: "Fairly difficult (10th-12th grade)",
                30: "Difficult (College level)",
                0: "Very difficult (College graduate level)"
            }
        },
        'flesch_grade': {
            'description': "Flesch-Kincaid Grade Level:",
            'interpretation': "Indicates the US grade level required to understand the text. For academic writing, scores between 10-12 are common, while graduate-level texts often score 12+."
        },
        'smog_index': {
            'description': "SMOG Index:",
            'interpretation': "Estimates the years of education needed to understand the text. Academic papers typically score between 13-15. Scores above 16 indicate very complex academic writing."
        },
        'gunning_fog': {
            'description': "Gunning Fog Index:",
            'interpretation': "Estimates readability based on sentence length and complex words. Scores of 13-16 indicate professional academic writing. Above 17 indicates very technical content."
        }
    }

    explanation = explanations[score_type]
    result = f"{explanation['description']} {score:.1f}\n"
    
    if score_type == 'flesch_ease':
        for threshold, meaning in sorted(explanation['interpretation'].items(), reverse=True):
            if score >= threshold:
                result += f"  → {meaning}"
                break
    else:
        result += f"  → {explanation['interpretation']}"
    
    return result

def clean_latex_content(content):
    # Remove LaTeX commands and comments
    content = re.sub(r'\\[a-zA-Z]+{[^}]*}', '', content)
    content = re.sub(r'%.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'\\[a-zA-Z]+', '', content)
    return content

def analyze_text_complexity(text):
    # Basic text cleanup
    words = re.findall(r'\w+', text.lower())
    sentences = re.split(r'[.!?]+', text)
    
    if not words or not sentences:
        return None

    # Calculate statistics
    word_count = len(words)
    sentence_count = len([s for s in sentences if s.strip()])
    char_count = sum(len(word) for word in words)
    
    # Get unique words and frequency
    unique_words = set(words)
    word_freq = Counter(words).most_common(10)
    
    # Calculate averages
    avg_word_length = char_count / word_count if word_count > 0 else 0
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
    
    # Calculate readability scores
    readability_scores = {
        'flesch_ease': textstat.flesch_reading_ease(text),
        'flesch_grade': textstat.flesch_kincaid_grade(text),
        'smog_index': textstat.smog_index(text),
        'gunning_fog': textstat.gunning_fog(text)
    }
    
    return {
        'avg_word_length': avg_word_length,
        'avg_sentence_length': avg_sentence_length,
        'unique_words': len(unique_words),
        'top_words': word_freq,
        'readability': readability_scores
    }

def analyze_chapter(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            clean_content = clean_latex_content(content)
            words = re.findall(r'\w+', clean_content)
            word_count = len(words)
            complexity_stats = analyze_text_complexity(clean_content)
            return word_count, complexity_stats
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return 0, None

def generate_stats():
    chapters_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'chapters')
    stats = {}
    complexity_data = {}
    total_words = 0
    
    print("\nAnalyzing Thesis Content...")
    print("=" * 80)

    # Analyze each chapter
    for filename in sorted(os.listdir(chapters_dir)):
        if filename.endswith('.tex'):
            file_path = os.path.join(chapters_dir, filename)
            word_count, complexity = analyze_chapter(file_path)
            chapter_name = filename.replace('.tex', '').split('_', 1)[1]
            stats[chapter_name] = word_count
            complexity_data[chapter_name] = complexity
            total_words += word_count

    # Calculate overall metrics
    all_scores = {
        'flesch_ease': [],
        'flesch_grade': [],
        'smog_index': [],
        'gunning_fog': []
    }
    
    for complexity in complexity_data.values():
        if complexity:
            for score_type in all_scores:
                all_scores[score_type].append(complexity['readability'][score_type])

    # Print comprehensive overview
    print("\nTHESIS OVERVIEW")
    print("=" * 80)
    print(f"Total Word Count: {total_words:,} words")
    print(f"Number of Chapters: {len(stats)} chapters")
    
    # Word distribution overview
    avg_chapter_length = total_words / len(stats) if stats else 0
    max_chapter = max(stats.items(), key=lambda x: x[1])
    min_chapter = min(stats.items(), key=lambda x: x[1])
    
    print("\nWord Distribution:")
    print("-" * 40)
    print(f"Average Chapter Length: {avg_chapter_length:.0f} words")
    print(f"Longest Chapter: '{max_chapter[0]}' ({max_chapter[1]} words)")
    print(f"Shortest Chapter: '{min_chapter[0]}' ({min_chapter[1]} words)")
    
    print("\nOverall Readability Metrics:")
    print("-" * 40)
    for score_type in all_scores:
        if all_scores[score_type]:
            avg_score = sum(all_scores[score_type]) / len(all_scores[score_type])
            print(explain_readability_score(score_type, avg_score))

    print("\nDetailed Chapter Analysis")
    print("=" * 80)
    
    for chapter, count in stats.items():
        percentage = (count / total_words) * 100
        print(f"\n{chapter.replace('_', ' ').title()}:")
        print("-" * 40)
        print(f"Word Count: {count:,} words ({percentage:.1f}% of thesis)")
        
        if complexity_data[chapter]:
            complexity = complexity_data[chapter]
            print(f"Unique Words: {complexity['unique_words']}")
            print(f"Average Word Length: {complexity['avg_word_length']:.1f} characters")
            print(f"Average Sentence Length: {complexity['avg_sentence_length']:.1f} words")
            
            print("\nReadability Scores:")
            for score_type in ['flesch_ease', 'flesch_grade', 'smog_index', 'gunning_fog']:
                score = complexity['readability'][score_type]
                print(explain_readability_score(score_type, score))
            
            print("\nMost Common Words:")
            for word, freq in complexity['top_words'][:5]:
                print(f"  - {word}: {freq} times")

    # Create visualization
    chapters = list(stats.keys())
    word_counts = list(stats.values())
    
    plt.figure(figsize=(12, 6))
    plt.bar(chapters, word_counts)
    plt.xticks(rotation=45, ha='right')
    plt.title('Word Count Distribution Across Chapters')
    plt.xlabel('Chapters')
    plt.ylabel('Word Count')
    plt.tight_layout()
    
    # Save the plot
    plot_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images', 'word_distribution.png')
    plt.savefig(plot_path)
    print(f"\nWord distribution plot saved as: {plot_path}")

if __name__ == '__main__':
    generate_stats()