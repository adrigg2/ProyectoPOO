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
                pos_objetivo: Posicion = self.posicion + Posicion(i, 1) * self.direccion #type:ignore
                no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                if no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) == 0:
                    return True
                elif no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) != self.jugador:
                    pos_objetivo += Posicion(i, 1) * self.direccion #type: ignore
                    no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                    if no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) == 0:
                        return True
        return False
    
    def reportar_posicion(self) -> None:
        self.tablero.actualizar_tablero(self.posicion, self.jugador)
    
    def calcular_movimientos(self) -> list[str]:
        movimientos_validos: list[str] = []
        if not self.promocionado:
            for i in range (-1, 2, 2):
                pos_objetivo: Posicion = self.posicion + Posicion(i, 1) * self.direccion #type:ignore
                no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                if no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) == 0:
                    movimientos_validos.append(self.codificar_posicion(pos_objetivo))
                elif no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) != self.jugador:
                    pos_objetivo += Posicion(i, 1) * self.direccion #type: ignore
                    no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                    if no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) == 0:
                        movimientos_validos.append(self.codificar_posicion(pos_objetivo))
        return movimientos_validos
    
    def codificar_posicion(self, posicion: Posicion) -> str:
        resultado = self.diccionario_columna[posicion.coord_x] + str(posicion.coord_y + 1)
        return resultado
    
    def mover(self, movimiento: str) -> tuple[bool, Posicion]:
        nueva_posicion = self.tablero.convertir_a_posicion(movimiento)
        vieja_posicion = Posicion(self.posicion.coord_x, self.posicion.coord_y)
        self.posicion = nueva_posicion
        self.tablero.actualizar_tablero(self.posicion, self.jugador, vieja_posicion)

        if nueva_posicion != vieja_posicion + Posicion(1, 1) * self.direccion and nueva_posicion != vieja_posicion + Posicion(-1, 1) * self.direccion:
            return True
        else:
            return False, Posicion(0, 0)

    def capturar(self, posicion_capturada: Posicion, direccion: Posicion) -> bool:
        posicion_capturada += Posicion(-1, -1) * self.direccion * Posicion(1, -1) #type:ignore
        if self.posicion == posicion_capturada:
            vieja_posicion = Posicion(self.posicion.coord_x, self.posicion.coord_y)
            self.posicion = Posicion(-1, -1)
            self.tablero.actualizar_tablero(self.posicion, self.jugador, vieja_posicion)
            return True
        return False

if __name__ == "__main__":
    pieza1 = Pieza(Posicion(1, 1), 1, Tablero())
    print(pieza1.comprobar_movibilidad())