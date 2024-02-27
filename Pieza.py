from Tablero import Tablero
from Vector import Vector
from math import sqrt

class Pieza:
    __posicion: Vector
    __direccion: Vector
    __dama: bool
    __jugador: int
    __id: int
    __tablero: Tablero
    __lista_capturas: list[list[Vector]]
    __fila_promociones: list[Vector]

    @property
    def posicion(self):
        return self.__posicion
    
    @property
    def jugador(self):
        return self.__jugador
    
    @property
    def fila_promociones(self):
        return self.__fila_promociones

    def __init__(self, posicion: Vector, jugador: int, tablero: Tablero, dama: bool = False) -> None:
        self.__posicion = posicion
        self.__dama = dama
        self.__jugador = jugador
        self.__tablero = tablero
        self.__lista_capturas = []

        if not self.__dama:
            self.__id = self.__jugador * 10
        else:
            self.__id = self.__jugador * 10 + 1

        if self.__jugador == 1:
            self.__direccion = Vector(1, 1)
            self.__fila_promociones = [Vector(0, 7), Vector(2, 7), Vector(4, 7), Vector(6, 7)]
        elif self.__jugador == 2:
            self.__direccion = Vector(1, -1)
            self.__fila_promociones = [Vector(1, 0), Vector(3, 0), Vector(5, 0), Vector(7, 0)]
    
    # Método para reportar al tablero la posición inicial de la pieza
    def reportar_posicion(self) -> None:
        self.__tablero.actualizar_tablero(self.__posicion, self.__id)

    # Método para comprobar si una pieza puede moverse
    # Devuelve una tupla de bools, [0] -> Puede moverse, [1] -> Puede capturar
    def comprobar_movilidad(self) -> tuple[bool, bool]:
        movilidad_sin_captura: bool = False

        # Si no es dama, comprueba las casillas a 1 posición de distancia en diagonal hacia delante
        if not self.__dama:
            for i in range (-1, 2, 2):
                pos_objetivo: Vector = self.__posicion + Vector(i, 1) * self.__direccion #type:ignore
                no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                if no_fuera_limites and self.__tablero.comprobar_posicion(pos_objetivo) == 0:
                    movilidad_sin_captura = True
                elif no_fuera_limites and self.__tablero.comprobar_posicion(pos_objetivo) // 10 != self.__jugador:
                    pos_objetivo += Vector(i, 1) * self.__direccion #type: ignore
                    no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                    if no_fuera_limites and self.__tablero.comprobar_posicion(pos_objetivo) == 0:
                        return True, True
                    
        #Si es dama, comprueba todas las casillas en diagonal
        else:
            for i in range(-1, 2, 2):
                for j in range(-1, -9, -1):
                    pos_objetivo: Vector = self.__posicion + Vector(j, j * i) * self.__direccion #type:ignore
                    no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                    if no_fuera_limites and self.__tablero.comprobar_posicion(pos_objetivo) == 0:
                        movilidad_sin_captura = True
                    elif no_fuera_limites and self.__tablero.comprobar_posicion(pos_objetivo) // 10 != self.__jugador:
                        pos_objetivo += Vector(j, j * i).normalizar() * sqrt(2) * self.__direccion #type: ignore
                        no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                        if no_fuera_limites and self.__tablero.comprobar_posicion(pos_objetivo) == 0:
                            return True, True
                        else:
                            break
            
            for i in range(-1, 2, 2):
                for j in range(1, 9):
                    pos_objetivo: Vector = self.__posicion + Vector(j, j * i) * self.__direccion #type:ignore
                    no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                    if no_fuera_limites and self.__tablero.comprobar_posicion(pos_objetivo) == 0:
                        movilidad_sin_captura = True
                    elif no_fuera_limites and self.__tablero.comprobar_posicion(pos_objetivo) // 10 != self.__jugador:
                        pos_objetivo += Vector(j, j * i).normalizar() * sqrt(2) * self.__direccion #type: ignore
                        no_fuera_limites: bool = pos_objetivo.coord_x >= 0 and pos_objetivo.coord_x < 8 and pos_objetivo.coord_y >= 0 and pos_objetivo.coord_y < 8
                        if no_fuera_limites and self.__tablero.comprobar_posicion(pos_objetivo) == 0:
                            return True, True
                        else:
                            break

        return movilidad_sin_captura, False
    
    # Método para calcular los movimientos posibles de la pieza y devolverlos como una lista de strings
    def calcular_movimientos(self) -> list[str]:
        # Función para comprobar si una posición está libre, ocupada por una pieza aliada o ocupada por una enemiga
        # Devuelve una cadena vacía si la posición está ocupada por una pieza enemiga que no se puede capturar
        # Devuelve una posición como cadena si la posición está disponible y un bool que indica si hay una captura
        def comprobar_posicion(posicion: Vector, incremento_x: int, incremento_y: int = 1, hay_captura: bool = False) -> tuple[str, bool]:
            no_fuera_limites: bool = posicion.coord_x >= 0 and posicion.coord_x < 8 and posicion.coord_y >= 0 and posicion.coord_y < 8
            if no_fuera_limites and self.__tablero.comprobar_posicion(posicion) == 0:
                return self.__tablero.codificar_posicion(posicion), hay_captura
            
            # Si la casilla está ocupada por una pieza enemiga, comprueba si la siguiente está vacía y, por tanto
            # si se puede capturar.
            elif no_fuera_limites and self.__tablero.comprobar_posicion(posicion) // 10 != self.__jugador and not hay_captura:
                pos_captura: Vector = posicion.__copy__() #type:ignore
                posicion += Vector(incremento_x, incremento_y).normalizar() * sqrt(2) * self.__direccion #type: ignore
                no_fuera_limites: bool = posicion.coord_x >= 0 and posicion.coord_x < 8 and posicion.coord_y >= 0 and posicion.coord_y < 8
                if no_fuera_limites and self.__tablero.comprobar_posicion(posicion) == 0:
                    self.__lista_capturas.append([Vector(incremento_x, incremento_y).normalizar() * sqrt(2), pos_captura.__copy__()]) #type:ignore
                    hay_captura = True
                    return self.__tablero.codificar_posicion(posicion), hay_captura
            return "", hay_captura
        
        movimientos_validos: list[str] = []
        self.__lista_capturas = []

        # Si no es dama, comprueba las casillas a 1 posición de distancia en diagonal hacia delante
        if not self.__dama:
            for i in range (-1, 2, 2):
                pos_objetivo: Vector = self.__posicion + Vector(i, 1) * self.__direccion #type:ignore
                posible_movimiento = comprobar_posicion(pos_objetivo, i)[0]
                if posible_movimiento != "":
                    movimientos_validos.append(posible_movimiento)

        #Si es dama, comprueba todas las casillas en diagonal
        else:
            hay_captura: bool = False
            for i in range(-1, 2, 2):
                hay_captura = False
                for j in range(-1, -9, -1):
                    pos_objetivo: Vector = self.__posicion + Vector(j, j * i) * self.__direccion #type:ignore
                    posible_movimiento, hay_captura = comprobar_posicion(pos_objetivo, j, j * i, hay_captura)
                    if posible_movimiento != "" and posible_movimiento not in movimientos_validos:
                        movimientos_validos.append(posible_movimiento)
                    elif posible_movimiento == "":
                        break

            for i in range(-1, 2, 2):
                hay_captura = False
                for j in range(1, 9):
                    pos_objetivo: Vector = self.__posicion + Vector(j, j * i) * self.__direccion #type:ignore
                    posible_movimiento, hay_captura = comprobar_posicion(pos_objetivo, j, j * i, hay_captura)
                    if posible_movimiento != "" and posible_movimiento not in movimientos_validos:
                        movimientos_validos.append(posible_movimiento)
                    elif posible_movimiento == "":
                        break

        # Si existe la posibilidad de captura, elimina los movimientos que no impliquen una captura
        if self.__lista_capturas and not self.__dama:
            i: int = 0
            while i < len(movimientos_validos):
                pos_movimiento: Vector = self.__tablero.convertir_a_posicion(movimientos_validos[i])
                for captura in self.__lista_capturas:
                    misma_direccion: bool = (pos_movimiento - self.__posicion).coord_x / captura[0].coord_x == (pos_movimiento - self.__posicion).coord_y / (captura[0].coord_y * self.__direccion.coord_y) #type:ignore
                    if misma_direccion:
                        i += 1
                        break
                else:
                    del movimientos_validos[i]        
        elif self.__lista_capturas and self.__dama:
            i: int = 0
            while i < len(movimientos_validos):
                pos_movimiento: Vector = self.__tablero.convertir_a_posicion(movimientos_validos[i])
                for captura in self.__lista_capturas:
                    producto_escalar: float = (pos_movimiento - self.__posicion).normalizar().producto_escalar(captura[0].normalizar() * self.__direccion) #type:ignore
                    misma_direccion: bool = producto_escalar > 0.999 and producto_escalar < 1.001
                    if misma_direccion:
                        distancia_movimiento = pos_movimiento - self.__posicion
                        distancia_captura = captura[1] - self.__posicion
                        if distancia_movimiento > distancia_captura: #type:ignore
                            i += 1
                            break
                else:
                    del movimientos_validos[i]
        return movimientos_validos
    
    # Método para mover la pieza, devuelve una tupla de un bool y un vector
    # [0] -> Está capturando    [1] -> Posición a capturar 
    def mover(self, movimiento: str) -> tuple[bool, Vector]:
        nueva_posicion = self.__tablero.convertir_a_posicion(movimiento)
        vieja_posicion = Vector(self.__posicion.coord_x, self.__posicion.coord_y)
        self.__posicion = nueva_posicion

        # Si la pieza alcanza el final del tablero y no es una dama, promociona a dama
        if self.__posicion in self.__fila_promociones and not self.__dama:
            self.promocionar()
        
        self.__tablero.actualizar_tablero(self.__posicion, self.__id, vieja_posicion)

        for captura in self.__lista_capturas:
            proporcion_x: float = (nueva_posicion - vieja_posicion).coord_x / captura[0].coord_x #type:ignore
            proporcion_y: float = (nueva_posicion - vieja_posicion).coord_y / (captura[0].coord_y * self.__direccion.coord_y) #type:ignore
            if proporcion_x == proporcion_y:
                return True, captura[1]
        
        return False, Vector(-1, -1)

    # Método para capturar la pieza y eliminarla del tablero
    def capturar(self) -> None:
        vieja_posicion = Vector(self.__posicion.coord_x, self.__posicion.coord_y)
        self.__posicion = Vector(-1, -1)
        self.__tablero.actualizar_tablero(self.__posicion, self.__id, vieja_posicion)
    
    # Método para promocionar la pieza a dama. Incrementa su id en 1 para facilitar su representación
    # en el tablero
    def promocionar(self) -> None:
        self.__dama = True
        self.__id += 1

if __name__ == "__main__":
    pieza1 = Pieza(Vector(1, 1), 1, Tablero())
    print(pieza1.comprobar_movilidad())