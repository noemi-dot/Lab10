from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = None
        self._edges = None
        self.G = nx.Graph()

    def costruisci_grafo(self, threshold):
        """
        Costruisce il grafo (self.G) inserendo tutti gli Hub (i nodi) presenti e filtrando le Tratte con
        guadagno medio per spedizione >= threshold (euro)
        """
        # TODO
        dao = DAO()
        id_map = {}

        #  Caricamento Nodi (Hub)
        # Se gli Hub non sono ancora stati caricati, li leggiamo e popoliamo il set di nodi
        if self._nodes is None or self.G.number_of_nodes() == 0:
            self._nodes = dao.leggi_hub()
            id_map = {hub.id: hub for hub in self._nodes}
            self.G.add_nodes_from(self._nodes)
        else:
            # Se i nodi esistono già, ricostruiamo la mappa per l'accesso
            id_map = {hub.id: hub for hub in self._nodes}

        # Pulisci gli archi precedenti per ricostruire il grafo con la nuova soglia
        self.G.clear_edges()

        #Caricamento e Aggregazione Spedizioni
        spedizioni_raw = dao.get_spedizioni_per_tratte()
        tratte_aggregate = {}

        for spedizione in spedizioni_raw:
            id_orig = spedizione['id_hub_origine']
            id_dest = spedizione['id_hub_destinazione']
            valore = spedizione['valore_merce']

            # Normalizza la tratta
            coppia_hub = frozenset({id_orig, id_dest})

            if coppia_hub not in tratte_aggregate:
                tratte_aggregate[coppia_hub] = [0.0, 0]

                # Aggiorna i totali
            tratte_aggregate[coppia_hub][0] += valore
            tratte_aggregate[coppia_hub][1] += 1

        #Aggiunta Archi (con filtro)
        for coppia_hub, dati_tratta in tratte_aggregate.items():

            valore_totale = dati_tratta[0]
            numero_spedizioni = dati_tratta[1]

            # Calcola guadagno medio
            valore_medio = valore_totale / numero_spedizioni

            #Aggiungi solo se il valore medio supera la soglia
            if valore_medio >= threshold:
                # Estrai gli ID dalla coppia
                id1, id2 = tuple(coppia_hub)

                # Ottieni gli oggetti Hub da usare come nodi in NetworkX
                u = id_map.get(id1)
                v = id_map.get(id2)

                if u and v:
                    # Aggiungi l'arco con il peso (weight)
                    self.G.add_edge(u, v, weight=valore_medio)

    def get_num_edges(self):
        """
        Restituisce il numero di Tratte (edges) del grafo
        :return: numero di edges del grafo
        """
        # TODO
        return self.G.number_of_edges()
    def get_num_nodes(self):
        """
        Restituisce il numero di Hub (nodi) del grafo
        :return: numero di nodi del grafo
        """
        # TODO
        return self.G.number_of_nodes()

    def get_all_edges(self):
        """
        Restituisce tutte le Tratte (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """
        # TODO
        # Restituisce una lista di tuple (u, v, data), dove data è un dizionario con 'weight'
        # e aggiorna self._edges
        self._edges = list(self.G.edges(data=True))
        return self._edges

