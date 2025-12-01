from dataclasses import dataclass

@dataclass
class Fermata:
    _id_fermata : int
    _nome : str
    _coordX : float
    _coordY : float

    @property
    def id_fermata(self) -> int:
        return self._id_fermata

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def coordX(self) -> float:
        return self._coordX

    @property
    def coordY(self) -> float:
        return self._coordY

    def __str__(self):
        return f'Fermata: {self.id_fermata} {self.nome} {self._coordX} {self.coordY}'

    def __hash__(self):
        return hash(self.id_fermata)