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
    def inicio(self) -> None:
        menu_inicio: bool = True
        jugar: bool = False

        self.__vista.bienvenida()

        while menu_inicio:
            try:
                opcion_elegida: int = self.__vista.menu_inicio()
                if opcion_elegida == 1:
                    jugar = True
                    menu_inicio = False
                elif opcion_elegida == 2:
                    if self.cargar_partida():
                        jugar = True
                        menu_inicio = False
                elif opcion_elegida == 3:
                    menu_inicio = False
            except:
                print("La opción elegida no es correcta.")

        while jugar:
            jugar = self.jugar()

    # Método que gestiona la ejecución del juego
    # Devuelve un bool que indica si la partida debe reiniciarse o no
    def jugar(self) -> bool:
        if not self.__piezas:
            self.generar_piezas()
        for pieza in self.__piezas:
            pieza.reportar_posicion()
        juego: bool = True
        partida_guardada: bool = False
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
            if piezas_movibles:
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
                    elif pieza_a_mover == "guardar":
                        self.guardar_partida()
                        juego = False
                        partida_guardada = True
                        break
                    
                    posicion_pieza: Vector = self.__tablero.convertir_a_posicion(pieza_a_mover)

                    # Busca la pieza a mover en la lista de piezas y genera los movimientos que
                    # puede realizar
                    for pieza in self.__piezas:
                        if pieza.posicion == posicion_pieza:
                            continuar_captura: bool = True
                            primer_movimiento: bool = True
                            while continuar_captura:
                                posiciones_a_mover: list[str] = pieza.calcular_movimientos()
                                movimiento: str = self.__vista.mostrar_movimientos(posiciones_a_mover, primer_movimiento)

                                # Comprueba si el jugador ha decidido abandonar o reiniciar
                                if movimiento == "abandonar":
                                    juego = False
                                    movimiento_elegido = True
                                    break
                                elif movimiento == "reiniciar":
                                    self.reiniciar_juego()
                                    return True
                                elif movimiento == "guardar":
                                    self.guardar_partida()
                                    juego = False
                                    movimiento_elegido = True
                                    partida_guardada = True
                                    break
                                
                                if movimiento != "atras":
                                    captura: bool
                                    posicion_captura: Vector
                                    captura, posicion_captura = pieza.mover(movimiento)
                                    primer_movimiento = False
                                    if captura:
                                        self.captura(posicion_captura)
                                        continuar_captura = pieza.comprobar_movilidad()[1]
                                    else:
                                        continuar_captura = False
                                    movimiento_elegido = True
                                else:
                                    continuar_captura = False
                            break

                if juego:
                    self.cambiar_turno()
                    juego = self.fin_de_juego()
            # Si el jugador no puede mover ninguna pieza, ha perdido
            else:
                juego = False
        # Una vez el juego ha terminado, se muestra la pantalla de fin de juego (solo si no se ha reiniciado)
        if not partida_guardada:
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
    
    # Método que gestiona el guardado de la partida
    # Guarda las casillas del tablero en su forma de int y el turno al final marcado con una T
    def guardar_partida(self) -> None:
        with open("partida_guardada.txt", "w", encoding="utf-8") as archivo_guardado:
            archivo_guardado.close()

            archivo_guardado = open("partida_guardada.txt", "a", encoding="utf-8")

            casillas_tablero: list[str] = []

            for i in range(len(self.__tablero.casillas)):
                fila = "· "
                for j in range(len(self.__tablero.casillas[i])):
                    fila += str(self.__tablero.casillas[i][j]) + " "
                fila += "\n"
                casillas_tablero.append(fila)

            archivo_guardado.writelines(casillas_tablero)
            archivo_guardado.write(f"\nT {self.__turno}")

    # Método que gestiona la carga de una partida guardada
    # Lee linea a linea el archivo guardado para recojer el estado de las casillas y el turno
    def cargar_partida(self) -> bool:
        try:
            with open("partida_guardada.txt", "r", encoding="utf-8") as archivo_guardado:
                num_filas: int = 0
                casillas_guardadas: list[list[int]] = []
                for linea in archivo_guardado:
                    if "·" in linea:
                        num_filas += 1
                        casillas_guardadas.append([int(i) for i in linea.lstrip("·").split()])
                    elif "T" in linea:
                        self.__turno = int(linea[-1])
                if num_filas != 8:
                    raise Exception("El número de filas guardadas no son las que deberían.")
                
                self.__tablero = Tablero(casillas_guardadas)

                for i, linea in enumerate(casillas_guardadas):
                    for j, casilla in enumerate(linea):
                        if casilla == 10:
                            pieza: Pieza = Pieza(Vector(j, i), casilla // 10, self.__tablero)
                            self.__piezas.append(pieza)
                        elif casilla == 11:
                            pieza: Pieza = Pieza(Vector(j, i), casilla // 10, self.__tablero, True)
                            self.__piezas.append(pieza)
                        elif casilla == 20:
                            pieza: Pieza = Pieza(Vector(j, i), casilla // 10, self.__tablero)
                            self.__piezas.append(pieza)
                        elif casilla == 21:
                            pieza: Pieza = Pieza(Vector(j, i), casilla // 10, self.__tablero, True)
                            self.__piezas.append(pieza)
            return True

        except FileNotFoundError:
            print("\nNo hay ninguna partida guardada.\n")
            return False
        except Exception:
            print("\nEl archivo está corrupto.\n")
            return False

if __name__ == "__main__":
    juego = Juego()
    juego.inicio()
