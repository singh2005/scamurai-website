import os
import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def create_blog_post(toot_id: str, article_text: str, article_url: str, toot_date: datetime) -> str:

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a cybersecurity-focused blog writer. Your job is to rewrite consumer protection articles into ~500-word, friendly, funny, "
                    "easy-to-understand blog posts for a general audience. Include key warnings and helpful takeaways.\n\n"
                    "Return your response in this exact format:\n\n"
                    "Title: [Catchy blog title]\n"
                    "Description: [One-sentence blog summary]\n"
                    "[The main blog content in markdown format]\n\n"
                    "End the blog content with a line that includes the original article URL."
                )
            },
            {"role": "user", "content": article_text}
        ],
        max_tokens=800,
        temperature=0.7,
    )

    full_output = response.choices[0].message.content.strip()

    # Extract title and description
    lines = full_output.splitlines()
    title_line = ""
    description_line = ""
    body_lines = []

    for line in lines:
        if line.lower().startswith("title:"):
            title_line = line.split(":", 1)[1].strip().strip('"')
        elif line.lower().startswith("description:"):
            description_line = line.split(":", 1)[1].strip().strip('"')
        else:
            body_lines.append(line)

    # Fallbacks if GPT doesn't follow format strictly
    title = title_line or "Scam Alert: Stay Safe Online"
    description = description_line or "Learn how to spot and avoid common scams in the digital world."
    date = toot_date.strftime("%Y-%m-%d")

    yaml_safe_title = title.replace("\n", " ").replace('"', '\\"')
    yaml_safe_description = description.replace("\n", " ").replace('"', '\\"')


    front_matter = f"""---
title: "{yaml_safe_title}"
date: {date}
description: "{yaml_safe_description}"
draft: false
---

"""

    blog_body = "\n".join(body_lines).strip()

    # Append article URL if it's not already present
    if article_url not in blog_body:
        blog_body += f"\n\n---\nOriginal article: {article_url}"

    return front_matter + blog_body



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

    blog_post = create_blog_post(toot_id, sample_text, sample_url)
    print(blog_post)
