#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import argparse
import json
import sys
from urllib.parse import urlparse
from datetime import datetime

def scrape_metadata(url):
    """Attempts to scrape basic metadata (title, author, date, site) from a URL."""
    metadata = {
        "url": url,
        "title": None,
        "author": None,
        "date": None, # Publication date
        "site_name": None,
        "snippet": None,
        "access_date": datetime.now().strftime('%Y-%m-%d'),
        "error": None
    }

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=20, allow_redirects=True)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        # Check if content is likely HTML
        content_type = response.headers.get('Content-Type', '').lower()
        if 'html' not in content_type:
            metadata['error'] = f"Non-HTML content type: {content_type}"
            return metadata

        soup = BeautifulSoup(response.content, 'html.parser')

        # --- Extract Title ---
        if soup.title and soup.title.string:
            metadata['title'] = soup.title.string.strip()
        else:
            # Fallback: Try Open Graph title
            og_title = soup.find('meta', property='og:title')
            if og_title and og_title.get('content'):
                metadata['title'] = og_title['content'].strip()
            else:
                 # Fallback: Try first H1
                 h1 = soup.find('h1')
                 if h1:
                     metadata['title'] = h1.get_text().strip()

        # --- Extract Author ---
        # This is highly heuristic and unreliable
        author_tag = soup.find('meta', attrs={'name': 'author'}) # Standard meta tag
        if author_tag and author_tag.get('content'):
            metadata['author'] = author_tag['content'].strip()
        else:
            # Try Open Graph article author
            og_author = soup.find('meta', property='article:author')
            if og_author and og_author.get('content'):
                metadata['author'] = og_author['content'].strip()
            else:
                 # Look for common class names (very site-specific)
                 author_element = soup.find(class_=['author', 'byline', 'writer', 'article-author'])
                 if author_element:
                     # Try to get text, potentially cleaning up links within it
                     author_text = author_element.get_text(separator=' ', strip=True)
                     # Basic cleanup for common prefixes like "By "
                     if author_text.lower().startswith('by '):
                         author_text = author_text[3:]
                     metadata['author'] = author_text
                 else:
                    # Check for schema.org/JSON-LD (simple check for author property)
                    try:
                        json_ld_scripts = soup.find_all('script', type='application/ld+json')
                        for script in json_ld_scripts:
                            data = json.loads(script.string)
                            # Check common structures
                            if isinstance(data, list):
                                data = data[0] # Assume first item is main entity
                            if isinstance(data, dict):
                                author_info = data.get('author')
                                if isinstance(author_info, dict) and author_info.get('name'):
                                    metadata['author'] = author_info['name'].strip()
                                    break
                                elif isinstance(author_info, list) and len(author_info) > 0 and isinstance(author_info[0], dict) and author_info[0].get('name'):
                                    metadata['author'] = author_info[0]['name'].strip() # Take first author
                                    break
                    except (json.JSONDecodeError, TypeError, AttributeError):
                        pass # Ignore errors in parsing JSON-LD

        # --- Extract Date ---
        # Also heuristic
        date_tag = soup.find('meta', property='article:published_time')
        if date_tag and date_tag.get('content'):
            metadata['date'] = date_tag['content'].strip().split('T')[0] # Get YYYY-MM-DD part
        else:
            time_tag = soup.find('time', datetime=True)
            if time_tag and time_tag.get('datetime'):
                 metadata['date'] = time_tag['datetime'].strip().split('T')[0]
            else:
                # Look for common class names (site-specific)
                date_element = soup.find(class_=['date', 'published', 'post-date', 'timestamp'])
                if date_element:
                    # Attempt to extract text, might need further parsing
                    metadata['date'] = date_element.get_text(strip=True)
                    # Basic check if it looks like a date - rudimentary!
                    if not any(c.isdigit() for c in metadata['date']):
                        metadata['date'] = None # Discard if no digits

        # --- Extract Site Name ---
        og_site = soup.find('meta', property='og:site_name')
        if og_site and og_site.get('content'):
            metadata['site_name'] = og_site['content'].strip()
        else:
            # Fallback to domain name
            parsed_url = urlparse(url)
            if parsed_url.netloc:
                # Remove www. if present
                metadata['site_name'] = parsed_url.netloc.replace('www.', '')

        # --- Extract Snippet ---
        # Try first paragraph
        first_p = soup.find('p')
        if first_p:
            metadata['snippet'] = first_p.get_text(strip=True)[:300] # Limit length
        elif soup.body: # Fallback to start of body text
             body_text = soup.body.get_text(separator=' ', strip=True)
             metadata['snippet'] = body_text[:300]

    except requests.exceptions.HTTPError as http_err:
        metadata['error'] = f"HTTP error: {http_err}"
    except requests.exceptions.RequestException as req_err:
        metadata['error'] = f"Request error: {req_err}"
    except Exception as e:
        metadata['error'] = f"An unexpected error occurred during scraping: {e}"

    # Clean up None values before returning
    cleaned_metadata = {k: v for k, v in metadata.items() if v is not None}
    return cleaned_metadata

def main():
    parser = argparse.ArgumentParser(description='Scrape basic metadata (title, author, date) from a URL.')
    parser.add_argument('--url', required=True, help='The URL to scrape.')

    args = parser.parse_args()

    scraped_data = scrape_metadata(args.url)

    # Print the result as JSON to stdout
    print(json.dumps(scraped_data, indent=2))

    if scraped_data.get("error"):
        sys.exit(1) # Indicate failure
    else:
        sys.exit(0) # Indicate success

if __name__ == "__main__":
    main() 