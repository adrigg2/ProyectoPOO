from Pieza import Pieza
from Tablero import Tablero
from Vector import Vector
from Vista import Vista
from Excepciones import ArchivoCorruptoError, OpcionNoValidaError

class Juego:
    ABANDONAR = 1
    REINICIAR = 2
    GUARDAR = 3
    __tablero: Tablero
    __piezas: dict[int, Pieza]
    __vista: Vista
    __turno: int

    def __init__(self) -> None:
        self.__tablero = Tablero()
        self.__piezas = {}
        self.__vista = Vista()
        self.__turno = 1

    # Método que genera las piezas iniciales del juego y las coloca en su posición
    def generar_piezas(self) -> None:
        for i in range (3):
            for j in range(i - 1, 8, 2):
                if j >= 0:
                    pieza: Pieza = Pieza(Vector(j, i), 1, self.__tablero)
                    self.__piezas.update({pieza.id : pieza})

        for i in range (5, 8):
            for j in range(i - 7, 8, 2):
                if j >= 0:
                    pieza: Pieza = Pieza(Vector(j, i), 2, self.__tablero)
                    self.__piezas.update({pieza.id : pieza})

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
            except OpcionNoValidaError:
                print("La opción elegida no es correcta.")

        while jugar:
            jugar = self.jugar()

    # Método que gestiona la ejecución del juego
    # Devuelve un bool que indica si la partida debe reiniciarse o no
    def jugar(self) -> bool:
        if not self.__piezas:
            self.generar_piezas()
        for pieza in self.__piezas.values():
            pieza.reportar_posicion()
        juego: bool = True
        partida_guardada: bool = False
        while juego:
            situacion_piezas: list[tuple[Vector, bool]] = []

            # Comprobar la movilidad de las piezas del jugador que debe mover
            for pieza in self.__piezas.values():
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
            
            piezas_movibles: list[Vector] = [i[0] for i in situacion_piezas]
            
            if piezas_movibles:
                resultado_movimiento: int = self.elegir_movimiento(piezas_movibles)

                if resultado_movimiento == Juego.ABANDONAR:
                    juego = False
                elif resultado_movimiento == Juego.REINICIAR:
                    self.reiniciar_juego()
                    return True
                elif resultado_movimiento == Juego.GUARDAR:
                    self.guardar_partida()
                    juego = False
                    partida_guardada = True
                
                if juego:
                    self.cambiar_turno()
                    juego = self.fin_de_juego()
            # Si el jugador no puede mover ninguna pieza, ha perdido
            else:
                juego = False
        if not partida_guardada:
            self.__vista.fin_de_juego(self.__turno)
            if self.__vista.reiniciar().lower() == "s":
                return True
        return False
    
    # Método que gestiona la selección de un movimiento. Recibe la lista de posibles piezas a mover y
    # devuelve 0 si el movimiento es exitoso o las constantes ABANDONAR, REINICIAR o GUARDAR en otro caso
    def elegir_movimiento(self, piezas_movibles) -> int:
        movimiento_elegido: bool = False

        while not movimiento_elegido:            
            self.__vista.mostrar_tablero(self.__tablero.casillas, self.__turno, piezas_movibles)
            pieza_a_mover: str = self.__vista.mostrar_piezas_movibles(piezas_movibles, self.__turno)

            if pieza_a_mover == "abandonar":
                return Juego.ABANDONAR
            elif pieza_a_mover == "reiniciar":
                return Juego.REINICIAR
            elif pieza_a_mover == "guardar":
                return Juego.GUARDAR
            
            posicion_pieza: Vector = self.__tablero.convertir_a_posicion(pieza_a_mover)
            id_pieza: int = self.__tablero.comprobar_posicion(posicion_pieza) % 100
            pieza: Pieza = self.__piezas[id_pieza]

            continuar_captura: bool = True
            primer_movimiento: bool = True
            while continuar_captura:
                posiciones_a_mover: list[str] = pieza.calcular_movimientos()
                posiciones_a_marcar = [self.__tablero.convertir_a_posicion(i) for i in posiciones_a_mover]
                self.__vista.mostrar_tablero(self.__tablero.casillas, self.__turno, posiciones_a_marcar)
                movimiento: str = self.__vista.mostrar_movimientos(posiciones_a_mover, primer_movimiento)

                if movimiento == "abandonar":
                    return Juego.ABANDONAR
                elif movimiento == "reiniciar":
                    return Juego.REINICIAR
                elif movimiento == "guardar":
                    return Juego.GUARDAR
                
                if movimiento != "atras":
                    captura: bool
                    posicion_captura: int
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
        return 0

    
    # Método para cambiar el turno
    def cambiar_turno(self) -> None:
        if self.__turno == 1:
            self.__turno = 2
        else:
            self.__turno = 1        

    # Método para gestionar la captura de una pieza
    # Busca la pieza cuya posición coincida con la posición a capturar y luego la captura
    def captura(self, id: int) -> None:
        self.__piezas[id].capturar()
        self.__piezas.pop(id)
    
    # Método para reiniciar la partida
    # Reinicia las variables del juego a su estado inicial (en __init__())
    def reiniciar_juego(self) -> None:
        self.__tablero = Tablero()
        self.__piezas = {}
        self.__vista = Vista()
        self.__turno = 1
    
    # Método que comprueba si el juego ha terminado, es decir, si el jugador
    # que debe mover se ha quedado sin piezas
    def fin_de_juego(self) -> bool:
        for pieza in self.__piezas.values():
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
    # Guarda las casillas del tablero en su forma de int con un · para marcar cada fila y el turno al final marcado con una T
    def guardar_partida(self) -> None:
        archivo_guardado = open("partida_guardada.save", "w", encoding="utf-8")
        archivo_guardado.close()

        with open("partida_guardada.save", "a", encoding="utf-8") as archivo_guardado:
            casillas_tablero: list[str] = []

            for i in range(len(self.__tablero.casillas)):
                fila = "· "
                for j in range(len(self.__tablero.casillas[i])):
                    fila += f"{self.__tablero.casillas[i][j] // 100:4}"
                fila += "\n"
                casillas_tablero.append(fila)

            archivo_guardado.writelines(casillas_tablero)
            archivo_guardado.write(f"\nT {self.__turno}")

    # Método que gestiona la carga de una partida guardada
    # Lee linea a linea el archivo guardado para recojer el estado de las casillas y el turno
    def cargar_partida(self) -> bool:
        carga_finalizada: bool = False
        carga_exitosa: bool = False
        while not carga_finalizada:
            try:
                with open("partida_guardada.save", "r", encoding="utf-8") as archivo_guardado:
                    self.__turno = 0
                    casillas_guardadas: list[list[int]] = []
                    casillas_validas: list[int] = [0, 10, 11, 20, 21]
                    for linea in archivo_guardado:
                        if "·" in linea:
                            casillas_guardadas.append([int(i) for i in linea.lstrip("·").split() if i.isnumeric() and int(i) in casillas_validas])
                        elif "T" in linea:
                            try:
                                self.__turno = int(linea.rstrip("\n")[-1])
                            except ValueError:
                                raise ArchivoCorruptoError("Hay un caracter inválido guardado como turno.")
                    if len(casillas_guardadas) != 8:
                        raise ArchivoCorruptoError("El número de filas guardadas no son las que deberían.")
                    if self.__turno <= 0 or self.__turno > 2:
                        raise ArchivoCorruptoError("No hay turno guardado o el turno guardado es incorrecto.")
                    for fila in casillas_guardadas:
                        if len(fila) != 8:
                            raise ArchivoCorruptoError("El número de casillas de una fila no es el que debería.")
                    
                    self.__tablero = Tablero(casillas_guardadas)

                    for i, linea in enumerate(casillas_guardadas):
                        for j, casilla in enumerate(linea):
                            piezas: list[int] = [10, 11, 20, 21]

                            # Se comprueba si hay posiciones no válidas marcadas como ocupadas
                            if ((i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0)) and casilla in piezas:
                                raise ArchivoCorruptoError("Hay piezas en posiciones no válidas.")

                            if casilla == 10 or casilla == 20:
                                pieza: Pieza = Pieza(Vector(j, i), casilla // 10, self.__tablero)
                                if pieza.posicion in pieza.fila_promociones:
                                    raise ArchivoCorruptoError("Hay piezas en posiciones no válidas")

                                self.__piezas.update({pieza.id : pieza})
                            elif casilla == 11 or casilla == 21:
                                pieza: Pieza = Pieza(Vector(j, i), casilla // 10, self.__tablero, dama=True)
                                self.__piezas.update({pieza.id : pieza})
                carga_finalizada = True
                carga_exitosa = True

            except FileNotFoundError:
                print("\nNo hay ninguna partida guardada.\n")
                carga_finalizada = True
            except ArchivoCorruptoError as e:
                print(f"\nEl archivo está corrupto.\n{e}\n¿Quieres intentar arreglarlo? (s/n)")
                opcion_elegida: str = ""
                while opcion_elegida.lower() != "s" and opcion_elegida.lower() != "n":
                    opcion_elegida = input()
                    if opcion_elegida.lower() != "s" and opcion_elegida.lower() != "n":
                        print("Opción no válida")
                if opcion_elegida == "s":
                    carga_finalizada = not self.arreglar_archivo_guardado()
                else:
                    carga_finalizada = True
        return carga_exitosa
    
    def arreglar_archivo_guardado(self) -> bool:
        try:
            turno: int = 0
            casillas: list[list[int]] = []
            casillas_validas: list[int] = [0, 10, 11, 20, 21]
            with open("partida_guardada.save", "r", encoding="utf-8") as archivo_guardado:
                for linea in archivo_guardado:
                    if "·" in linea:
                        casillas.append([int(i) for i in linea.lstrip("·").split() if i.isnumeric() and int(i) in casillas_validas])
                    elif "T" in linea:
                        try:
                            turno = int(linea.rstrip("\n")[-1])
                        except ValueError:
                            turno = 1
                if len(casillas) < 8:
                    for i in range(8 - len(casillas)):
                        casillas.append([0, 0, 0, 0, 0, 0, 0, 0])
                if len(casillas) > 8:
                    for i in range(len(casillas) - 8):
                        casillas.pop()
                if turno <= 0 or turno > 2:
                    turno = 1
                for fila in casillas:
                    if len(fila) < 8:
                        for i in range(8 - len(fila)):
                            fila.append(0)
                    if len(fila) > 8:
                        for i in range(len(fila) - 8):
                            fila.pop()

                for i, linea in enumerate(casillas):
                    for j, casilla in enumerate(linea):
                        piezas: list[int] = [10, 11, 20, 21]

                        if ((i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0)) and casilla in piezas:
                            casillas[i][j] = 0

                        if casilla == 10 or casilla == 20:
                            pieza: Pieza = Pieza(Vector(j, i), casilla // 10, self.__tablero)
                            if pieza.posicion in pieza.fila_promociones:
                                casillas[i][j] += 1

            # Reescritura del archivo corregido:
            archivo_guardado = open("partida_guardada.save", "w", encoding="utf-8")
            archivo_guardado.close()

            with open("partida_guardada.save", "a", encoding="utf-8") as archivo_guardado:
                casillas_tablero: list[str] = []

                for i in range(len(casillas)):
                    fila = "· "
                    for j in range(len(casillas[i])):
                        fila += f"{casillas[i][j]:4}"
                    fila += "\n"
                    casillas_tablero.append(fila)

                archivo_guardado.writelines(casillas_tablero)
                archivo_guardado.write(f"\nT {turno}")
            
            return True
        
        except FileNotFoundError:
            print("El archivo no existe")
            return False
            

if __name__ == "__main__":
    juego = Juego()
    juego.inicio()
