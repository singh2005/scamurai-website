import os
import re
import glob
import unicodedata
from ftc_article_scraper import extract_ftc_article_text
from ic3_article_scraper import extract_ic3_article_text
from rss_link_fetcher import fetch_rss_links
from blog_post_generator import create_blog_post
from pubdate_parser import parse_pubdate


POSTS_DIR = "content/posts"
os.makedirs(POSTS_DIR, exist_ok=True)

def is_posted(scam_url: str):
    search_line = f"Original article: {scam_url}"
    for filename in glob.glob("content/posts/*.md"):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip() == search_line:
                    print(f"{scam_url} Found in {filename}")
                    return True
    return False

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

    for scam_title, scam_url, scam_pubdate in scams:
        if is_posted(scam_url):
            print("Already posted!")
            continue

        scam_id = slugify(scam_title)
        blog_path = os.path.join(POSTS_DIR, f"{scam_id}.md")

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
            print(f"❌ Error processing toot {scam_id}: {e}")


if __name__ == "__main__":
    main()
