"""
projekt_3.py: treti projekt do Engeto Online Python Akademie
author: Michaela Hronová
email: hronova.michaela09@gmail.com; hronova@ceps.cz
discord: Míša H.#5316
"""

import requests
from bs4 import BeautifulSoup
import unicodedata
from typing import Dict


def extract_number_from_cell(cell) -> int:
    raw = unicodedata.normalize("NFKC", cell.text)
    value = int(raw.replace(" ", ""))
    return value


def extract_overall_data(table_overall) -> Dict[str, int]:
    rows = table_overall.find_all("tr")
    row_data = rows[2]
    data = row_data.find_all("td")
    overall_dict = {}
    overall_dict["registered"] = extract_number_from_cell(data[3])
    overall_dict["envelopes"] = extract_number_from_cell(data[4])
    overall_dict["valid"] = extract_number_from_cell(data[7])
    return overall_dict


def extract_party_table(table_parties) -> Dict[str,int]:
    rows = table_parties.find_all("tr")
    party_dict = {}
    for row in rows[2:]:
        row_cells = row.find_all("td")
        party_cell = row_cells[1]
        party_name = party_cell.text
        votes_cell = row_cells[2]
        votes_count = extract_number_from_cell(votes_cell)
        party_dict[party_name] = votes_count
    return party_dict


def extract_result_page(parsed_text) -> Dict[str, int]:
    tables = parsed_text.find_all("table")
    overall_dict = extract_overall_data(tables[0])
    party_votes_dict = {}
    for table in tables_parties:
        party_votes_dict.update(extract_party_table(table_parties=table))
    overall_dict.update(party_votes_dict)
    return overall_dict    