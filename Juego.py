from Pieza import Pieza
from Tablero import Tablero
from Vector import Vector
from Vista import Vista

class Juego:
    __tablero: Tablero
    __piezas: list[Pieza]
    __vista: Vista
    __turno: int

    def __init__(self) -> None:
        self.__tablero = Tablero()
        self.__piezas = []
        self.__vista = Vista()
        self.__turno = 1

    # Método que genera las piezas iniciales del juego y las coloca en su posición
    def generar_piezas(self) -> None:
        for i in range (3):
            for j in range(i - 1, 8, 2):
                if j >= 0:
                    self.__piezas.append(Pieza(Vector(j, i), 1, self.__tablero))

        for i in range (5, 8):
            for j in range(i - 7, 8, 2):
                if j >= 0:
                    self.__piezas.append(Pieza(Vector(j, i), 2, self.__tablero))

    # Método para gestionar el inicio y los reinicios del juego
    def inicio(self):
        jugar: bool = True

        self.__vista.bienvenida()
        while jugar:
            jugar = self.jugar()

    # Método que gestiona la ejecución del juego
    # Devuelve un bool que indica si la partida debe reiniciarse o no
    def jugar(self) -> bool:
        self.generar_piezas()
        for pieza in self.__piezas:
            pieza.reportar_posicion()
        juego: bool = True
        while juego:
            self.__vista.mostrar_tablero(self.__tablero.casillas)
            situacion_piezas: list[tuple[Vector, bool]] = []

            # Comprobar la movilidad de las piezas del jugador que debe mover
            for pieza in self.__piezas:
                if pieza.jugador == self.__turno:
                    situacion_pieza: tuple[bool, bool] = pieza.comprobar_movilidad()
                    if situacion_pieza[0]:
                        situacion_piezas.append((pieza.posicion, situacion_pieza[1]))
            
            # Si existe la posibilidad de captura, eliminar como piezas movibles aquellas que
            # no puedan capturar
            if self.comprobar_captura(situacion_piezas):
                i: int = 0
                while i < len(situacion_piezas):
                    if not situacion_piezas[i][1]:
                        del situacion_piezas[i]
                    else:
                        i += 1
            
            piezas_movibles: list[Vector] = []

            # Guardar las piezas movibles en una lista
            for pieza in situacion_piezas:
                piezas_movibles.append(pieza[0])

            # Si el jugador puede mover piezas, continúa el juego
            if len(piezas_movibles) != 0:
                movimiento_elegido: bool = False

                # Repite el bucle mientras no se elija un movimiento
                while not movimiento_elegido:
                    pieza_a_mover: str = self.__vista.mostrar_piezas_movibles(piezas_movibles)

                    # Comprueba si el jugador ha decidido abandonar o reiniciar
                    if pieza_a_mover == "abandonar":
                        juego = False
                        break
                    elif pieza_a_mover == "reiniciar":
                        self.reiniciar_juego()
                        return True
                    
                    posicion_pieza: Vector = self.__tablero.convertir_a_posicion(pieza_a_mover)

                    # Busca la pieza a mover en la lista de piezas y genera los movimientos que
                    # puede realizar
                    for pieza in self.__piezas:
                        if pieza.posicion == posicion_pieza:
                            posiciones_a_mover: list[str] = pieza.calcular_movimientos()
                            movimiento: str = self.__vista.mostrar_movimientos(posiciones_a_mover)

                            # Comprueba si el jugador ha decidido abandonar o reiniciar
                            if movimiento == "abandonar":
                                juego = False
                                movimiento_elegido = True
                                break
                            elif pieza_a_mover == "reiniciar":
                                self.reiniciar_juego()
                                return True
                            
                            if movimiento != "atras":
                                captura, posicion_captura = pieza.mover(movimiento)
                                if captura:
                                    self.captura(posicion_captura)
                                movimiento_elegido = True
                                break

                if juego:
                    self.cambiar_turno()
                    juego = self.fin_de_juego()
            # Si el jugador no puede mover ninguna pieza, ha perdido
            else:
                juego = False
        # Una vez el juego ha terminado, se muestra la pantalla de fin de juego
        self.__vista.fin_de_juego(self.__turno)
        return False
    
    def cambiar_turno(self) -> None:
        if self.__turno == 1:
            self.__turno = 2
        else:
            self.__turno = 1        

    # Método para gestionar la captura de una pieza
    # Busca la pieza cuya posición coincida con la posición a capturar y luego la captura
    def captura(self, posicion: Vector) -> None:
        for i in range(len(self.__piezas)):
            if self.__piezas[i].posicion == posicion:
                self.__piezas[i].capturar()
                del self.__piezas[i]
                return
    
    # Método para reiniciar la partida
    # Reinicia las variables del juego a su estado inicial (en __init__())
    def reiniciar_juego(self) -> None:
        self.__tablero = Tablero()
        self.__piezas = []
        self.__vista = Vista()
        self.__turno = 1
    
    # Método que comprueba si el juego ha terminado, es decir, si el jugador
    # que debe mover se ha quedado sin piezas
    def fin_de_juego(self) -> bool:
        for pieza in self.__piezas:
            if pieza.jugador == self.__turno:
                return True
        return False
    
    # Método que comprueba si existe la posibilidad de captura
    def comprobar_captura(self, situacion_piezas: list[tuple[Vector, bool]]) -> bool:
        for pieza in situacion_piezas:
            if pieza[1]:
                return True
        return False

if __name__ == "__main__":
    juego = Juego()
    juego.inicio()
