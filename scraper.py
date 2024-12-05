import requests
from bs4 import BeautifulSoup
import json

# URL of the page to scrape
params = [
    ("semeval-2021", "2021semeval"),
    ("semeval-2022", "2022semeval"),
    ("semeval-2023", "2023semeval"),
    ("semeval-2024", "2024semeval"),
]

for param in params:
    url = f"https://aclanthology.org/events/{param[0]}/"  # Replace with the actual URL

    # Send a GET request to the page
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful

    # Parse the page content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the main div containing the papers
    main_div = soup.find("div", id=f"{param[1]}-1")

    # List to store extracted data
    papers = []

    if main_div:
        # Find all <p> tags with the relevant class
        paper_entries = main_div.find_all("p", class_="d-sm-flex align-items-stretch")

        for entry in paper_entries:
            # Extract the title
            title_tag = entry.find("strong").find("a")
            title = title_tag.text.strip() if title_tag else "No title found"

            abs_link = entry.find("a", string="abs")  # Alternate approach matching by text
            if not abs_link:
                print("Abstract link not found in entry.")  # Debug: Report missing link
            else:
                abs_id = abs_link["href"].strip("#")  # Remove the '#' prefix
                # Find the div containing the abstract
                abstract_div = main_div.find("div", id=abs_id)
                if abstract_div:
                    card_body = abstract_div.find("div", class_="card-body")
                    abstract = card_body.text.strip() if card_body else "No abstract found"
                else:
                    print(f"No div found with id: {abs_id}")  # Debug: Log missing abstract div
                    abstract = "No abstract found"

            # Append the paper's information
            papers.append({"title": title, "abstract": "No abstract found" if not abs_link else abstract})

    # Save the extracted data to a JSON file
    output_file = f"papers-{param[0]}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=4)

    print(f"Extracted {len(papers)} papers. Saved to {output_file}.")
