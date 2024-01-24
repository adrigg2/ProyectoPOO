from Pieza import Pieza
from Tablero import Tablero
from Posicion import Posicion
from Vista import Vista

class Juego:
    tablero: Tablero
    piezas: list[Pieza]
    vista: Vista
    turno: int

    def __init__(self) -> None:
        self.tablero = Tablero()
        self.piezas = []

        piezas = {
            1 : "\033[91mo\033[00m",
            2 : "\033[92mo\033[00m"
        }
        self.vista = Vista(piezas)
        self.turno = 1

    def generar_piezas(self) -> None:
        for i in range (3):
            for j in range(i - 1, 8, 2):
                if j >= 0:
                    self.piezas.append(Pieza(Posicion(j, i), 2, self.tablero))

        for i in range (5, 8):
            for j in range(i - 7, 8, 2):
                if j >= 0:
                    self.piezas.append(Pieza(Posicion(j, i), 1, self.tablero))

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
            self.vista.mostrar_tablero(self.tablero.casillas)
            piezas_movibles: list[Posicion] = []
            for pieza in self.piezas:
                if pieza.jugador == self.turno:
                    if pieza.comprobar_movibilidad():
                        piezas_movibles.append(pieza.posicion)
            print(self.tablero)
            self.vista.mostrar_piezas_movibles(piezas_movibles)

            juego = False


if __name__ == "__main__":
    juego = Juego()
    juego.inicio()
