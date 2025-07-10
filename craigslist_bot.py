# Craigslist Daily Alert Bot for "musician wanted" and "guitar teacher"
# Sends email to coyotevolkmusic@gmail.com

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# CONFIGURATION
SENDER_EMAIL = "coyotevolkmusic@gmail.com"
RECEIVER_EMAIL = "coyotevolkmusic@gmail.com"
APP_PASSWORD = "Gigme135b7"  # Gmail app password
KEYWORDS = ["musician wanted", "guitar teacher"]
BASE_URL = "https://losangeles.craigslist.org"
SEARCH_URLS = [
    "https://losangeles.craigslist.org/search/muc?sort=date",         # Central LA
    "https://losangeles.craigslist.org/search/lss?sort=date",
    "https://losangeles.craigslist.org/wst/search/muc?sort=date",    # West LA
    "https://losangeles.craigslist.org/wst/search/lss?sort=date",
    "https://losangeles.craigslist.org/lgb/search/muc?sort=date",    # Long Beach
    "https://losangeles.craigslist.org/lgb/search/lss?sort=date"     # Long Beach lessons
]

# Scrape function
def scrape_craigslist():
    matches = []
    for url in SEARCH_URLS:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for post in soup.find_all("li", class_="result-row"):
            title = post.find("a", class_="result-title hdrlnk").text.lower()
            link = post.find("a", class_="result-title hdrlnk")["href"]
            if any(keyword in title for keyword in KEYWORDS):
                matches.append(f"- {title.title()}\n{link}")
    return matches

# Email sending function
def send_email(listings):
    if not listings:
        return
    body = "New Craigslist Listings Found:\n\n" + "\n\n".join(listings)
    msg = MIMEText(body)
    msg["Subject"] = "🎸 New Craigslist Music Leads"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

# Main logic
if __name__ == "__main__":
    listings = scrape_craigslist()
    send_email(listings)
    print(f"Checked Craigslist on {datetime.now().strftime('%Y-%m-%d %H:%M')} — {len(listings)} matches found.")
