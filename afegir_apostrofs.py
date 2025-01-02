import csv

def process_files(morfologia_file, apostrofs_file, output_file):
    # Llegir el fitxer morfologia.csv i emmagatzemar les dades en un diccionari
    morfologia_dict = {}
    with open(morfologia_file, 'r', encoding='utf-8') as morfologia:
        reader = csv.reader(morfologia)
        for i, row in enumerate(reader):
            if row:  # Comprovar que la fila no estigui buida
                arrel = row[0].strip()  # Eliminar espais
                derivats = [word.strip() for word in row[1:]]
                morfologia_dict[arrel] = derivats

    print("Fitxer morfologia.csv carregat correctament.")

    # Llegir el fitxer apostrofs.txt i afegir les paraules a les arrels corresponents
    with open(apostrofs_file, 'r', encoding='utf-8') as apostrofs:
        for i, line in enumerate(apostrofs):
            line = line.strip()
            if line:  # Comprovar que la línia no estigui buida
                # Trobar la base de la paraula
                if "'" in line:
                    # Separar la part abans i després de l'apòstrof
                    parts = line.split("'")
                    # Si la part abans de l'apòstrof és significativa, prioritzar-la
                    if len(parts[0]) > 1:
                        base_word = parts[0].strip()
                    else:  # Si no, usar la part després de l'apòstrof
                        base_word = parts[-1].strip()
                else:
                    base_word = line.strip()

                # Comprovació de depuració: Mostrem la paraula i la base
                print(f"Processant línia: {line}, Base detectada: {base_word}")

                # Cercar la base en qualsevol arrel o derivat i actualitzar la fila
                added = False
                for arrel, derivats in morfologia_dict.items():
                    # Si la base coincideix exactament amb l'arrel o un derivat
                    if base_word == arrel or base_word in derivats:
                        if line not in derivats:  # Evitar duplicats
                            derivats.append(line)  # Afegir la paraula a la llista de derivats
                            print(f"Afegint: {line} a {arrel}")
                            added = True
                            break

                if not added:
                    print(f"Advertència: {base_word} no trobat a morfologia.csv ni en els derivats.")

    print("Fitxer apostrofs.txt processat correctament.")

    # Escriure el resultat en un nou fitxer CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as output:
        writer = csv.writer(output)
        for arrel, paraules in morfologia_dict.items():
            writer.writerow([arrel] + paraules)  # Escriure arrel + derivats en la mateixa fila

    print(f"Fitxer generat: {output_file}")

# Exemple d'ús
morfologia_file = 'morfologia.csv'
apostrofs_file = 'apostrofs.txt'
output_file = 'morfologia_i_apostrofs.csv'
process_files(morfologia_file, apostrofs_file, output_file)

