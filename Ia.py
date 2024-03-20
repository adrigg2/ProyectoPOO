from random import choice
from Tablero import Tablero
from Vector import Vector

class Ia:
    __tablero: Tablero

    def __init__(self, tablero) -> None:
        self.__tablero = tablero

    def elegir_pieza(self, piezas_movibles: list[Vector]) -> str:
        piezas_elegibles: list[str] = [self.__tablero.codificar_posicion(i) for i in piezas_movibles]
        return choice(piezas_elegibles)

    def elegir_movimiento(self, posiciones_a_elegir) -> str:
        return choice(posiciones_a_elegir)
