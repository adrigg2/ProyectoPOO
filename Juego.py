from Pieza import Pieza
from Tablero import Tablero
from Posicion import Posicion
from Vista import Vista

class Juego:
    tablero: Tablero
    piezas: list[Pieza]
    vista: Vista

    def __init__(self) -> None:
        self.tablero = Tablero()
        self.piezas = []
        self.vista = Vista()

    def generar_piezas(self) -> None:
        for i in range (3):
            for j in range(i - 1, 8, 2):
                if j >= 0:
                    self.piezas.append(Pieza(Posicion(j, i), 2, self.tablero))

        for i in range (5, 8):
            for j in range(i - 7, 8, 2):
                if j >= 0:
                    self.piezas.append(Pieza(Posicion(j, i), 1, self.tablero))
                    
        # self.piezas.append(Pieza(Posicion(1, 0), 2, self.tablero))
        # self.piezas.append(Pieza(Posicion(3, 0), 2, self.tablero))
        # self.piezas.append(Pieza(Posicion(5, 0), 2, self.tablero))
        # self.piezas.append(Pieza(Posicion(7, 0), 2, self.tablero))
        # self.piezas.append(Pieza(Posicion(0, 1), 2, self.tablero))
        # self.piezas.append(Pieza(Posicion(2, 1), 2, self.tablero))
        # self.piezas.append(Pieza(Posicion(4, 1), 2, self.tablero))
        # self.piezas.append(Pieza(Posicion(6, 1), 2, self.tablero))
        # self.piezas.append(Pieza(Posicion(1, 2), 2, self.tablero))
        # self.piezas.append(Pieza(Posicion(3, 2), 2, self.tablero))
        # self.piezas.append(Pieza(Posicion(5, 2), 2, self.tablero))
        # self.piezas.append(Pieza(Posicion(7, 2), 2, self.tablero))

        # self.piezas.append(Pieza(Posicion(0, 7), 1, self.tablero))
        # self.piezas.append(Pieza(Posicion(2, 7), 1, self.tablero))
        # self.piezas.append(Pieza(Posicion(4, 7), 1, self.tablero))
        # self.piezas.append(Pieza(Posicion(6, 7), 1, self.tablero))
        # self.piezas.append(Pieza(Posicion(1, 6), 1, self.tablero))
        # self.piezas.append(Pieza(Posicion(3, 6), 1, self.tablero))
        # self.piezas.append(Pieza(Posicion(5, 6), 1, self.tablero))
        # self.piezas.append(Pieza(Posicion(7, 6), 1, self.tablero))
        # self.piezas.append(Pieza(Posicion(0, 5), 1, self.tablero))
        # self.piezas.append(Pieza(Posicion(2, 5), 1, self.tablero))
        # self.piezas.append(Pieza(Posicion(4, 5), 1, self.tablero))
        # self.piezas.append(Pieza(Posicion(6, 5), 1, self.tablero))

    def inicio(self):
        Vista.bienvenida()

        menu_principal: bool = True

        while menu_principal:
            opcion: int = Vista.menu_principal()
            if opcion == 1:
                Vista.intrucciones()
            elif opcion == 2:
                self.jugar()
            else:
                menu_principal = False

    def jugar(self):
        self.generar_piezas()
        for pieza in self.piezas:
            pieza.reportar_posicion()
        juego: bool = True
        while juego:
            print(self.tablero)
            juego = False


if __name__ == "__main__":
    juego = Juego()
    juego.inicio()
