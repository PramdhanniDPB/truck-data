import json
import re
from typing import Iterable

import requests


API_URL = "http://10.10.206.205/api_truck.php?year=2026"
OUTPUT_PATH = "truck-2026.json"

# Set keywords to match in the `loct` field (case-insensitive).
# Example: ["CITE", "BOGOR"]
KEYWORDS = ["CITEUREUP", "CIREBON", "BOSOWA", "GROBOGAN"]


def matches_loct(loct_value: str, keywords: Iterable[str]) -> bool:
	if not loct_value:
		return False
	loct_lower = loct_value.lower()
	return any(keyword.lower() in loct_lower for keyword in keywords)


def main() -> None:
	response = requests.get(API_URL, timeout=30)
	response.raise_for_status()
	data = response.json()

	if not isinstance(data, list):
		raise ValueError("Unexpected API response: expected a list of objects")

	for item in data:
		trnp_value = item.get("trnp", "")
		if trnp_value:
			# Extract letters before space or '-'.
			item["trnp_code"] = re.split(r"[\s-]", trnp_value)[0]

	filtered = [item for item in data if matches_loct(item.get("loct", ""), KEYWORDS)]

	with open(OUTPUT_PATH, "w", encoding="utf-8") as file_handle:
		json.dump(filtered, file_handle, ensure_ascii=False, indent=4)

	print(f"Saved {len(filtered)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
	if not KEYWORDS:
		raise SystemExit("Set KEYWORDS before running.")
	main()
