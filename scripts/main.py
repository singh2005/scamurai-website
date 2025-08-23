import os
import re
import unicodedata
from ftc_article_scraper import extract_ftc_article_text
from ic3_article_scraper import extract_ic3_article_text
from rss_link_fetcher import fetch_rss_links
from blog_post_generator import create_blog_post
from pubdate_parser import parse_pubdate


POSTS_DIR = "content/posts"
os.makedirs(POSTS_DIR, exist_ok=True)

def slugify(text: str):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

def main():
    ftc_scams = fetch_rss_links("https://consumer.ftc.gov/blog/gd-rss.xml")
    ic3_scams = fetch_rss_links("https://www.ic3.gov/PSA/RSS")
    scams = ftc_scams + ic3_scams

    for scam in scams[]:
        scam_title = scam[0]
        scam_url = scam[1]
        scam_pubdate = scam[2]
        scam_id = slugify(scam_title)
        blog_path = os.path.join(POSTS_DIR, f"{scam_id}.md")

        if os.path.exists(blog_path):
            print(f"✅ Skipping blog: {scam_id} (already exists)")
            continue

        scam_date = parse_pubdate(scam_pubdate)

        try:
            if "consumer.ftc.gov" in scam_url:
                article_text = extract_ftc_article_text(scam_url)
            elif "ic3.gov" in scam_url:
                article_text = extract_ic3_article_text(scam_url)
            else:
                print(f"⚠️  Skipping blog {scam_id} (unsupported domain): {scam_url}")
                continue

            blog_post = create_blog_post(scam_id, article_text, scam_url, scam_date)
            with open(blog_path, "w", encoding="utf-8") as f:
                f.write(blog_post)

            print(f"✅ Blog post saved: {blog_path}")

        except Exception as e:
            print(f"❌ Error processing toot {toot_id}: {e}")


if __name__ == "__main__":
    main()
