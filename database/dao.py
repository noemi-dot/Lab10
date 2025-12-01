from unittest import result

from database.DB_connect import DBConnect
from model.hub import Hub
from model.compagnia import Compagnia
from model.spedizione import Spedizione

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO
    @staticmethod
    def leggi_hub():
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query="SELECT * FROM hub"
        try:
            cursor.execute(query)
            for row in cursor:
                hub=Hub(row["id"], row["codice"], row["nome"],row["citta"], row["stato"], row["latitudine"], row["longitudine"])
                result.append(hub)
        except Exception as e:
            print(f"errore durante la lettura della query")
            result= None
        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def leggi_compagnia():
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)

        query="SELECT * FROM compagnia"
        try:
            cursor.execute(query)
            for row in cursor:
                compagnia=Compagnia(row["id"], row["codice"], row["nome"])
                result.append(compagnia)
        except Exception as e:
            print("errore nella lettura della query")
            result= None
        finally:
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def leggi_spedizione():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query="SELECT * FROM spedizione"
        try:
            cursor.execute(query)
            for row in cursor:
                spedizione=Spedizione(row["id"],row["id_compagnia"], row["numero_tracking"], row["id_hub_origine"], row["id_hub_destinazione"], row["data_ritiro_programmata"], row["distanza"], row["data_consegna"], row["valore_merce"])
                result.append(spedizione)
        except Exception as e:
            print("errore nella lettura della query")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def get_spedizioni_per_tratte():
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)

        # Query semplice: recupera i dati necessari per calcolare le tratte
        query = """
        SELECT
            id_hub_origine,
            id_hub_destinazione,
            valore_merce
        FROM
            spedizione
        WHERE
            id_hub_origine <> id_hub_destinazione
        """

        try:
            cursor.execute(query)
            # Restituisce una lista di dizionari con i dati delle spedizioni
            result = cursor.fetchall()

        except Exception as e:
            print(f"Errore durante l'esecuzione della query per le spedizioni: {e}")
            result = None

        finally:
            cursor.close()
            cnx.close()

        return result