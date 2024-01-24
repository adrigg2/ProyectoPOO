from Tablero import Tablero
from Posicion import Posicion

class Pieza:
    posicion: Posicion
    promocionado: bool
    jugador: int
    tablero: Tablero

    def __init__(self, posicion: Posicion, jugador: int, tablero: Tablero) -> None:
        self.posicion = posicion
        self.promocionado = False
        self.jugador = jugador
        self.tablero = tablero
    
    def comprobar_movibilidad(self) -> bool:
        if not self.promocionado:
            for i in range (-1, 2, 2):
                pos_objetivo: Posicion = self.posicion + Posicion(i, 1) #type:ignore
                if self.tablero.comprobar_posicion(pos_objetivo) == 0:
                    return True
        return False
    
    def reportar_posicion(self) -> None:
        self.tablero.actualizar_tablero(self.posicion, self.jugador)
    
if __name__ == "__main__":
    pieza1 = Pieza(Posicion(1, 1), 1, Tablero())
    print(pieza1.comprobar_movibilidad())