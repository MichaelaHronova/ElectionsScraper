"""
projekt_3.py: treti projekt do Engeto Online Python Akademie
author: Michaela Hronová
email: hronova.michaela09@gmail.com; hronova@ceps.cz
discord: Míša H.#5316
"""

import requests
from bs4 import BeautifulSoup
import unicodedata
from typing import Dict, List, Tuple
import sys



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


def parse_result_page(parsed_text: BeautifulSoup) -> Dict[str, int]:
    tables = parsed_text.find_all("table")
    overall_dict = extract_overall_data(tables[0])
    party_votes_dict = {}
    for table in tables[1:]:
        party_votes_dict.update(extract_party_table(table_parties=table))
    overall_dict.update(party_votes_dict)
    return overall_dict    


def parse_region_page(parsed_text: BeautifulSoup) -> List[Dict[str, str]]:
    tables = parsed_text.find_all("table")
    counties_list = []
    for table in tables:
        rows = table.find_all("tr")
        for row in rows[2:]:
            county_dict = {}
            cells = row.find_all("td")
            county_dict["code"] = cells[0].text
            county_dict["location"] = cells[1].text
            county_dict["url"] = cells[2].a["href"]
            counties_list.append(county_dict)
    return counties_list   


def parse_url_county_page(parsed_text: BeautifulSoup) -> List[str]:
    table = parsed_text.find("table")
    cells = table.find_all("td")
    url_list = []
    for cell in cells:
        a_tag = cell.find("a")
        if a_tag is not None:
            url_list.append(a_tag.get("href"))
    return url_list


def read_input() -> Tuple[str, str]:
    if len(sys.argv) != 3:
        print("Incorrect number of parameters.")
        print("Please, provide 2 parameters.")
        sys.exit()
    url = sys.argv[1]
    csv_name = sys.argv[2]
    if not csv_name.endswith(".csv"):
        print("Second parameters should be a .csv file name.")
        sys.exit()
    return url, csv_name

if __name__== "__main__":
    url, csv_name = read_input()
    print(url)
    print(csv_name)
    