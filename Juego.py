from Pieza import Pieza
from Tablero import Tablero
from Vector import Vector
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
            10 : "\033[91mo\033[00m",
            20 : "\033[92mo\033[00m",
            11 : "\033[91mO\033[00m",
            21 : "\033[92mO\033[00m"
        }
        self.vista = Vista(piezas)
        self.turno = 1

    def generar_piezas(self) -> None:
        for i in range (3):
            for j in range(i - 1, 8, 2):
                if j >= 0:
                    self.piezas.append(Pieza(Vector(j, i), 1, self.tablero))

        for i in range (5, 8):
            for j in range(i - 7, 8, 2):
                if j >= 0:
                    self.piezas.append(Pieza(Vector(j, i), 2, self.tablero))

    def jugar(self):
        self.vista.bienvenida()
        self.generar_piezas()
        for pieza in self.piezas:
            pieza.reportar_posicion()
        juego: bool = True
        while juego:
            self.vista.mostrar_tablero(self.tablero.casillas)
            situacion_piezas: list[tuple[Vector, bool]] = []
            for pieza in self.piezas:
                if pieza.jugador == self.turno:
                    situacion_pieza: tuple[bool, bool] = pieza.comprobar_movilidad()
                    if situacion_pieza[0]:
                        situacion_piezas.append((pieza.posicion, situacion_pieza[1]))
            
            if self.comprobar_captura(situacion_piezas):
                i: int = 0
                while i < len(situacion_piezas):
                    if not situacion_piezas[i][1]:
                        del situacion_piezas[i]
                    else:
                        i += 1
            
            piezas_movibles: list[Vector] = []
            for pieza in situacion_piezas:
                piezas_movibles.append(pieza[0])

            
            if len(piezas_movibles) != 0:
                movimiento_elegido: bool = False
                while not movimiento_elegido:
                    pieza_a_mover: str = self.vista.mostrar_piezas_movibles(piezas_movibles)
                    if pieza_a_mover == "abandonar":
                        juego = False
                        break
                    posicion_pieza: Vector = self.tablero.convertir_a_posicion(pieza_a_mover)
                    for pieza in self.piezas:
                        if pieza.posicion == posicion_pieza:
                            posiciones_a_mover: list[str] = pieza.calcular_movimientos()
                            movimiento: str = self.vista.mostrar_movimientos(posiciones_a_mover)
                            if movimiento == "abandonar":
                                juego = False
                                movimiento_elegido = True
                                break
                            if movimiento != "atras":
                                captura, posicion_captura = pieza.mover(movimiento)
                                if captura:
                                    self.captura(posicion_captura)
                                movimiento_elegido = True
                                break

                if juego:
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
        

    def captura(self, posicion: Vector) -> None:
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
    
    def comprobar_captura(self, situacion_piezas: list[tuple[Vector, bool]]) -> bool:
        for pieza in situacion_piezas:
            if pieza[1]:
                return True
        return False

if __name__ == "__main__":
    juego = Juego()
    juego.jugar()
