import os
import csv
from bs4 import BeautifulSoup

# Funció per afegir articles l' i d' per paraules que comencen per vocals o h
def afegir_articles(paraules):
    noves_flexions = set()  # Utilitzem un conjunt per evitar duplicats
    vocals_i_h = "aeiouhàèéíïòóúüAEIOUH"
    for paraula in paraules:
        if paraula and paraula[0] in vocals_i_h:
            noves_flexions.add(f"l'{paraula}")
            noves_flexions.add(f"d'{paraula}")
    return list(noves_flexions)

# Funció per afegir m', t', s' només a verbs que comencen per vocals o h
def afegir_pronoms(paraules):
    noves_flexions = set()  # Utilitzem un conjunt per evitar duplicats
    vocals_i_h = "aeiouhàèéíïòóúüAEIOUH"
    for paraula in paraules:
        if paraula and paraula[0] in vocals_i_h:
            noves_flexions.add(f"m'{paraula}")
            noves_flexions.add(f"t'{paraula}")
            noves_flexions.add(f"s'{paraula}")
    return list(noves_flexions)

# Funció per processar un fitxer HTML i actualitzar-lo
def processa_html(html_path, arrels_flexions):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Cerca les entrades amb <idx:orth>
    for idx_orth in soup.find_all("idx:orth"):
        paraula = idx_orth.text.strip()
        es_verb = False

        # Verifica si la paraula té un verb associat en un element <em class="v">
        verb = idx_orth.find_previous("em", class_="v")
        if verb:
            es_verb = True

        if paraula in arrels_flexions:
            # Crea el bloc <idx:infl> si no existeix
            if not idx_orth.find("idx:infl"):
                idx_infl = soup.new_tag("idx:infl")
                idx_orth.append(idx_infl)
            else:
                idx_infl = idx_orth.find("idx:infl")

            # Afegeix les flexions al bloc <idx:infl>
            flexions = arrels_flexions[paraula]

            if es_verb:
                # Per als verbs, afegim també les formes m', t', s' si comencen per vocals o h
                flexions += afegir_pronoms(flexions)

            # Per a altres paraules, afegim només l' i d' si comencen per vocals o h
            flexions += afegir_articles(flexions)

            # Elimina duplicats i assegura que les formes no inclouen l'entrada original
            flexions = list(set(flexions) - {paraula})

            for flexio in flexions:
                idx_iform = soup.new_tag("idx:iform", value=flexio)
                idx_infl.append(idx_iform)

    # Sobreescriu el fitxer HTML actualitzat, sense tancar etiquetes <idx:entry>
    html_output = str(soup)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_output)

# Llegeix el fitxer CSV
csv_file = "morfologia.csv"  # Canvia-ho si el fitxer té un altre nom o ubicació
arrels_flexions = {}
with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        paraula_arrel = row[0].strip()
        flexions = [col.strip() for col in row[1:]]
        arrels_flexions[paraula_arrel] = flexions

# Processa tots els fitxers HTML d'una carpeta
html_folder = "html_parts"  # Substitueix pel nom de la carpeta on tens els fitxers HTML
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

