from Vector import Vector
from Excepciones import OpcionNoValidaError
from colorama import Fore, Back, Style

class Vista:
    __piezas: dict[int, str]
    __diccionario_columna: dict[int, str]
    __palabras_clave: tuple[str, str, str]
    __color_jugador: dict[int, str]

    def __init__(self) -> None:
        self.__piezas = {
            0 : "o",
            1 : "O",
            10 : f"{Style.BRIGHT}{Fore.RED}o{Style.RESET_ALL}",
            20 : f"{Style.BRIGHT}{Fore.BLUE}o{Style.RESET_ALL}",
            11 : f"{Style.BRIGHT}{Fore.RED}O{Style.RESET_ALL}",
            21 : f"{Style.BRIGHT}{Fore.BLUE}O{Style.RESET_ALL}"
        }

        self.__diccionario_columna = {
            0 : 'a',
            1 : 'b',
            2 : 'c',
            3 : 'd',
            4 : 'e',
            5 : 'f',
            6 : 'g',
            7 : 'h'
        }

        self.__palabras_clave = (
            "abandonar",
            "reiniciar",
            "guardar"
        )

        self.__color_jugador = {
            1 : Style.BRIGHT + Back.RED,
            2 : Style.BRIGHT + Back.BLUE
        }

    # Método que imprime un mensaje de bienvenida
    def bienvenida(self) -> None:
        print("Bienvenid@ al juego de las damas\n")

    # Método que imprime el menú de inicio y devuelve la opción elegida por el jugador
    # o lanza una excepción si la opción no es correcta
    def menu_inicio(self) -> int:
        opciones_posibles: list[int] = [1, 2, 3]

        print("\nElije una opción escribiendo su número:")
        print("1. Jugar")
        print("2. Cargar partida")
        print("3. Salir\n")

        try:
            opcion_elegida: int = int(input())
        except ValueError:
            raise OpcionNoValidaError("La opción elegida debe ser un número")

        if opcion_elegida not in opciones_posibles:
            raise OpcionNoValidaError("La opción elegida no es correcta")
        else:
            return opcion_elegida

    # Método para mostrar el tablero en pantalla
    def mostrar_tablero(self, casillas_tablero: list[list[int]], turno: int, posiciones_a_marcar: list[Vector] = []) -> None:
        print()
        filas: list[str] = []
        texto_ayuda: tuple[str, str, str, str, str, str] = (
            f"\t ESCRIBE {Fore.YELLOW}\"ABANDONAR\"{Style.RESET_ALL}",
            "\t PARA ABANDONAR LA PARTIDA",
            f"\t ESCRIBE {Fore.YELLOW}\"REINICIAR\"{Style.RESET_ALL}",
            "\t PARA REINICIAR LA PARTIDA",
            f"\t ESCRIBE {Fore.YELLOW}\"GUARDAR\"{Style.RESET_ALL}",
            "\t PARA GUARDAR Y SALIR"
        )

        # Analiza las casillas de la lista de int que recibe como parámetro y la convierte en caracteres
        for i, fila in enumerate(casillas_tablero):
            fila_string = f"{i + 1}\t"
            for j, casilla in enumerate(fila):
                if Vector(j, i) in posiciones_a_marcar:
                    if casilla == 0:
                        if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0):
                            fila_string += f"{Style.BRIGHT}{self.__color_jugador[turno]}#{Style.RESET_ALL}  "
                        else:
                            fila_string += f"{Style.BRIGHT}{self.__color_jugador[turno]}·{Style.RESET_ALL}  "
                    else:
                        fila_string += f"{Style.BRIGHT}{self.__color_jugador[turno]}{self.__piezas[casilla // 100 % 10]}{Style.RESET_ALL}  "
                else:
                    if casilla == 0:
                        if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0):
                            fila_string += "#  "
                        else:
                            fila_string += "·  "
                    else:
                        fila_string += f"{self.__piezas[casilla // 100]}  "
            filas.append(fila_string)
        # Invierte el tablero para mostrarlo con las filas en orden descendiente (de la 8 a la 1)
        filas = filas[::-1]
        filas.append("\ta  b  c  d  e  f  g  h\n")

        # Coloca el texto de ayuda centrado en el tablero
        for i in range(1, 7):
            filas[i] += texto_ayuda[i - 1]

        resultado = "\n".join(filas)
        print(resultado)

    # Método que muestra las piezas que pueden ser movidas y devuelve la pieza elegida por el jugador
    def mostrar_piezas_movibles(self, posiciones: list[Vector], turno: int) -> str:
        piezas_movibles: str = ""
        if turno == 1:
            piezas_movibles += f"Mueven {Style.BRIGHT}{Fore.RED}blancas{Style.RESET_ALL}:\n"
        else:
            piezas_movibles += f"Mueven {Style.BRIGHT}{Fore.BLUE}negras{Style.RESET_ALL}:\n"
        
        for posicion in posiciones:
            id_casilla: str = self.__diccionario_columna[int(posicion.coord_x)] + str(int(posicion.coord_y) + 1)
            piezas_movibles += id_casilla + "  "
        print(piezas_movibles)

        pieza_a_mover: str = ""
        opcion_incorrecta: bool = pieza_a_mover not in piezas_movibles.split() and pieza_a_mover not in self.__palabras_clave
        while opcion_incorrecta:
            pieza_a_mover = input("Elige pieza a mover: ").lower()
            opcion_incorrecta = pieza_a_mover not in piezas_movibles.split() and pieza_a_mover not in self.__palabras_clave
            if opcion_incorrecta:
                print("Esa no es una posición válida.")

        return pieza_a_mover.lower()
    
    # Método que muestra los posibles movimientos de la pieza elegida por el jugador y devuelve la opción elegida
    def mostrar_movimientos(self, posiciones: list[str], primer_movimiento: bool) -> str:
        movimientos_posibles: str = "  ".join(posiciones)
        print(movimientos_posibles)

        posicion_a_mover: str = ""
        if primer_movimiento:
            opcion_incorrecta: bool = posicion_a_mover not in posiciones and posicion_a_mover != "atras" and posicion_a_mover not in self.__palabras_clave
            while opcion_incorrecta:
                posicion_a_mover = input("Elige posición para mover la pieza (o escribe \"atras\" para elegir otra pieza): ").lower()
                opcion_incorrecta = posicion_a_mover not in posiciones and posicion_a_mover != "atras" and posicion_a_mover not in self.__palabras_clave
                if opcion_incorrecta:
                    print("Esa no es una posición válida.")
        else:
            opcion_incorrecta: bool = posicion_a_mover not in posiciones and posicion_a_mover not in self.__palabras_clave[:2]
            while opcion_incorrecta:
                posicion_a_mover = input("Puedes seguir capturando. Elige posición para mover la pieza: ").lower()
                opcion_incorrecta = posicion_a_mover not in posiciones and posicion_a_mover not in self.__palabras_clave[:2]
                if posicion_a_mover == "guardar":
                    print(f"Solo se puede guardar al principio del turno")
                elif opcion_incorrecta:
                    print("Esa no es una posición válida.")

        return posicion_a_mover
    
    # Método para mostrar el texto de final de juego
    def fin_de_juego(self, perdedor: int) -> None:
        if perdedor == 1:
            print("------------------")
            print(f"Ganan las {Style.BRIGHT}{Fore.BLUE}negras{Style.RESET_ALL}")
            print("------------------")
        elif perdedor == 2:
            print("------------------")
            print(f"Ganan las {Style.BRIGHT}{Fore.RED}blancas{Style.RESET_ALL}")
            print("------------------")

    # Método para que permitir al jugador indicar si quiere volver a empezar una vez la partida ha terminado
    def reiniciar(self):
        return input("¿Quieres volver a jugar? (escribe \"s\" si sí, cualquier cosa si no): ")


if __name__ == "__main__":
    pass
