from Tablero import Tablero
from Posicion import Posicion

class Pieza:
    posicion: Posicion
    direccion: Posicion
    dama: bool
    jugador: int
    id: int
    tablero: Tablero
    diccionario_columna: dict[int, str]
    lista_capturas: list[list[Posicion]]
    fila_promociones: list[Posicion]

    def __init__(self, posicion: Posicion, jugador: int, tablero: Tablero) -> None:
        self.posicion = posicion
        self.dama = False
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
        self.lista_capturas = []
        self.id = self.jugador * 10

        if self.jugador == 1:
            self.direccion = Posicion(1, 1)
            self.fila_promociones = [Posicion(0, 7), Posicion(2, 7), Posicion(4, 7), Posicion(6, 7)]
        elif self.jugador == 2:
            self.direccion = Posicion(1, -1)
            self.fila_promociones = [Posicion(1, 0), Posicion(3, 0), Posicion(5, 0), Posicion(7, 0)]
    
    def reportar_posicion(self) -> None:
        self.tablero.actualizar_tablero(self.posicion, self.id)

    # Función para comprobar si una pieza puede moverse
    # Devuelve una tupla de booleans, [0] -> Puede moverse, [1] -> Puede capturar
    def comprobar_movilidad(self) -> tuple[bool, bool]:
        if not self.dama:
            for i in range (-1, 2, 2):
                pos_objetivo: Posicion = self.posicion + Posicion(i, 1) * self.direccion #type:ignore
                no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                if no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) == 0:
                    return True, False
                elif no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) // 10 != self.jugador:
                    pos_objetivo += Posicion(i, 1) * self.direccion #type: ignore
                    no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                    if no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) == 0:
                        return True, True
        else:
            for i in range (-1, 1, 2):
                for j in range (-1, 2, 2):
                    pos_objetivo: Posicion = self.posicion + Posicion(i, i * j) * self.direccion #type:ignore
                    no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                    if no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) == 0:
                        return True, False
                    elif no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) // 10 != self.jugador:
                        pos_objetivo += Posicion(i, j) * self.direccion #type: ignore
                        no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                        if no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) == 0:
                            return True, True
        return False, False
    
    def calcular_movimientos(self) -> list[str]:
        movimientos_validos: list[str] = []
        self.lista_capturas = []
        if not self.dama:
            for i in range (-1, 2, 2):
                pos_objetivo: Posicion = self.posicion + Posicion(i, 1) * self.direccion #type:ignore
                posible_movimiento = self.comprobar_posicion(pos_objetivo, i)
                if posible_movimiento != "":
                    movimientos_validos.append(posible_movimiento)
        else:
            for i in range(-1, -9, -1):
                for j in range (-1, 1, 2):
                    pos_objetivo: Posicion = self.posicion + Posicion(i, i * j) * self.direccion #type:ignore
                    posible_movimiento = self.comprobar_posicion(pos_objetivo, i, i * j)
                    if posible_movimiento != "":
                        movimientos_validos.append(posible_movimiento)

            for i in range(1, 9):
                for j in range (-1, 1, 2):
                    pos_objetivo: Posicion = self.posicion + Posicion(i, i * j) * self.direccion #type:ignore
                    posible_movimiento = self.comprobar_posicion(pos_objetivo, i, i * j)
                    if posible_movimiento != "":
                        movimientos_validos.append(posible_movimiento)

        if len(self.lista_capturas) != 0:
            for movimiento in movimientos_validos:
                pos_movimiento: Posicion = self.tablero.convertir_a_posicion(movimiento)
                for captura in self.lista_capturas:
                    if (pos_movimiento - self.posicion).coord_x / captura[0].coord_x == (pos_movimiento - self.posicion).coord_y / (captura[0].coord_y * self.direccion.coord_y): #type:ignore
                        break
                else:
                    movimientos_validos.remove(movimiento)
        return movimientos_validos
    
    def comprobar_posicion(self, posicion: Posicion, incremento_x: int, incremento_y: int = 1) -> str:
        no_fuera_limites: bool = posicion.coord_x >= 0 and posicion.coord_x < 8 and posicion.coord_y >= 0 and posicion.coord_y < 8
        if no_fuera_limites and self.tablero.comprobar_posicion(posicion) == 0:
            return self.codificar_posicion(posicion)
        elif no_fuera_limites and self.tablero.comprobar_posicion(posicion) // 10 != self.jugador:
            pos_captura: Posicion = posicion.__copy__() #type:ignore
            posicion += Posicion(incremento_x, incremento_y) * self.direccion #type: ignore
            no_fuera_limites: bool = posicion.coord_x >= 0 and posicion.coord_x < 8 and posicion.coord_y >= 0 and posicion.coord_y < 8
            if no_fuera_limites and self.tablero.comprobar_posicion(posicion) == 0:
                self.lista_capturas.append([Posicion(incremento_x, incremento_y), pos_captura.__copy__()]) #type:ignore
                return self.codificar_posicion(posicion)
        return ""
    
    def codificar_posicion(self, posicion: Posicion) -> str:
        resultado = self.diccionario_columna[posicion.coord_x] + str(posicion.coord_y + 1)
        return resultado
    
    def mover(self, movimiento: str) -> tuple[bool, Posicion]:
        nueva_posicion = self.tablero.convertir_a_posicion(movimiento)
        vieja_posicion = Posicion(self.posicion.coord_x, self.posicion.coord_y)
        self.posicion = nueva_posicion

        if self.posicion in self.fila_promociones:
            self.promocionar()
        
        self.tablero.actualizar_tablero(self.posicion, self.id, vieja_posicion)

        for captura in self.lista_capturas:
            print("Intentando captura")
            if (nueva_posicion - vieja_posicion).coord_x / captura[0].coord_x == (nueva_posicion - vieja_posicion).coord_y / (captura[0].coord_y * self.direccion.coord_y): #type:ignore
                print("Captura")
                return True, captura[1]
        
        return False, Posicion(-1, -1)

    def capturar(self) -> None:
        vieja_posicion = Posicion(self.posicion.coord_x, self.posicion.coord_y)
        self.posicion = Posicion(-1, -1)
        self.tablero.actualizar_tablero(self.posicion, self.id, vieja_posicion)
    
    def promocionar(self) -> None:
        self.dama = True
        self.id += 1

if __name__ == "__main__":
    pieza1 = Pieza(Posicion(1, 1), 1, Tablero())
    print(pieza1.comprobar_movilidad())