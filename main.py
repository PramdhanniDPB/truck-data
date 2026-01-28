import requests
import json
import re
import datetime


# Function to fetch data from URL
def fetch_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

# Main execution
if __name__ == "__main__":
    year = 2024
    url = "http://10.10.206.205/data/api/nopolactive?year={}".format(year)
    data = fetch_url(url)

    # Process data
    seen_nopol = set()
    duplicates = []
    unique_data = []

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                # Add trnp_code
                if item.get('trnp'):
                    # Extract letters before space or -
                    item['trnp_code'] = re.split(r'[\s-]', item['trnp'])[0]

                # Check for duplicates in nomor_polisi
                nopol = item.get('nomor_polisi')
                if nopol:
                    # Remove spaces
                    cleaned_nopol = str(nopol).replace(' ', '')
                    item['nomor_polisi'] = cleaned_nopol

                    if cleaned_nopol in seen_nopol:
                        duplicates.append(cleaned_nopol)
                        continue # Skip adding this item to unique_data
                    else:
                        seen_nopol.add(cleaned_nopol)

                unique_data.append(item)

    data = unique_data

    if duplicates:
        print(f"Removed {len(duplicates)} duplicate nomor_polisi:")
        for d in duplicates:
            print(f"- {d}")
    else:
        print("No duplicate nomor_polisi found.")

    output_file = 'truck-' + str(year) + '.json'
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Data exported to {output_file}")