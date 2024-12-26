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

    # Funció per afegir "l'" a paraules que comencen per vocal o h
    def add_apostrophe(word):
        if word[0] in 'aeiouhAEIOUH':
            return f"l'{word}"
        return None

    # Funció per afegir "d'" a verbs en infinitiu, gerundi i participi
    def add_d_apostrophe(word):
        if word.endswith(('ar', 'er', 're', 'ir', 'nt', 't', 'da', 'ts', 'des')) and word[0] in 'aeiouhAEIOUH':
            return f"d'{word}"
        return None

    # Funció per afegir "m'", "t'", "s'", "n'" a verbs flexionats
    def add_pronoun_apostrophes(word):
        if word[0] in 'aeiouhAEIOUH':
            return [f"m'{word}", f"t'{word}", f"s'{word}", f"n'{word}"]
        return []

    # Funció per afegir "'m", "'t", "'l", "'s", "'n" a verbs que acaben en vocal
    def add_suffix_apostrophes(word):
        # Comprovem si la paraula acaba en "-eu" i la tractem com si acabés en consonant
        if word.endswith('eu'):
            return []  # No afegim sufixos com "'m", "'t", "'l", "'s", "'n" a paraules que acaben en -eu
        if word[-1] in 'aeiouAEIOU':  # Si acaba en vocal
            return [f"{word}'m", f"{word}'t", f"{word}'l", f"{word}'s", f"{word}'n"]
        return []

    # Escriu al fitxer de sortida
    with open(output_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Escriu cada arrel i els seus derivats a una fila
        for root, derived_list in word_dict.items():
            derived_set = set(derived_list)

            # Aplica "l'" a l'arrel i derivats si comencen per vocal o h
            derived_set.update(filter(None, [add_apostrophe(word) for word in [root] + derived_list]))

            # Si és verb (més de 10 derivats), aplica les regles addicionals
            if len(derived_list) > 10:
                derived_set.update(filter(None, [add_d_apostrophe(word) for word in derived_list]))

                # Aplica "m'", "t'", "s'", "n'" a formes verbals flexionades
                for word in derived_list:
                    derived_set.update(add_pronoun_apostrophes(word))

                # Aplica "'m", "'t", "'l", "'s", "'n" a verbs que acaben en vocal
                for word in derived_list:
                    derived_set.update(add_suffix_apostrophes(word))

            # Escriu al fitxer CSV
            writer.writerow([root] + sorted(derived_set))

# Nom dels fitxers d'entrada i sortida
input_file = "diccionari.txt"
output_file = "morfologia.csv"

# Executa el procés
process_text_to_csv(input_file, output_file)

print(f"S'ha generat el fitxer {output_file} amb èxit!")

