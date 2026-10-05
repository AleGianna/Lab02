import csv
from csv import reader
from operator import truediv


def carica_da_file(file_path):
    """Carica le foto dal file,  creando un nuovo anno ogni volta che compare per la prima volta"""
    try:
        list = []
        f=open(file_path, "r")
        file=csv.reader(f)
        inte = next(file)
        anni = set()
        for row in file:
            diz={}
            diz[inte[0].strip()] = row[0]
            diz[inte[1].strip()] = row[1]
            diz[inte[2].strip()] = row[2]
            diz[inte[3].strip()] = int(row[3])
            diz[inte[4].strip()] = int(row[4])
            anni.add(int(row[4]))
            list.append(diz)
        album ={}
        for anno in anni:
            album[anno] = []
            for row in list:
                if anno == int(row["anno"]):
                   album[anno].append(row)
        f.close()
        return album
    except FileNotFoundError:
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""

    if not (1 <= mese <= 12):
        return None

    for dizAnni in album.values():
        for row in dizAnni:
            if row["codice"] == codice:
                return None

    newPhoto = {
        "codice": codice,
        "titolo": titolo,
        "autore": autore,
        "mese": mese,
        "anno": anno
    }

    try:
        with open(file_path, mode="a", newline="", encoding="utf-8") as f_writer:
            writer = csv.writer(f_writer)
            writer.writerow([codice, titolo, autore, mese, anno])
    except FileNotFoundError:
        return None

    if anno not in album:
        album[anno] = []
        print(f"Prima foto dell'anno {anno}")

    album[anno].append(newPhoto)

    return newPhoto

def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    for dizAnni in album.values():
        for row in dizAnni:
            if row["codice"] == codice:
                 risultato = row
                 return f"{row['codice']}, {row['titolo']}, {row['autore']}, {row['mese']}, {row['anno']}"

    return None

def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    titoli=[]
    s=False
    for anni in album.keys():
        if anno == anni:
            s = True
            break
    if not s:
        return None
    for row in album[int(anno)]:
            titoli.append(row["titolo"])
    titoli.sort()
    return titoli


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    print("album caricato!")
                    break
                print(f"file {file_path} non trovato")

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                if not 1<=mese<=12 :
                   print("Il mese selezionato non esiste")
                else:
                    print("La foto è già presente nel album")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
