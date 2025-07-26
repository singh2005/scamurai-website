import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    )
}

def extract_ic3_article_text(url: str) -> str:
    print(f"[INFO] Fetching IC3 article from: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"[ERROR] Failed to fetch page: {e}")

    soup = BeautifulSoup(response.text, 'html.parser')

    main_content = soup.find('main', id='main')
    if not main_content:
        raise Exception("[ERROR] Could not find main content")

    sections = main_content.find_all('section')
    if not sections:
        raise Exception("[ERROR] Could not find any sections in main content")

    article_text_parts = []

    for section in sections:
        # Extract heading tags h2 or h3 if available
        heading = section.find(['h2', 'h3'])
        if heading:
            article_text_parts.append(heading.get_text(strip=True))

        # Extract paragraphs and lists inside the section
        # Preserve structure by adding new lines between elements
        for elem in section.find_all(['p', 'ul', 'ol']):
            if elem.name == 'p':
                article_text_parts.append(elem.get_text(strip=True))
            elif elem.name in ['ul', 'ol']:
                # For lists, get each list item
                items = [li.get_text(strip=True) for li in elem.find_all('li')]
                article_text_parts.append('\n'.join(f"- {item}" for item in items))

        # Add a blank line between sections
        article_text_parts.append('')

    # Join all parts with double newlines
    return '\n\n'.join(article_text_parts).strip()


if __name__ == "__main__":
    test_url = "https://www.ic3.gov/PSA/2025/PSA250723-4"  
    article_text = extract_ic3_article_text(test_url)
    print("\n--- IC3 Article Content ---\n")
    print(article_text)
