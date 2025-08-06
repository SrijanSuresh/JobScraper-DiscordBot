import requests
from bs4 import BeautifulSoup

# Sites to scrape
job_sites = {
    "Google": "https://careers.google.com/jobs/results/?q=new%20grad",
    "Meta": "https://www.metacareers.com/jobs?new_grad=1",
    "Amazon": "https://www.amazon.jobs/en/teams/university-tech",
    "NVIDIA": "https://www.nvidia.com/en-us/about-nvidia/careers/university-recruiting/"
}

keywords = ["New Grad 2026", "Graduating 2026", "Bachelors", "University Graduate", "Entry Level"]

DISCORD_WEBHOOK = ""  # replace this

def notify_discord(message):
    payload = {
        "content": message
    }
    requests.post(DISCORD_WEBHOOK, json=payload)

def check_jobs():
    results = []
    for company, url in job_sites.items():
        try:
            res = requests.get(url, timeout=10)
            if any(kw.lower() in res.text.lower() for kw in keywords):
                results.append(f"🎯 `{company}` might have a match!\n🔗 {url}")
        except Exception as e:
            print(f"[!] Error scraping {company}: {e}")
    
    if results:
        notify_discord("\n\n".join(results))
    else:
        print("No new matches found.")

def lambda_handler(event, context):
    check_jobs()
    return {
        'statusCode': 200,
        'body': 'Job check done'
    }
