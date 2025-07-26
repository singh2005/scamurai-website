from mastodon import Mastodon
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def get_recent_toots(limit=40):
	mastodon = Mastodon(
		access_token=os.environ['MASTODON_TOKEN'],
		api_base_url=os.environ['MASTODON_BASE_URL']
	)

	account_id = '114768502244982655'
	toots = mastodon.account_statuses(account_id, limit=limit)

	result = []
	for toot in toots:
		content_html = toot['content']
		original_url = extract_url_from_html(content_html)

		if original_url:
			result.append({
				"id": toot['id'],
				"date": toot['created_at'],
				"mastodon_url": toot['url'],
				"original_url": original_url,
				"raw_html": content_html
			})

	return result


def extract_url_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a"):
        href = a.get("href", "")
        # Ignore links to mastodon.social (hashtags, mentions)
        if not href.startswith("https://mastodon.social"):
            return href
    return None


if __name__ == "__main__":
	from pprint import pprint
	toots = get_recent_toots(limit=3)
	for toot in toots:
		pprint(toot)