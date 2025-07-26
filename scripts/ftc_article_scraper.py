import requests
from bs4 import BeautifulSoup

def extract_article_text(url: str) -> str:
    print(f"[INFO] Fetching article from: {url}")
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"[ERROR] Failed to fetch page: {e}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all divs with the target class
    body_divs = soup.find_all('div', class_='field--name-body')

    # Confirm we have enough blocks
    if len(body_divs) < 6:
        raise Exception(f"[ERROR] Expected at least 6 content blocks, found {len(body_divs)}")

    # Grab the 6th block (index 5)
    article_div = body_divs[5]
    text = article_div.get_text(separator='\n', strip=True)
    return text

if __name__ == "__main__":
    test_url = "https://consumer.ftc.gov/consumer-alerts/2025/07/scammy-texts-offering-refunds-amazon-purchases"
    article_text = extract_article_text(test_url)
    print("\n[ARTICLE CONTENT]\n")
    print(article_text)
