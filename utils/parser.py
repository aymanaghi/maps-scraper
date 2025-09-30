def parse_results(soup, max_results):
    listings = []
    cards = soup.select(".Nv2PK")[:max_results]
    for card in cards:
        name = card.select_one(".qBF1Pd")
        rating = card.select_one(".MW4etd")
        address = card.select_one(".W4Efsd")
        website = card.select_one("a[href^='http']")

        listings.append({
            "name": name.text if name else "",
            "rating": rating.text if rating else "",
            "address": address.text if address else "",
            "website": website["href"] if website else ""
        })
    return listings
