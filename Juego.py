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
                    self.piezas.append(Pieza(Posicion(j, i), 1, self.tablero))

        for i in range (5, 8):
            for j in range(i - 7, 8, 2):
                if j >= 0:
                    self.piezas.append(Pieza(Posicion(j, i), 2, self.tablero))

    def inicio(self):
        self.vista.bienvenida()

        menu_principal: bool = True

        while menu_principal:
            opcion: int = self.vista.menu_principal()
            if opcion == 1:
                self.vista.intrucciones()
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
            pieza_a_mover: str = self.vista.mostrar_piezas_movibles(piezas_movibles)
            posicion_pieza: Posicion = self.tablero.convertir_a_posicion(pieza_a_mover)

            if len(piezas_movibles) != 0:
                for pieza in self.piezas:
                    if pieza.posicion == posicion_pieza:
                        posiciones_a_mover: list[str] = pieza.calcular_movimientos()
                        movimiento: str = self.vista.mostrar_movimientos(posiciones_a_mover)
                        captura, posicion_captura = pieza.mover(movimiento)
                        if captura:
                            self.captura(posicion_captura)
                        break

                self.cambiar_turno()
                juego = self.fin_de_juego()
            else:
                juego = False
        self.vista.fin_de_juego(self.turno)
    
    def cambiar_turno(self) -> None:
        if self.turno == 1:
            self.turno = 2
        else:
            self.turno = 1
        

    def captura(self, posicion: Posicion) -> None:
        for pieza in self.piezas:
            if pieza.posicion == posicion:
                pieza.capturar()
                self.piezas.remove(pieza)
                return
            
    def fin_de_juego(self) -> bool:
        for pieza in self.piezas:
            if pieza.jugador == self.turno:
                return True
        return False

if __name__ == "__main__":
    juego = Juego()
    juego.inicio()
