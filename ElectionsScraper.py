"""
projekt_3.py: treti projekt do Engeto Online Python Akademie
author: Michaela Hronová
email: hronova.michaela09@gmail.com; hronova@ceps.cz
discord: Míša H.#5316
"""

import requests
from bs4 import BeautifulSoup
import unicodedata
from typing import Tuple

def extract_number_from_cell(cell) -> int:
    raw = unicodedata.normalize("NFKC", cell.text)
    value = int(raw.replace(" ", ""))
    return value

def extract_overall_data(table_overall) -> Tuple[int, int, int]:
    rows = table_overall.find_all("tr")
    row_data = rows[2]
    data = row_data.find_all("td")
    registered = extract_number_from_cell(data[3])
    envelopes = extract_number_from_cell(data[4])
    valid = extract_number_from_cell(data[7])
    return (registered, envelopes, valid)