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
            self.direccion = Posicion(1, 1)
        elif self.jugador == 2:
            self.direccion = Posicion(1, -1)
    
    def comprobar_movibilidad(self) -> bool:
        if not self.promocionado:
            for i in range (-1, 2, 2):
                try:
                    pos_objetivo: Posicion = self.posicion + Posicion(i, 1) * self.direccion #type:ignore
                    if self.tablero.comprobar_posicion(pos_objetivo) == 0:
                        return True
                except IndexError:
                    continue
        return False
    
    def reportar_posicion(self) -> None:
        self.tablero.actualizar_tablero(self.posicion, self.jugador)
    
    def calcular_movimientos(self) -> list[str]:
        movimientos_validos: list[str] = []
        if not self.promocionado:
            for i in range (-1, 2, 2):
                try:
                    pos_objetivo: Posicion = self.posicion + Posicion(i, 1) * self.direccion #type:ignore
                    if self.tablero.comprobar_posicion(pos_objetivo) == 0:
                        movimientos_validos.append(self.codificar_posicion(pos_objetivo))
                except IndexError:
                    continue
        return movimientos_validos
    
    def codificar_posicion(self, posicion: Posicion) -> str:
        resultado = self.diccionario_columna[posicion.coord_x] + str(posicion.coord_y)
        return resultado
    
if __name__ == "__main__":
    pieza1 = Pieza(Posicion(1, 1), 1, Tablero())
    print(pieza1.comprobar_movibilidad())