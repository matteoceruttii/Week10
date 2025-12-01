import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

# funzione per generare il grafo
    def handleCreaGrafo(self,e):
        self._model.creaGrafo()

# funzione che restituice le possibili raggiungibili
    def handleCercaRaggiungibili(self,e):
        pass

# funzione che popola il dropdown
    def populate_dropdown(self, dd):
        self._model.getAllFermate()
        # le fermate le trovo nel model, in _lista_fermate

        for fermata in self._model._lista_fermate:
            # option con chiave (non visibile all'utente) e testo (mostrato)
            dd.options.append(ft.dropdown.Option(key = fermata.id_fermata,
                                                 text = fermata.nome))