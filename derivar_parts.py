import os
import csv
from bs4 import BeautifulSoup

# Funció per processar un fitxer HTML i actualitzar-lo
def processa_html(html_path, arrels_flexions):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Cerca les entrades amb <idx:orth>
    for idx_orth in soup.find_all("idx:orth"):
        paraula = idx_orth.text.strip()

        flexions = []

        # Afegeix les flexions si la paraula està directament al diccionari
        if paraula in arrels_flexions:
            flexions.extend(arrels_flexions[paraula])

        # Si és un verb pronominal (acaba en -se), afegeix també les flexions de la forma sense -se
        if paraula.endswith("-se"):
            forma_no_pronominal = paraula[:-3]
            if forma_no_pronominal in arrels_flexions:
                flexions.extend(arrels_flexions[forma_no_pronominal])
            # També afegeix la forma sense -se com una flexió addicional
            flexions.append(forma_no_pronominal)

        # Només continua si hi ha flexions a afegir
        if flexions:
            # Crea el bloc <idx:infl> si no existeix
            if not idx_orth.find("idx:infl"):
                idx_infl = soup.new_tag("idx:infl")
                idx_orth.append(idx_infl)
            else:
                idx_infl = idx_orth.find("idx:infl")

            # Elimina duplicats i la paraula original de la llista
            flexions = list(set(flexions) - {paraula})

            # Afegeix les flexions com a <idx:iform>
            for flexio in sorted(flexions):  # sorted opcional per ordre alfabètic
                idx_iform = soup.new_tag("idx:iform", value=flexio)
                idx_infl.append(idx_iform)

    # Sobreescriu el fitxer HTML actualitzat
    html_output = str(soup)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_output)


# Llegeix el fitxer CSV
csv_file = "morfologia_i_apostrofs.csv"  # Canvia-ho si cal
arrels_flexions = {}
with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        paraula_arrel = row[0].strip()
        flexions = [col.strip() for col in row[1:] if col.strip()]
        arrels_flexions[paraula_arrel] = flexions

# Processa tots els fitxers HTML d'una carpeta
html_folder = "html_parts"  # Substitueix-ho pel nom correcte de la carpeta
for filename in os.listdir(html_folder):
    if filename.endswith(".html"):
        html_path = os.path.join(html_folder, filename)
        print(f"Processant: {html_path}")
        processa_html(html_path, arrels_flexions)

# Elimina etiquetes </idx:entry> al final del processament
for filename in os.listdir(html_folder):
    if filename.endswith(".html"):
        html_path = os.path.join(html_folder, filename)
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("</idx:entry>", "")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Processat: {html_path}")

print("Processament complet!")
