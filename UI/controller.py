import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def mostra_tratte(self, e):
        """
        Funzione che controlla prima se il valore del costo inserito sia valido (es. non deve essere una stringa) e poi
        popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Hub presenti
        * Numero di Tratte
        * Lista di Tratte che superano il costo indicato come soglia
        """
        # TODO
        # Validazione della Soglia
        soglia_str = self._view.guadagno_medio_minimo.value
        self._view.lista_visualizzazione.controls.clear()

        if not soglia_str:
            self._view.lista_visualizzazione.controls.append(
                ft.Text("**Attenzione:** Inserisci un valore numerico come soglia.", weight=ft.FontWeight.BOLD)
            )
            self._view.update()
            return

        try:
            soglia = float(soglia_str)
            if soglia < 0:
                self._view.lista_visualizzazione.controls.append(
                    ft.Text("**Attenzione:** La soglia deve essere un valore non negativo.",
                            weight=ft.FontWeight.BOLD)
                )
                self._view.update()
                return
        except ValueError:
            self._view.lista_visualizzazione.controls.append(
                ft.Text("**Errore:** La soglia inserita non è un numero valido.", weight=ft.FontWeight.BOLD)
            )
            self._view.update()
            return

        #Costruzione del Grafo nel Model
        try:
            # Chiama la funzione nel Model per costruire il grafo e filtrare le tratte
            self._model.costruisci_grafo(soglia)
        except Exception as ex:
            # Gestionce gli errori che possono avvenire durante la connessione/query
            self._view.lista_visualizzazione.controls.append(
                ft.Text(f" Errore:Impossibile costruire il grafo. Dettagli: {ex}", weight=ft.FontWeight.BOLD)
            )
            self._view.update()
            return

        # 3. Recupero delle Statistiche e Aggiornamento della View

        num_nodi = self._model.get_num_nodes()
        num_archi = self._model.get_num_edges()
        lista_tratte = self._model.get_all_edges()

        # Aggiunta delle informazioni generali
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Analisi Hub Completata (Soglia: {soglia:.2f} €) ", weight=ft.FontWeight.BOLD, size=16)
        )
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Hub presenti (Nodi): **{num_nodi}**", weight=ft.FontWeight.BOLD)
        )
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Tratte valide (Archi): **{num_archi}**", weight=ft.FontWeight.BOLD)
        )
        self._view.lista_visualizzazione.controls.append(ft.Divider())

        # Aggiunta della lista delle tratte
        if num_archi == 0:
            self._view.lista_visualizzazione.controls.append(
                ft.Text("Nessuna tratta commerciale ha raggiunto la soglia di guadagno specificata.")
            )
        else:
            self._view.lista_visualizzazione.controls.append(
                ft.Text("### Elenco Tratte Valide:", weight=ft.FontWeight.BOLD, size=14)
            )

            # Ciascun elemento di lista_tratte è una tupla (u, v, data), dove u e v sono oggetti Hub
            for i, (u, v, data) in enumerate(lista_tratte, start=1):
                guadagno_medio = data['weight']

                # Aggiungi l'indice 'i)' all'inizio della stringa
                tratta_info = (
                    f"{i}) [{u.codice} ({u.citta}) <-> {v.codice} ({v.citta})] "
                    f"- Guadagno Medio: **{guadagno_medio:.2f} €**"
                )
                self._view.lista_visualizzazione.controls.append(
                    ft.Text(tratta_info)
                )
        # Aggiornamento finale dell'interfaccia Flet
        self._view.update()

