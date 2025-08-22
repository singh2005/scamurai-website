import requests
import xml.etree.ElementTree as ET


def fetch_rss_links(feed_url: str):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      "AppleWebKit/537.36 (KHTML, like Gecko)"
                      "Chrome/115.0.0.0 Safari/537.36"
    }

    resp = requests.get(feed_url, headers=headers)
    resp.raise_for_status()

    # Parse XML
    root = ET.fromstring(resp.content)

    # Namespace not needed for description
    items = root.findall(".//item")

    links = []

    for item in items:
        link = item.findtext("link", "").strip()
        if link:
            links.append(link)

    return links


if __name__ == "__main__":
    feed_url = "https://consumer.ftc.gov/blog/gd-rss.xml"
    links = fetch_rss_links(feed_url)

    for link in links:
        print(link)

    feed_url = "https://www.ic3.gov/PSA/RSS"
    links = fetch_rss_links(feed_url)

    for link in links:
        print(link)
        