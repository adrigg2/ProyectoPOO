from Tablero import Tablero
from Posicion import Posicion

class Pieza:
    posicion: Posicion
    direccion: Posicion
    promocionado: bool
    jugador: int
    tablero: Tablero
    diccionario_columna: dict[int, str]

    def __init__(self, posicion: Posicion, jugador: int, tablero: Tablero) -> None:
        self.posicion = posicion
        self.promocionado = False
        self.jugador = jugador
        self.tablero = tablero
        self.diccionario_columna = {
            0 : 'a',
            1 : 'b',
            2 : 'c',
            3 : 'd',
            4 : 'e',
            5 : 'f',
            6 : 'g',
            7 : 'h'
        }

        if self.jugador == 1:
            self.direccion = Posicion(1, -1)
        elif self.jugador == 2:
            self.direccion = Posicion(1, 1)
    
    def comprobar_movibilidad(self) -> bool:
        if not self.promocionado:
            for i in range (-1, 2, 2):
                try:
                    pos_objetivo: Posicion = self.posicion + Posicion(i, 1) * self.direccion #type:ignore
                    print(f"{self.posicion}, {pos_objetivo}")
                    if self.tablero.comprobar_posicion(pos_objetivo) == 0:
                        print("True")
                        return True
                except IndexError:
                    continue
        print("False")
        return False
    
    def reportar_posicion(self) -> None:
        self.tablero.actualizar_tablero(self.posicion, self.jugador)
    
    def calcular_movimientos(self) -> str:
        if not self.promocionado:
            for i in range (-1, 2, 2):
                try:
                    pos_objetivo: Posicion = self.posicion + Posicion(i, 1) * self.direccion #type:ignore
                    print(f"{self.posicion}, {pos_objetivo}")
                    if self.tablero.comprobar_posicion(pos_objetivo) == 0:
                        print("True")
                        return True
                except IndexError:
                    continue
    
if __name__ == "__main__":
    pieza1 = Pieza(Posicion(1, 1), 1, Tablero())
    print(pieza1.comprobar_movibilidad())