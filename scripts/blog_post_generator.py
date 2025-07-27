import os
import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def create_blog_post(toot_id: str, article_text: str, article_url: str, output_dir= str) -> str:
    """
    Generate a user-friendly blog post using ChatGPT based on the article text,
    include the original article URL, and save as a Markdown file.

    Returns the path to the saved Markdown file.
    """

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": (
                "You are a cybersecurity-focused blog writer. Your job is to rewrite consumer protection articles into ~500-word, friendly, funny, easy-to-understand blog posts "
                "for a general audience. Include key warnings and helpful takeaways. End with the original article URL."
            )},
            {"role": "user", "content": article_text}
        ],
        max_tokens=800,
        temperature=0.7,
    )

    blog_post = response.choices[0].message.content

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"{toot_id}.md")

    # Save Markdown file including original URL at the bottom
    with open(filename, "w", encoding="utf-8") as f:
        f.write(blog_post)
        f.write("\n\n---\n")
        f.write(f"Original article: {article_url}\n")

    return filename


if __name__ == "__main__":
    # Example usage
    toot_id = '114909168119844436'
    sample_url = "https://consumer.ftc.gov/consumer-alerts/2025/07/scammy-texts-offering-refunds-amazon-purchases"
    sample_text = """Scammers are pretending to be Amazon again. This time, they’re sending texts claiming there’s a problem with something you bought. They offer a refund if you click a link — but it’s a scam. Here’s how the scam works so you can avoid it.
You get an unexpected text that looks like it’s from Amazon. It claims the company did a “routine quality inspection” and an item you recently bought doesn’t meet Amazon’s standards or has been recalled. The text offers you a full refund and says you don’t need to return the item — as long as you click a link to request your money back. But there is no refund. Instead, it’s a
phishing scam
to steal your money or
personal information
.
To avoid a scam like this:
Don’t click links in unexpected texts
— and don’t respond to them. If you think the message could be legit, contact the company using a phone number, email, or website you know is real — not the info from the text.
Check your Amazon account
. If you’re worried, log in through the Amazon website or app — don’t use the link in the text — to see if there’s a problem with or recall on anything you’ve ordered.
Send unwanted texts to
7726 (SPAM)
or use your phone’s “report junk” option. Once you’ve reported it, delete the message.
Learn more about how to get fewer
spam texts
. And if you spot a scam, tell the FTC at
ReportFraud.ftc.gov
.
Want to know more about what to do if you have a problem with something you bought? Read
Solving Problems With a Business: Returns, Refunds, and Other Resolutions
.
"""

    output_path = create_blog_post(toot_id, sample_text, sample_url, '../content/posts')
    print(f"Blog post saved to: {output_path}")
