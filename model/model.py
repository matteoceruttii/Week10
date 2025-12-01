from database.DAO import DAO
import networkx as nx
from geopy.distance import geodesic

class Model:
    def __init__(self):
        self._lista_fermate =[]
        self._dizionario_fermate = {}
        self._grafo = None

    def getAllFermate(self):
        # model memorizza le fermate
        fermate = DAO.readAllFermate()
        self._lista_fermate = fermate

        for fermata in self._lista_fermate:
            self._dizionario_fermate[fermata.id_fermata] = fermata

    def creaGrafo(self):
        # grafo semplice
        self._grafo = nx.MultiDiGraph()       # posso avere più archi tra due nodi (il DiGraph me ne dava uno con un peso maggiore)

        # definisco i nodi
        for fermata in self._lista_fermate:
            self._grafo.add_node(fermata)

        # ricerca dei nodi vicini (PRIMO MODO)
        '''# definisco gli archi
        for u in self._grafo:       # per ogni nodo
            for v in self._grafo:    # per ognuno dei possibili nodi connessi
                risultato = DAO.existConnessioneTra(u, v)
                if (len(risultato) > 0):        # c'è un arco
                    self._grafo.add_edge(u, v)
                    print(f"Aggiunto l'arco tra {u} e {v}")'''

        # ricerca dei nodi vicini (SECONDO MODO)
        '''for u in self._grafo:
            connessioniAVicini = DAO.searchViciniAFermata(u)
            for connessione in connessioniAVicini:
                fermataArrivo = self._dizionario_fermate[connessione.id_fermata]
                self._grafo.add_edge(u, fermataArrivo)
                print(f"Aggiunto arco tra {u} e {fermataArrivo}")
                print(len(self._grafo.edges()))'''

        # TERZO MODO (una query sola che estrae tutte le connessioni)
        '''lista_connessioni = DAO.readAllConnessioni()
        for c in lista_connessioni:
            u_nodo = self._dizionario_fermate[c.id_stazP]
            v_nodo = self._dizionario_fermate[c.id_stazA]
            self._grafo.add_edge(u_nodo, v_nodo)
            print(f'Aggiunto arco tra {u_nodo} e {v_nodo}')'''


        # COSTRUISCO UN GRAFO PESATO
        '''lista_connessioni = DAO.readAllConnessioni()
        for c in lista_connessioni:
            u_nodo = self._dizionario_fermate[c.id_stazP]
            v_nodo = self._dizionario_fermate[c.id_stazA]
            # funzione implementata su networkx per verificare se esiste un arco tra i due elementi (nodi)
            if self._grafo.has_edge(u_nodo, v_nodo):
                self._grafo[u_nodo][v_nodo]["peso"] += 1
            else:
                self._grafo.add_edge(u_nodo, v_nodo, peso = 1)
            print(f'Aggiunto arco tra {u_nodo} e {v_nodo}, peso = {self._grafo[u_nodo][v_nodo]["peso"]}')'''

        # MULTIDIGRAFO (multigrafo orientato)
        lista_connessioni = DAO.readAllConnessioni()
        for c in lista_connessioni:
            u_nodo = self._dizionario_fermate[c.id_stazP]
            v_nodo = self._dizionario_fermate[c.id_stazA]

            # tempo di percorrenza della line come peso degli archi
            #   a) velocità
            velocita = DAO.readVelocita(c._id_linea)

            #   b) distanza
            punto_u = (u_nodo._coordX, u_nodo._coordY)
            punto_v = (v_nodo._coordX, v_nodo._coordY)
            distanza = geodesic(punto_u, punto_v).km        # in km all'ora

            #   c) tempo
            tempo = distanza/velocita * 60

            self._grafo.add_edge(u_nodo, v_nodo, tempo = tempo)
            print(f'Aggiunto arco tra {u_nodo} e {v_nodo}, {velocita}, {distanza} {velocita}')

        print(self._grafo)