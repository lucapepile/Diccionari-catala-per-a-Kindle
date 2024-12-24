# Diccionari-catala-per-a-Kindle
Aquesta és una versió del DIEC2, utilitzable a Kindle. Està feta a partir de la versió .epub del diccionari, a partir de la qual s'ha construït la versió html (fitxer content.html) amb els criteris exigits per Amazon mitjançant reemplaçaments per expressions regulars. A partir d'aquesta versió, s'hi ha afegit tota la morfologia nominal i verbal mitjançant el diccionari per a Hunspell de Sofcatalà. S'han creat tots els fitxers necessaris per poder exportar el diccionari a un format .mobi, mitjançant Kindle Previewer. El fitxer resultant és el que s'ha de copiar mitjançant USB a la carpeta _documents > dictionaries_ del Kindle.

**Els passos a seguir són els següents:**  
1) Descarrega tots els documents en una carpeta, juntament amb el [diccionari.txt](https://github.com/Softcatala/catalan-dict-tools/blob/master/resultats/lt/diccionari.txt) de Softcatalà.  
2) Executa el codi ordenar_diccionari.py. Això crearà un fitxer morfologia.csv, amb tota la flexió nominal i verbal, i apòstrofs perquè el diccionari ho pugui reconèixer.
3) Executa el codi partir_content.py. Això crearà una carpeta nova anomenada parts_html i hi partirà el fitxer content.html en 300 parts, ja que Kindle Previewer no pot processar els fitxers grans.
4) Executa el codi derivar_parts.py. Això comprovarà si les entrades del diccionari coincideixen amb les paraules arrel del fitxer morfologia.csv i en cas afirmatiu, afegirà tota la morfologia necessària a cada paraula que apareix al diccionari, perquè Kindle ho pugui reconèixer.

Cal tindre el compte que els meus coneixements de programació són pràcticament nuls. Tot el codi ha estat escrit mitjançant IA. La meua feina, a base d'assaig error, ha consistit en ajustar-lo simplificant i ajustant al màxim les demandes al programador. El diccionari inclou algunes apostrofacions no utilitzades en català, de manera que hi ha cert marge per ajustar-lo.
