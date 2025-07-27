import os
from mastodon_fetcher import get_recent_toots
from ftc_article_scraper import extract_ftc_article_text
from ic3_article_scraper import extract_ic3_article_text
from blog_post_generator import create_blog_post

POSTS_DIR = "content/posts"
os.makedirs(POSTS_DIR, exist_ok=True)

def main():
    toots = get_recent_toots(limit=30)

    for toot in toots:
        toot_id = str(toot["id"])
        blog_path = os.path.join(POSTS_DIR, f"{toot_id}.md")

        if os.path.exists(blog_path):
            print(f"✅ Skipping toot {toot_id} (already exists)")
            continue

        url = toot["original_url"]

        try:
            if "consumer.ftc.gov" in url:
                article_text = extract_ftc_article_text(url)
            elif "ic3.gov" in url:
                article_text = extract_ic3_article_text(url)
            else:
                print(f"⚠️  Skipping toot {toot_id} (unsupported domain): {url}")
                continue

            blog_post = create_blog_post(toot_id, article_text, url)

            with open(blog_path, "w", encoding="utf-8") as f:
                f.write(blog_post)

            print(f"✅ Blog post saved: {blog_path}")

        except Exception as e:
            print(f"❌ Error processing toot {toot_id}: {e}")

if __name__ == "__main__":
    main()
