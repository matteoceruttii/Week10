from database.DB_connect import DBConnect
from model.Connessione import Connessione
from model.Fermata import Fermata

class DAO():
    pass

    @staticmethod
    def readAllFermate():
        conn = DBConnect.get_connection()
        result = []
        query = ''' SELECT * FROM Fermata '''
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)

        # lettura del risultato tramite cursore
        for row in cursor:
            fermata = Fermata(row['id_fermata'], row['nome'], row['coordX'], row['coordY'])
            result.append(fermata)

        cursor.close()
        conn.close()
        return result       # restituisco lista di oggetti Fermata (DTO)


    @staticmethod
    def existConnessioneTra(u : Fermata, v : Fermata):
        # verifica se esiste una connessione tra nodo u e v
        conn = DBConnect.get_connection()
        result = []
        query = ''' SELECT COUNT(*)
                    FROM connessione c
                    WHERE c.id_stazP = %s AND c.id_stazA = %s '''
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (u.id_fermata, v.id_fermata ))       # tupla con i parametri
        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def searchViciniAFermata(u: Fermata):
        # cerco le stazioni collegate a quella passata come parametro
        conn = DBConnect.get_connection()
        result = []
        query = ''' SELECT *
                    FROM connessione c
                    WHERE c.id_stazP = %s '''

        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (u.id_fermata, ))  # tupla con i parametri
        for row in cursor:
            connessione = Connessione(row['id_connessione'],
                                      row['id_linea'],
                                      row['id_stazP'],
                                      row['id_stazA'])
            result.append(connessione)
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def readAllConnessioni():
        # cerco tutte le connessioni
        conn = DBConnect.get_connection()
        result = []
        query = ''' SELECT *
                    FROM connessione'''

        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        for row in cursor:
            connessione = Connessione(row['id_connessione'],
                                      row['id_linea'],
                                      row['id_stazP'],
                                      row['id_stazA'])
            result.append(connessione)
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def readVelocita(id_linea):
        # leggo la velocità delle linee lette dal database
        conn = DBConnect.get_connection()
        result = []
        query = ''' SELECT *
                    FROM linea
                    WHERE id_linea = %s '''

        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id_linea, ))
        for row in cursor:
            result.append(row['velocita'])
        cursor.close()
        conn.close()
        return result[0]        # la prima riga contiene la velocità letta