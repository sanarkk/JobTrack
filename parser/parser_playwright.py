import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright


def scrape_hiring_cafe(search_term, n_of_jobs):
    """Scrapes Hiring.cafe for job listings via network interception"""

    print(f"Starting scrape: {search_term}")
    # URL encoding for the search query
    # https://hiring.cafe/?searchState=%7B%22searchQuery%22%3A%22data+engineer%22%2C%22dateFetchedPastNDays%22%3A-1%7D
    # https://hiring.cafe/?searchState=%7B%22searchQuery%22%3A%22{search_term}%22%7D
    
    url = f"https://hiring.cafe/?searchState=%7B%22searchQuery%22%3A%22{search_term}%22%2C%22dateFetchedPastNDays%22%3A-1%7D"
    collected_jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        def handle_response(response):
            """Intercepts JSON responses containing job data."""
            if "search-jobs" in response.url and response.status == 200:
                try:
                    data = response.json()
                    batch = []

                    if isinstance(data, list):
                        batch = data
                    elif isinstance(data, dict):
                        if "hits" in data and "hits" in data["hits"]:
                            batch = [h["_source"] for h in data["hits"]["hits"]]
                        elif "results" in data:
                            batch = data["results"]

                    if batch:
                        print(f"  Captured {len(batch)} jobs")
                        collected_jobs.extend(batch)
                except Exception:
                    pass

        page.on("response", handle_response)

        page.goto(url)
        page.wait_for_timeout(4000)

        print("Scrolling for more results...")
        previous_height = 0
        target_jobs = max(0, int(n_of_jobs))
        no_growth_scrolls = 0
        max_no_growth_scrolls = 2
        max_total_scrolls = 200

        for i in range(max_total_scrolls):
            if target_jobs and len(collected_jobs) >= target_jobs:
                print("  Reached requested job count")
                break

            before_count = len(collected_jobs)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)
            new_height = page.evaluate("document.body.scrollHeight")
            after_count = len(collected_jobs)
            new_jobs = after_count - before_count

            if new_jobs > 0:
                no_growth_scrolls = 0
            else:
                no_growth_scrolls += 1

            print(
                f"  Scroll {i + 1}: +{max(0, new_jobs)} jobs, total {after_count}"
            )

            if new_height == previous_height and new_jobs <= 0:
                print("  Reached end of results")
                break

            if no_growth_scrolls >= max_no_growth_scrolls:
                print("  No new jobs after multiple scrolls")
                break

            previous_height = new_height

        browser.close()

    # Deduplicate by ID and limit to requested count
    unique_jobs = list({job["id"]: job for job in collected_jobs if "id" in job}.values())
    if target_jobs:
        unique_jobs = unique_jobs[:target_jobs]
    return unique_jobs


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Parse script arguments")
    arg_parser.add_argument("search_term", help="Search term for the opening to be parsed")
    arg_parser.add_argument(
        "--n_jobs", type=int, default=200, help="Number of jobs to be scraped"
    )
    args = arg_parser.parse_args()

    term = args.search_term.lower().strip()
    n_jobs = args.n_jobs

    jobs = scrape_hiring_cafe(search_term=term, n_of_jobs=n_jobs)

    if jobs:
        filename = (
            Path(__file__).resolve().parents[1]
            / "data"
            / "raw"
            / f"{term.replace(' ', '_')}_jobs.json"
        )
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(jobs)} jobs to {filename}")
    else:
        print("No jobs found")
