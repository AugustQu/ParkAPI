from bs4 import BeautifulSoup
import datetime

data_url = "http://www.ingolstadt.mobi/parkplatzauskunft.cfm"
city_name = "Ingolstadt"
file_name = "Ingolstadt"

# Additional information for single lots: http://www2.ingolstadt.de/Wirtschaft/Parken/Parkeinrichtungen_der_IFG/

def parse_html(html):
    soup = BeautifulSoup(html)

    # get time last updated
    data = {
        "last_updated": str(datetime.datetime.strptime(soup.p.string, "(%d.%m.%Y, %H.%M Uhr)")),
        "lots": []
    }

    # get all lots
    raw_lots = soup.find_all("tr")

    for lot in raw_lots:
        elements = lot.find_all("td")

        lot_name = elements[0].text

        data["lots"].append({
            "name": lot_name,
            "free": int(elements[1].text),
            "count": get_total_number(lot_name),
            "type": get_type(lot_name)
        })

    return data


def get_total_number(lot_name):
    mapping = {
        "Theater-West": 599,
        "Theater-Ost": 682,
        "Schloss": 435,
        "Münster": 384,
        "Reduit Tilly": 436,
        "Hallenbad": 836,
        "Festplatz": 1437,
        "Südl. Ringstraße": 257,
        "Hauptbahnhof": 812,
        "Nordbahnhof": 252,
        "Hauptbahnhof Ost": 240,
        "Congressgarage": 213
    }
    if lot_name not in mapping.keys():
        return 0
    else:
        return mapping[lot_name]


def get_type(lot_name):
    mapping = {
        "Theater-West": "Tiefgarage",
        "Theater-Ost": "Tiefgarage",
        "Schloss": "Tiefgarage",
        "Münster": "Tiefgarage",
        "Reduit Tilly": "Tiefgarage",
        "Hallenbad": "Parkplatz",
        "Festplatz": "Parkplatz",
        "Südl. Ringstraße": "Parkplatz",
        "Hauptbahnhof": "Parkhaus",
        "Nordbahnhof": "Parkplatz",
        "Hauptbahnhof Ost": "Parkhaus",
        "Congressgarage": "Tiefgarage"
    }
    if lot_name not in mapping.keys():
        return "unbekannt"
    else:
        return mapping[lot_name]


if __name__ == "__main__":
    file = open("../tests/ingolstadt.html")
    html_data = file.read()
    file.close()
    parse_html(html_data)
