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
import pandas as pd


def parse_url_to_bs(url: str) -> BeautifulSoup:
    respond = requests.get(url)
    if respond.status_code != 200:
        raise ValueError(f"Invalid url - {url}")
    parsed_text = BeautifulSoup(respond.text, "html.parser")
    return parsed_text


def extract_number_from_cell(cell) -> int:
    raw = unicodedata.normalize("NFKC", cell.text)
    value = int(raw.replace(" ", ""))
    return value


def extract_overall_data(table_overall) -> Dict[str, int]:
    rows = table_overall.find_all("tr")
    row_data = rows[-1]
    data = row_data.find_all("td")
    overall_dict = {}
    overall_dict["registered"] = extract_number_from_cell(data[-6])
    overall_dict["envelopes"] = extract_number_from_cell(data[-5])
    overall_dict["valid"] = extract_number_from_cell(data[-2])
    return overall_dict


def extract_party_table(table_parties) -> Dict[str,int]:
    rows = table_parties.find_all("tr")
    party_dict = {}
    for row in rows[2:]:
        row_cells = row.find_all("td")
        party_cell = row_cells[1]
        party_name = party_cell.text
        if party_name != "-":
            votes_cell = row_cells[2]
            votes_count = extract_number_from_cell(votes_cell)
            party_dict[party_name] = votes_count
    return party_dict


def parse_result_page(url: str) -> Dict[str, int]:
    parsed_text = parse_url_to_bs(url)
    tables = parsed_text.find_all("table")
    overall_dict = extract_overall_data(tables[0])
    party_votes_dict = {}
    for table in tables[1:]:
        party_votes_dict.update(extract_party_table(table_parties=table))
    overall_dict.update(party_votes_dict)
    return overall_dict    


def parse_location_url(url: str, base_url: str) -> Dict[str, int]:
    if "xvyber" in url:
        return parse_result_page(base_url + url)
    url_list = parse_url_county_page(base_url + url)
    result_dict = parse_result_page(base_url + url_list[0])
    for url_county in url_list[1:]:
        county_dict = parse_result_page(base_url + url_county)
        for key in result_dict.keys():
            result_dict[key] += county_dict[key]
    return result_dict


def parse_region_page(url: str) -> List[Dict[str, str]]:
    parsed_text = parse_url_to_bs(url)
    tables = parsed_text.find_all("table")
    counties_list = []
    for table in tables:
        rows = table.find_all("tr")
        for row in rows[2:]:
            county_dict = {}
            cells = row.find_all("td")
            if cells[0].text.isnumeric():
                county_dict["code"] = cells[0].text
                county_dict["location"] = cells[1].text
                county_dict["url"] = cells[2].a["href"]
                counties_list.append(county_dict)
    return counties_list   


def parse_url_county_page(url: str) -> List[str]:
    parsed_text = parse_url_to_bs(url)
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
    base_url = url.rsplit("/", maxsplit=1)[0] + "/"
    village_list = parse_region_page(url)
    for village_dict in village_list:
        village_url = village_dict.pop("url")
        print(f"Getting results from: {village_dict['location']}")
        village_total_results = parse_location_url(village_url, base_url)
        for key in village_total_results.keys():
            village_dict[key] = village_total_results[key]

    df = pd.DataFrame.from_records(data=village_list)
    df.to_csv(csv_name, sep=",", index=False)
    print(f"Data written to file {csv_name}")

