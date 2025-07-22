from mastodon import Mastodon
import os
import datetime

# Config
base_url = os.environ['MASTODON_BASE_URL']
token = os.environ['MASTODON_TOKEN']

mastodon = Mastodon(
    access_token=token,
    api_base_url=base_url
)

# Fetch latest toots
toots = mastodon.account_statuses("114768502244982655", limit=10)

# Ensure content/posts exists
os.makedirs("content/posts", exist_ok=True)

for toot in toots:
    toot_id = toot['id']
    created_at = toot['created_at']
    content = toot['content']

    filename = f"content/posts/{toot_id}.md"
    if os.path.exists(filename):
        continue

    with open(filename, "w") as f:
        f.write(f"---\n")
        f.write(f"title: \"Scam Alert {toot_id}\"\n")
        f.write(f"date: {created_at}\n")
        f.write(f"draft: false\n")
        f.write(f"---\n\n")
        f.write(f"{content}\n")
        f.write(f"\n[View on Mastodon]({toot['url']})\n")
