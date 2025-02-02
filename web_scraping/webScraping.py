import asyncio
from playwright.async_api import async_playwright
import json

async def run_scraping():
    async with async_playwright() as p:
        # Lansează browserul în modul headless
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Accesează pagina principală
        await page.goto("https://locuridinromania.ro/judetul-maramures")

        # Găsește toate link-urile ce au clasa 'elementor-post__thumbnail__link'
        links = await page.query_selector_all(".elementor-post__thumbnail__link")

        turistic_objects = []
        exclude_keywords = [
            "document.getElementById",
            "LocuriDinRomania.ro",
            "Sales Expert",
            "Mo Marketing",
            "Despre noi",
            "Termeni și condiții",
            "Cookies",
            "CUI",
            "PUBLISHING EXPERT",
            "Cum funcționează o drujbă cu motor 2T",
            "Alba", "Arad", "Argeș", "Bacău", "Bihor", "Bistrița-Năsăud",
            "Botoșani", "Brăila", "Brașov", "București", "Buzău", "Călărași",
            "Caraș-Severin", "Cluj", "Constanța", "Covasna", "Dâmbovița",
            "Dolj", "Galați", "Giurgiu", "Gorj", "Harghita", "Hunedoara",
            "Ialomița", "Iași", "Ilfov", "Maramureș", "Mehedinți", "Mureș",
            "Neamț", "Olt", "Prahova", "Sălaj", "Satu Mare", "Sibiu", "Suceava",
            "Teleorman", "Timiș", "Tulcea", "Vâlcea", "Vaslui", "Vrancea",
            "Biserici", "Cascade", "Castele", "Cetăți", "Grădini botanice",
            "Grădini zoologice", "Lacuri", "Mănăstiri", "Monumente", "Muzee",
            "Peșteri", "Saline", "Rezervații naturale", "Clădiri istorice",
            "Locuri de agrement", "Stațiuni turistice", "Monumente ale naturii",
            "Pârtii de schi", "Acest site folosește cookies",
            "Administrarea site-ului locuridinromania.ro este realizata de"
        ]

        # Parcurge fiecare link
        for idx, link in enumerate(links, start=1):
            url = await link.get_attribute("href")
            print(f"Accesăm: {url}")

            # Deschide pagina specifică
            page2 = await context.new_page()
            await page2.goto(url)

            # Extrage titlul (h1)
            title = await page2.query_selector("h1")
            title_text = await title.inner_text() if title else "Fără titlu"

            # Concatenează toate h3 și p pentru descriere
            h3_elements = await page2.query_selector_all("h3")
            p_elements = await page2.query_selector_all("p")

            description_text = ""
            for h3 in h3_elements:
                description_text += await h3.inner_text() + " "
            for p in p_elements:
                paragraph_text = await p.inner_text()
                if not any(keyword.lower() in paragraph_text.lower() for keyword in exclude_keywords):
                    description_text += paragraph_text + " "

            # Curățare suplimentară a descrierii
            description_text = description_text.replace("Cum funcționează o drujbă cu motor 2T?", "")

            # Filtrare suplimentară pentru descriere (aplicăm excluziile)
            description_text = " ".join([
                word for word in description_text.split()
                if not any(keyword.lower() in word.lower() for keyword in exclude_keywords)
            ])

            # Adaugă obiectul turistic la lista
            turistic_objects.append({
                "id": idx,
                "name": title_text.strip(),
                "description": description_text.strip(),
                "location": {
                    "county": "",
                    "city": "",
                    "latitude": "",
                    "longitude": ""
                },
                "category": "",
                "accommodation": [],
                "nearby_attractions": []
            })

            print(f"Titlu: {title_text}")
            print(f"Descriere: {description_text.strip()}")
            print("-" * 40)

            # Închide pagina curentă
            await page2.close()

        # Închide browserul
        await browser.close()

        # Salvează datele în format JSON
        with open("obiective-maramures.json", "w", encoding="utf-8") as f:
            json.dump({"obiective-maramures": turistic_objects}, f, ensure_ascii=False, indent=2)

        print("Datele au fost salvate în 'turistic_data.json'.")

# Rulează scriptul direct în event loop existent
await run_scraping()
