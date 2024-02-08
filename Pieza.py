from Tablero import Tablero
from Vector import Vector
from math import sqrt

class Pieza:
    posicion: Vector
    direccion: Vector
    dama: bool
    jugador: int
    id: int
    tablero: Tablero
    diccionario_columna: dict[int, str]
    lista_capturas: list[list[Vector]]
    fila_promociones: list[Vector]

    def __init__(self, posicion: Vector, jugador: int, tablero: Tablero) -> None:
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
            self.direccion = Vector(1, 1)
            self.fila_promociones = [Vector(0, 7), Vector(2, 7), Vector(4, 7), Vector(6, 7)]
        elif self.jugador == 2:
            self.direccion = Vector(1, -1)
            self.fila_promociones = [Vector(1, 0), Vector(3, 0), Vector(5, 0), Vector(7, 0)]
    
    def reportar_posicion(self) -> None:
        self.tablero.actualizar_tablero(self.posicion, self.id)

    # Función para comprobar si una pieza puede moverse
    # Devuelve una tupla de booleans, [0] -> Puede moverse, [1] -> Puede capturar
    def comprobar_movilidad(self) -> tuple[bool, bool]:
        movilidad_sin_captura: bool = False
        if not self.dama:
            for i in range (-1, 2, 2):
                pos_objetivo: Vector = self.posicion + Vector(i, 1) * self.direccion #type:ignore
                no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                if no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) == 0:
                    movilidad_sin_captura = True
                elif no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) // 10 != self.jugador:
                    pos_objetivo += Vector(i, 1) * self.direccion #type: ignore
                    no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                    if no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) == 0:
                        return True, True
        else:
            for i in range (-1, -9, -1):
                for j in range (-1, 2, 2):
                    pos_objetivo: Vector = self.posicion + Vector(i, i * j) * self.direccion #type:ignore
                    no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                    if no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) == 0:
                        movilidad_sin_captura = True
                    elif no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) // 10 != self.jugador:
                        pos_objetivo += Vector(i, i * j).normalizar() * sqrt(2) * self.direccion #type: ignore
                        no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                        if no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) == 0:
                            return True, True
            for i in range (1, 9):
                for j in range (-1, 2, 2):
                    pos_objetivo: Vector = self.posicion + Vector(i, i * j) * self.direccion #type:ignore
                    no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                    if no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) == 0:
                        movilidad_sin_captura = True
                    elif no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) // 10 != self.jugador:
                        pos_objetivo += Vector(i, i * j).normalizar() * sqrt(2) * self.direccion #type: ignore
                        no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                        if no_fuera_limites and self.tablero.comprobar_posicion(pos_objetivo) == 0:
                            return True, True
        return movilidad_sin_captura, False
    
    #TODO: Captura multiple
    def calcular_movimientos(self) -> list[str]:
        movimientos_validos: list[str] = []
        self.lista_capturas = []
        if not self.dama:
            for i in range (-1, 2, 2):
                pos_objetivo: Vector = self.posicion + Vector(i, 1) * self.direccion #type:ignore
                posible_movimiento = self.comprobar_posicion(pos_objetivo, i)
                if posible_movimiento != "":
                    movimientos_validos.append(posible_movimiento)
        else:
            for i in range(-1, -9, -1):
                for j in range (-1, 2, 2):
                    pos_objetivo: Vector = self.posicion + Vector(i, i * j) * self.direccion #type:ignore
                    posible_movimiento = self.comprobar_posicion(pos_objetivo, i, i * j)
                    if posible_movimiento != "" and posible_movimiento not in movimientos_validos:
                        movimientos_validos.append(posible_movimiento)

            for i in range(1, 9):
                for j in range (-1, 2, 2):
                    pos_objetivo: Vector = self.posicion + Vector(i, i * j) * self.direccion #type:ignore
                    posible_movimiento = self.comprobar_posicion(pos_objetivo, i, i * j)
                    if posible_movimiento != "" and posible_movimiento not in movimientos_validos:
                        movimientos_validos.append(posible_movimiento)

        if len(self.lista_capturas) != 0 and not self.dama:
            for movimiento in movimientos_validos:
                pos_movimiento: Vector = self.tablero.convertir_a_posicion(movimiento)
                for captura in self.lista_capturas:
                    misma_direccion: bool = (pos_movimiento - self.posicion).coord_x / captura[0].coord_x == (pos_movimiento - self.posicion).coord_y / (captura[0].coord_y * self.direccion.coord_y) #type:ignore
                    if misma_direccion:
                        break
                else:
                    movimientos_validos.remove(movimiento)
        #FIXME: Dama no reporta correctamente las capturas -> Pieza en la misma direccion, dama solo debería capturar por detrás
        elif len(self.lista_capturas) != 0 and self.dama:
            i: int = 0
            while i < len(movimientos_validos):
                pos_movimiento: Vector = self.tablero.convertir_a_posicion(movimientos_validos[i])
                for captura in self.lista_capturas:
                    producto_escalar: float = (pos_movimiento - self.posicion).normalizar().producto_escalar(captura[0].normalizar()) #type:ignore
                    misma_direccion: bool = producto_escalar > 0.999 and producto_escalar < 1.001
                    if misma_direccion:
                        distancia_movimiento = pos_movimiento - self.posicion
                        distancia_captura = captura[1] - self.posicion
                        if distancia_movimiento > distancia_captura: #type:ignore
                            i += 1
                            break
                else:
                    del movimientos_validos[i]
        return movimientos_validos
    
    def comprobar_posicion(self, posicion: Vector, incremento_x: int, incremento_y: int = 1) -> str:
        no_fuera_limites: bool = posicion.coord_x >= 0 and posicion.coord_x < 8 and posicion.coord_y >= 0 and posicion.coord_y < 8
        if no_fuera_limites and self.tablero.comprobar_posicion(posicion) == 0:
            return self.codificar_posicion(posicion)
        elif no_fuera_limites and self.tablero.comprobar_posicion(posicion) // 10 != self.jugador:
            pos_captura: Vector = posicion.__copy__() #type:ignore
            posicion += Vector(incremento_x, incremento_y).normalizar() * sqrt(2) * self.direccion #type: ignore
            no_fuera_limites: bool = posicion.coord_x >= 0 and posicion.coord_x < 8 and posicion.coord_y >= 0 and posicion.coord_y < 8
            if no_fuera_limites and self.tablero.comprobar_posicion(posicion) == 0:
                self.lista_capturas.append([Vector(incremento_x, incremento_y).normalizar() * sqrt(2), pos_captura.__copy__()]) #type:ignore
                return self.codificar_posicion(posicion)
        return ""
    
    def codificar_posicion(self, posicion: Vector) -> str:
        resultado = self.diccionario_columna[int(posicion.coord_x)] + str(int(posicion.coord_y) + 1)
        return resultado
    
    def mover(self, movimiento: str) -> tuple[bool, Vector]:
        nueva_posicion = self.tablero.convertir_a_posicion(movimiento)
        vieja_posicion = Vector(self.posicion.coord_x, self.posicion.coord_y)
        self.posicion = nueva_posicion

        if self.posicion in self.fila_promociones:
            self.promocionar()
        
        self.tablero.actualizar_tablero(self.posicion, self.id, vieja_posicion)

        for captura in self.lista_capturas:
            proporcion_x: float = (nueva_posicion - vieja_posicion).coord_x / captura[0].coord_x #type:ignore
            proporcion_y: float = (nueva_posicion - vieja_posicion).coord_y / (captura[0].coord_y * self.direccion.coord_y) #type:ignore
            if proporcion_x == proporcion_y:
                return True, captura[1]
        
        return False, Vector(-1, -1)

    def capturar(self) -> None:
        vieja_posicion = Vector(self.posicion.coord_x, self.posicion.coord_y)
        self.posicion = Vector(-1, -1)
        self.tablero.actualizar_tablero(self.posicion, self.id, vieja_posicion)
    
    def promocionar(self) -> None:
        self.dama = True
        self.id += 1

if __name__ == "__main__":
    pieza1 = Pieza(Vector(1, 1), 1, Tablero())
    print(pieza1.comprobar_movilidad())