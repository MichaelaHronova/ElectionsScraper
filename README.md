# Elections Scraper
Program umožňuje vybrat jakýkoliv územní celek z odkazu (https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) a pro příslušné obce vybraného okresu program stáhne volební výsledky a uloží je ve formátu CSV. Program ze stránky stáhne jednak souhrnné výsledky (počet registrovaných voličů, počet odevzdaných obálek a platných hlasů) a také počty hlasů odevzdaných jednotlivým politickým stranám a hnutím.

## Instalace

1. Nejdřív stáhněte program z GitHubu příkazem `git clone https://github.com/MichaelaHronova/ElectionsScraper.git`

2. Před samotným spuštěním programu je potřeba následujícím příkazem vytvořit virtuální prostředí `python -m venv venv`
3. Vytvořené virtuální prostředí se aktivuje příkazem `source venv/bin/activate` 
4. Dále je zapotřebí nainstalovat knihovny uvedené v souboru requirements.txt., a to příkazem `pip install -r requirements.txt`


## Spouštění

Program se spouští dvěma argumenty, a sice 
1) odkazem v uvozovkách, z něhož má program extrahovat data (např.: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6207)
2) jménem výstupního souboru s příponou .csv (např. `vysledky_znojmo.csv`).

Příklad: `python ElectionsScraper.py 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6207' vysledky_znojmo.csv`
 