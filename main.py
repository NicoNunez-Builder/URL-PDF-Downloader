import requests
from bs4 import BeautifulSoup
import os
import re

# URL that directly lists Family Law forms:
# The parameter "filter=FL" is used on the official website to filter by Family Law forms.
FAMILY_LAW_FORMS_URL = "https://www.courts.ca.gov/forms.htm?filter=FL"

def download_family_law_forms(url, output_folder="Family_Law_Forms"):
    """
    Downloads all PDF files linked on the given page (for Family Law forms)
    to the specified output folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Fetch the page
    print(f"Fetching forms page: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching the page: status code {response.status_code}")
        return

    # Parse the page HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <a> tags whose href ends with ".pdf" (case-insensitive)
    links = soup.find_all('a', href=re.compile(r'(?i)\.pdf$'))
    if not links:
        print("No PDF links found on the page.")
        return

    # Download each PDF
    for link in links:
        file_url = link['href']

        # The PDF link might be relative (starting with '/')
        # If so, prepend the domain
        if file_url.startswith('/'):
            file_url = "https://www.courts.ca.gov" + file_url

        # Extract just the filename at the end of the URL
        file_name = file_url.split('/')[-1]

        # Download the PDF and save to disk
        print(f"Downloading {file_name} from {file_url}...")
        pdf_response = requests.get(file_url)
        if pdf_response.status_code == 200:
            save_path = os.path.join(output_folder, file_name)
            with open(save_path, 'wb') as pdf_file:
                pdf_file.write(pdf_response.content)
            print(f"Saved to {save_path}")
        else:
            print(f"Failed to download {file_url} (status code {pdf_response.status_code})")

if __name__ == "__main__":
    download_family_law_forms(FAMILY_LAW_FORMS_URL)
