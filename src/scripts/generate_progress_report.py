#!/usr/bin/env python3
"""
Thesis Progress Visualization Tool
---------------------------------
This script generates a visual representation of thesis progress based on the
progress_tracker.md file, displaying chapters in chronological order.
"""

import re
import os
import sys
from datetime import datetime
from collections import OrderedDict

# ANSI colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def find_root_directory():
    """Find the thesis root directory."""
    # Start with the directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate up to the root (where the progress_tracker.md file is)
    root_dir = os.path.dirname(os.path.dirname(current_dir))
    
    return root_dir

def get_chapter_order(root_dir):
    """Extract chapter order from main.tex."""
    try:
        main_tex_path = os.path.join(root_dir, 'main.tex')
        with open(main_tex_path, 'r') as file:
            content = file.read()
        
        # Find all chapter includes
        chapter_pattern = r'\\input\{src/chapters/([^}]+)\}'
        chapters = re.findall(chapter_pattern, content)
        
        # Create a mapping of chapter filename to order and a normalized version
        chapter_order = {}
        for i, chapter in enumerate(chapters):
            # Remove .tex if it's there
            chapter_base = chapter.replace('.tex', '')
            
            # Create various forms for matching
            clean_name = chapter_base.replace('_', ' ').title()
            chapter_order[clean_name] = i
            
            # Also add the original format
            chapter_order[chapter_base.replace('_', ' ')] = i
            
            # Add lowercase version
            chapter_order[clean_name.lower()] = i
            
            # Add the version with underscores
            chapter_order[chapter_base] = i
        
        return chapter_order
    except Exception as e:
        print(f"Warning: Could not determine chapter order from main.tex: {e}")
        return {}

def parse_progress_tracker(file_path):
    """Parse the progress tracker markdown file."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            
        # Extract chapters progress table
        progress_table_pattern = r'\| Chapter\s+\| Status\s+\| Completion %\s+\| Last Updated\s+\| Notes\s+\|(.*?)\| \*\*Overall Completion\*\*\s+\|\s+\| \*\*(\d+)%\*\*\s+\|'
        match = re.search(progress_table_pattern, content, re.DOTALL)
        
        if not match:
            raise Exception("Could not find progress table in the markdown file")
        
        table_content = match.group(1)
        overall_completion = match.group(2)
        
        # Parse chapter rows
        chapters = []
        for line in table_content.strip().split('\n'):
            if '|' in line:
                parts = [part.strip() for part in line.split('|')]
                if len(parts) >= 6 and parts[1] and parts[3]:  # Ensure it's a valid data row
                    chapter = {
                        'name': parts[1],
                        'status': parts[2],
                        'completion': parts[3].replace('%', ''),
                        'last_updated': parts[4],
                        'notes': parts[5]
                    }
                    chapters.append(chapter)
        
        # Extract detailed chapter tracking
        detailed_chapters = {}
        chapter_pattern = r'### Chapter \d+: (.*?)\n\n\| Section.*?\|(.*?)(?=### Chapter \d+:|$)'
        for match in re.finditer(chapter_pattern, content, re.DOTALL):
            chapter_name = match.group(1).strip()
            sections_table = match.group(2).strip()
            
            sections = []
            for line in sections_table.split('\n'):
                if '|' in line:
                    parts = [part.strip() for part in line.split('|')]
                    if len(parts) >= 5 and parts[1]:  # Ensure it's a valid section row
                        section = {
                            'name': parts[1],
                            'status': parts[2],
                            'sources': parts[3],
                            'notes': parts[4]
                        }
                        sections.append(section)
            
            if sections:
                detailed_chapters[chapter_name] = sections
        
        return {
            'chapters': chapters,
            'overall_completion': overall_completion,
            'detailed_chapters': detailed_chapters
        }
    
    except Exception as e:
        print(f"Error parsing progress tracker: {e}")
        sys.exit(1)

def generate_progress_bar(percentage, width=30):
    """Generate a visual progress bar."""
    try:
        percentage = int(percentage)
    except ValueError:
        percentage = 0
    
    filled_width = int(width * percentage / 100)
    empty_width = width - filled_width
    
    # Choose color based on percentage
    if percentage >= 80:
        color = Colors.GREEN
    elif percentage >= 50:
        color = Colors.BLUE
    elif percentage >= 25:
        color = Colors.YELLOW
    else:
        color = Colors.RED
    
    # Unicode block characters for better-looking bars
    bar = color + '█' * filled_width + '░' * empty_width + Colors.ENDC
    return f"[{bar}] {percentage}%"

def get_status_color(status):
    """Return a colored representation of the status."""
    status = status.lower()
    if "completed" in status:
        return Colors.GREEN + status + Colors.ENDC
    elif "in progress" in status:
        return Colors.BLUE + status + Colors.ENDC
    elif "planned" in status:
        return Colors.YELLOW + status + Colors.ENDC
    else:
        return Colors.RED + status + Colors.ENDC

def print_visual_report(progress_data, chapter_order):
    """Print a visual report of thesis progress in chronological order."""
    chapters = progress_data['chapters']
    overall_completion = progress_data['overall_completion']
    detailed_chapters = progress_data['detailed_chapters']
    
    # Map chapter names to their correct order
    # First, create a mapping from names in progress_tracker.md to names in main.tex
    name_mapping = {
        'Introduction': 'introduction',
        'Fundamentals': 'fundamentals',
        'Classical vs Quantum': 'classical_vs_quantum',
        'Classical Crypto': 'classical_crypto',
        'Quantum Impact': 'quantum_impact',
        'Quantum Resistant': 'quantum_resistant',
        'Challenges': 'challenges',
        'Future Prospects': 'future_prospects',
        'Societal Implications': 'societal_implications'
    }
    
    # Order chapters according to the order in main.tex
    chapter_with_order = []
    
    for chapter in chapters:
        chapter_name = chapter['name']
        order = None
        
        # Skip empty rows
        if chapter_name.strip() == '----' or chapter_name.startswith('---'):
            continue
            
        # Try different variations of the name for matching
        if chapter_name in chapter_order:
            order = chapter_order[chapter_name]
        # Try using the mapping
        elif chapter_name in name_mapping and name_mapping[chapter_name] in chapter_order:
            order = chapter_order[name_mapping[chapter_name]]
        # Try lowercase
        elif chapter_name.lower() in chapter_order:
            order = chapter_order[chapter_name.lower()]
        # Try with spaces replaced by underscores
        elif chapter_name.lower().replace(' ', '_') in chapter_order:
            order = chapter_order[chapter_name.lower().replace(' ', '_')]
        
        if order is not None:
            chapter_with_order.append((order, chapter))
        else:
            # If we can't determine order, put at the end
            chapter_with_order.append((999, chapter))
    
    # Sort by order and extract just the chapter data
    chapter_with_order.sort(key=lambda x: x[0])
    ordered_chapters = [chapter for _, chapter in chapter_with_order]
    
    # Print header
    print(f"\n{Colors.HEADER}{Colors.BOLD}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print(f"┃                             THESIS PROGRESS VISUALIZATION                               ┃")
    print(f"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}OVERALL THESIS COMPLETION: {generate_progress_bar(overall_completion)}{Colors.ENDC}")
    print(f"\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Print summary statistics for better oversight
    completed_count = sum(1 for c in ordered_chapters if c['status'].lower() == 'completed')
    in_progress_count = sum(1 for c in ordered_chapters if 'in progress' in c['status'].lower())
    planned_count = sum(1 for c in ordered_chapters if 'planned' in c['status'].lower())
    total_chapters = len(ordered_chapters)
    
    print(f"\n{Colors.BOLD}SUMMARY:")
    print(f"  Completed chapters: {Colors.GREEN}{completed_count}/{total_chapters}{Colors.ENDC}")
    print(f"  In progress: {Colors.BLUE}{in_progress_count}/{total_chapters}{Colors.ENDC}")
    print(f"  Planned: {Colors.YELLOW}{planned_count}/{total_chapters}{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print(f"┃ CHRONOLOGICAL CHAPTER PROGRESS                                                        ┃")
    print(f"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{Colors.ENDC}")
    
    # Print chapter progress in order
    for i, chapter in enumerate(ordered_chapters):
        name = chapter['name']
        status = get_status_color(chapter['status'])
        progress_bar = generate_progress_bar(chapter['completion'])
        last_updated = chapter['last_updated']
        
        print(f"\n{Colors.BOLD}Chapter {i+1}: {name}{Colors.ENDC}")
        print(f"  Status: {status}")
        print(f"  Progress: {progress_bar}")
        print(f"  Last Updated: {last_updated}")
        if chapter['notes']:
            print(f"  Notes: {chapter['notes']}")
    
    # Sort detailed chapters
    ordered_detailed = OrderedDict()
    
    # Create mapping from standard names to detailed chapter names
    detailed_name_mapping = {}
    for detailed_name in detailed_chapters.keys():
        for standard_name in name_mapping.keys():
            if standard_name.lower() in detailed_name.lower() or name_mapping[standard_name].replace('_', ' ') in detailed_name.lower():
                detailed_name_mapping[standard_name] = detailed_name
    
    # Add chapters in order
    for chapter in ordered_chapters:
        chapter_name = chapter['name']
        
        # Try to find the detailed chapter
        if chapter_name in detailed_chapters:
            ordered_detailed[chapter_name] = detailed_chapters[chapter_name]
        elif chapter_name in detailed_name_mapping and detailed_name_mapping[chapter_name] in detailed_chapters:
            ordered_detailed[chapter_name] = detailed_chapters[detailed_name_mapping[chapter_name]]
    
    # Add any remaining detailed chapters
    for chapter_name, sections in detailed_chapters.items():
        added = False
        for ordered_name in ordered_detailed.keys():
            if ordered_name.lower() in chapter_name.lower() or chapter_name.lower() in ordered_name.lower():
                added = True
                break
        
        if not added:
            ordered_detailed[chapter_name] = sections
    
    # Detailed section progress if available
    if ordered_detailed:
        print(f"\n{Colors.BOLD}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print(f"┃ DETAILED SECTION PROGRESS (CHRONOLOGICAL)                                          ┃")
        print(f"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{Colors.ENDC}")
        
        for i, (chapter_name, sections) in enumerate(ordered_detailed.items()):
            # Filter out any invalid sections
            valid_sections = [s for s in sections if 'name' in s and 'status' in s]
            
            if not valid_sections:
                continue
                
            total_sections = len(valid_sections)
            completed_sections = sum(1 for s in valid_sections if s['status'].lower() == 'completed')
            chapter_percent = int(completed_sections / total_sections * 100) if total_sections > 0 else 0
            
            print(f"\n{Colors.BOLD}Chapter {i+1}: {chapter_name} ({completed_sections}/{total_sections} sections completed - {chapter_percent}%){Colors.ENDC}")
            print(f"  Progress: {generate_progress_bar(chapter_percent)}")
            
            for section in valid_sections:
                name = section['name']
                status = get_status_color(section['status'])
                print(f"  • {name}: {status}")
                if section.get('notes') and section['notes'] != 'None':
                    print(f"    - {section['notes']}")

def main():
    """Main function to generate and display the progress report."""
    root_dir = find_root_directory()
    progress_file = os.path.join(root_dir, 'progress_tracker.md')
    
    if not os.path.exists(progress_file):
        print(f"Error: Progress tracker file not found at {progress_file}")
        sys.exit(1)
    
    # Get the correct chapter order from main.tex
    chapter_order = get_chapter_order(root_dir)
    
    progress_data = parse_progress_tracker(progress_file)
    print_visual_report(progress_data, chapter_order)

if __name__ == "__main__":
    main()