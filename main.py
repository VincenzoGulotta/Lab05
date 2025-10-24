import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)

    def counter():

        # All'interno delle funzioni ho bisogno di trasformare il valore in int e poi nuovamente in str
        # altrimenti solleva un errore in txtOut.value

        def counterAdd(e):
            valore = int(txtOut.value)
            if valore < 7:
                txtOut.value = str(valore + 1)
                txtOut.update()

        def counterMinus(e):
            valore = int(txtOut.value)
            if valore > 1:                      # Costringo l'utente a inserire valori validi
                txtOut.value = str(valore - 1)
                txtOut.update()

        btnAdd = ft.IconButton(icon = ft.Icons.ADD_CIRCLE_ROUNDED,
                               icon_color = "green",
                               icon_size = 20,
                               on_click = counterAdd)

        btnMinus = ft.IconButton(icon = ft.Icons.REMOVE_CIRCLE_ROUNDED,
                                 icon_color = "red",
                                 icon_size = 20,
                                 on_click = counterMinus)

        # In txtOut.value non potevo inserire un int altrimenti dava errore
        txtOut = ft.TextField(width = 100,
                              border_color = "white",
                              disabled = True,
                              value = "2",
                              text_align = ft.TextAlign.CENTER)

        row = ft.Row([btnMinus, txtOut, btnAdd], alignment=ft.MainAxisAlignment.CENTER)

        # nel return faccio diventare txtOut.value di nuovo un int per requisiti dell'oggetto "automobile"
        return row, txtOut

    row, txtOut = counter() # Conservo la riga del counter ed il counter stesso, in modo da poter accedere
                            # successivamente al valore del counter


    marca = ft.TextField(text_size=20, label="Marca")
    modello = ft.TextField(text_size=20, label="Modello")
    anno = ft.TextField(text_size=20, label="Anno")


    def inserisci_auto(e):                      # Definisco una funzione per inserire le auto da chiamare successivamente

        if not Handlers():                      # Verifico che i valori inseriti siano validi

            num_posti = int(txtOut.value)       # Chiamo num_posti dentro la funzione così restituisce il valore aggiornato quando clicco,
                                                # se l'avessi chiamato fuori dalla funzione avrebbe restituito il valore iniziale del counter
            autonoleggio.aggiungi_automobile(
                marca.value,
                modello.value,
                anno.value,
                num_posti)
            aggiorna_lista_auto()               # Chiamo la funzione che aggiorna la lista di auto definita sotto

    # Definisco la riga aggiuntiva per l'inserimento delle auto

    row1 = ft.Row([marca, modello, anno, row], alignment=ft.MainAxisAlignment.CENTER)


    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto

    def Handlers():
        if not marca.value:             # Voglio che marca non sia vuoto
            alert.show_alert("❌ Errore: Inserisci una marca valida")
            return True

        if not modello.value:           # Voglio che modello non sia vuoto
            alert.show_alert("❌ Errore: Inserisci una modello valido")
            return True

        if not anno.value.isdigit() or not len(anno.value) == 4:    # Voglio che anno sia un numero e sia di 4 cifre
            alert.show_alert("❌ Errore: Inserisci un valore numerico valido per l'anno")
            return True
        return False

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto

    pulsante_inserisci_auto = ft.ElevatedButton("Inserisci automobile",
                                                on_click = inserisci_auto)      # Con "on_click" chiamo la funzione "inserisci_auto" che
                                                                                # a sua volta chiama "aggiorna_lista_auto" e "aggiungi_automobile"

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),

        # Sezione 3
        row1,
        pulsante_inserisci_auto,

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)