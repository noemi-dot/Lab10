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
                spedizione=Spedizione(row[""])
                pass