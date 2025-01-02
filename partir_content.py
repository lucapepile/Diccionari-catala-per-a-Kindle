import os

def dividir_i_processar_diccionari(arxiu_entrada, carpeta_sortida, num_parts):
    # Crea la carpeta de sortida si no existeix
    os.makedirs(carpeta_sortida, exist_ok=True)

    # Primer pas: comptar el nombre total d'entrades
    num_entrades = 0
    with open(arxiu_entrada, 'r', encoding='utf-8') as fitxer:
        for linia in fitxer:
            if '<idx:entry' in linia:
                num_entrades += 1

    # Calcula la mida aproximada de cada part
    mida_part = max(1, num_entrades // num_parts)

    # Segon pas: processar i dividir el fitxer
    part_actual = 1
    entrada_actual = 0
    capcalera_html = (
        '<html xmlns:math="http://exslt.org/math" xmlns:svg="http://www.w3.org/2000/svg" '
        'xmlns:tl="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" '
        'xmlns:saxon="http://saxon.sf.net/" xmlns:xs="http://www.w3.org/2001/XMLSchema" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xmlns:cx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:mbp="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" '
        'xmlns:mmc="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" '
        'xmlns:idx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf">'
        '<head>'
        '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'
        '<link href="styles.css" type="text/css" rel="stylesheet" />'
        '<title>Diccionari de la llengua catalana (DIEC2)</title>'
        '</head>'
        '<body>'
        '<mbp:frameset>\n'
    )
    tancament_html = '  </mbp:frameset>\n  </body>\n</html>'

    fitxer_sortida = open(os.path.join(carpeta_sortida, f'part_{part_actual:03d}.html'), 'w', encoding='utf-8')
    fitxer_sortida.write(capcalera_html)

    with open(arxiu_entrada, 'r', encoding='utf-8') as fitxer:
        escrivint_entrada = False
        for linia in fitxer:
            if '<idx:entry' in linia:
                # Comença una nova entrada
                entrada_actual += 1
                escrivint_entrada = True

                # Si hem arribat al límit de la mida de la part, tanquem l'actual i obrim una nova
                if entrada_actual > mida_part and part_actual < num_parts:
                    fitxer_sortida.write(tancament_html)  # Tanca l'HTML actual
                    fitxer_sortida.close()
                    part_actual += 1
                    entrada_actual = 1  # Restablim el comptador per la nova part
                    fitxer_sortida = open(os.path.join(carpeta_sortida, f'part_{part_actual:03d}.html'), 'w', encoding='utf-8')
                    fitxer_sortida.write(capcalera_html)

            if '</div>' in linia and escrivint_entrada:
                # Acaba una entrada
                escrivint_entrada = False

            # Escriu la línia actual al fitxer de sortida
            fitxer_sortida.write(linia)

    # Tanca l'últim fitxer de sortida
    fitxer_sortida.write(tancament_html)
    fitxer_sortida.close()

    print(f"Divisió completada! Fitxers desats a '{carpeta_sortida}'.")

    # Tercer pas: esborrar etiquetes </idx:entry>
    for nom_fitxer in os.listdir(carpeta_sortida):
        cami_fitxer = os.path.join(carpeta_sortida, nom_fitxer)

        # Processa només fitxers HTML
        if os.path.isfile(cami_fitxer) and nom_fitxer.endswith('.html'):
            # Llegeix el contingut del fitxer
            with open(cami_fitxer, 'r', encoding='utf-8') as fitxer:
                contingut = fitxer.read()

            # Elimina totes les etiquetes </idx:entry>
            contingut_modificat = contingut.replace('</idx:entry>', '')

            # Guarda els canvis al mateix fitxer
            with open(cami_fitxer, 'w', encoding='utf-8') as fitxer:
                fitxer.write(contingut_modificat)

            print(f"Processat: {nom_fitxer}")

    print("Totes les etiquetes </idx:entry> han estat eliminades.")

# Exemple d'ús
dividir_i_processar_diccionari('content.html', 'html_parts', 300)
