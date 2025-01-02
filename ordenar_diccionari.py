import csv
import re
from collections import defaultdict

# Funció per processar el document de text i extreure dades amb les noves regles
def process_text_to_csv(input_file, output_file):
    # Diccionari per agrupar derivats per arrel
    word_dict = defaultdict(list)

    # Llegeix el fitxer d'entrada
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.readlines()

    # Cerca línies que segueixin el patró: "forma arrel etiqueta"
    pattern = re.compile(r'^(\S+)\s+(\S+)\s+\S+$')

    for line in content:
        match = pattern.match(line)
        if match:
            derived, root = match.groups()
            if derived != root:  # Evita duplicar l'arrel com a derivat
                word_dict[root].append(derived)

    # Escriu al fitxer de sortida
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Escriu cada arrel i els seus derivats a una fila
        for root, derived_list in word_dict.items():
            derived_set = set(derived_list)
            # Escriu al fitxer CSV
            writer.writerow([root] + sorted(derived_set))

    # Elimina les primeres 27 línies del fitxer CSV
    with open(output_file, 'r', encoding='utf-8') as csvfile:
        lines = csvfile.readlines()

    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        csvfile.writelines(lines[27:])

# Nom dels fitxers d'entrada i sortida
input_file = "diccionari.txt"
output_file = "morfologia.csv"

# Executa el procés
process_text_to_csv(input_file, output_file)

print(f"S'ha generat el fitxer {output_file} amb èxit!")
