import csv

def process_files_optimized(morfologia_file, apostrofs_file, output_file):
    # Crear un diccionari amb les arrels i els derivats
    morfologia_dict = {}
    word_to_root = {}  # Índex invers per cerques ràpides

    # Llegir el fitxer morfologia.csv i crear l'índex invers
    with open(morfologia_file, 'r', encoding='utf-8') as morfologia:
        reader = csv.reader(morfologia)
        for row in reader:
            if row:
                arrel = row[0].strip()
                derivats = set(word.strip() for word in row[1:])
                morfologia_dict[arrel] = derivats
                # Afegir arrel i derivats a l'índex invers
                word_to_root[arrel] = arrel
                for derivat in derivats:
                    word_to_root[derivat] = arrel

    print("Fitxer morfologia.csv carregat correctament.")

    # Llegir el fitxer apostrofs.txt i afegir les paraules a les arrels corresponents
    with open(apostrofs_file, 'r', encoding='utf-8') as apostrofs:
        for line in apostrofs:
            line = line.strip()
            if line:
                # Trobar la base de la paraula
                if "'" in line:
                    parts = line.split("'")
                    base_word = parts[0].strip() if len(parts[0]) > 1 else parts[-1].strip()
                else:
                    base_word = line.strip()

                # Cercar la base a l'índex invers
                root = word_to_root.get(base_word)
                if root:
                    # Afegir la paraula als derivats de la seva arrel si no hi és
                    if line not in morfologia_dict[root]:
                        morfologia_dict[root].add(line)  # Utilitzar conjunts per evitar duplicats
                        print(f"Afegint: {line} a {root}")
                else:
                    print(f"Advertència: {base_word} no trobat a morfologia.csv ni en els derivats.")

    print("Fitxer apostrofs.txt processat correctament.")

    # Escriure el resultat en un nou fitxer CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as output:
        writer = csv.writer(output)
        for arrel, derivats in morfologia_dict.items():
            writer.writerow([arrel] + sorted(derivats))  # Escriure arrel + derivats ordenats

    print(f"Fitxer generat: {output_file}")

# Exemple d'ús
morfologia_file = 'morfologia.csv'
apostrofs_file = 'apostrofs.txt'
output_file = 'morfologia_i_apostrofs.csv'

process_files_optimized(morfologia_file, apostrofs_file, output_file)
