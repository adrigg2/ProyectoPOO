from Vector import Vector
from Excepciones import OpcionNoValidaError

class Vista:
    __piezas: dict[int, str]
    __diccionario_columna: dict[int, str]
    __palabras_clave: tuple[str, str, str]

    def __init__(self) -> None:
        self.__piezas = {
            10 : "\033[91mo\033[00m",
            20 : "\033[92mo\033[00m",
            11 : "\033[91mO\033[00m",
            21 : "\033[92mO\033[00m"
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

    def bienvenida(self) -> None:
        print("Bienvenid@ al juego de las damas\n")

    def menu_inicio(self) -> int:
        opciones_posibles: list[int] = [1, 2, 3]

        print("Elije una opción escribiendo su número:")
        print("1. Jugar")
        print("2. Cargar partida")
        print("3. Salir")

        opcion_elegida: int = int(input())

        if opcion_elegida not in opciones_posibles:
            raise OpcionNoValidaError("La opción elegida no es correcta")
        else:
            return opcion_elegida

    # Método para mostrar el tablero en pantalla
    def mostrar_tablero(self, casillas_tablero: list[list[int]]) -> None:
        print()
        filas: list[str] = []
        texto_ayuda: tuple[str, str, str, str, str, str] = (
            "\t ESCRIBE \"ABANDONAR\"",
            "\t PARA ABANDONAR LA PARTIDA",
            "\t ESCRIBE \"REINICIAR\"",
            "\t PARA REINICIAR LA PARTIDA",
            "\t ESCRIBE \"GUARDAR\"",
            "\t PARA GUARDAR Y SALIR"
        )

        # Analiza las casillas de la lista de int que recibe como parámetro y la convierte en caracteres
        for i, fila in enumerate(casillas_tablero):
            fila_string = f"{i + 1}\t"
            for j, casilla in enumerate(fila):
                if casilla == 0:
                    if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0):
                        fila_string += "#  "
                    else:
                        fila_string += "·  "
                else:
                    fila_string += f"{self.__piezas[casilla]}  "
            filas.append(fila_string)
        filas = filas[::-1]
        filas.append("\ta  b  c  d  e  f  g  h\n")

        # Coloca el texto de ayuda centrado en el tablero
        for i in range(1, 7):
            filas[i] += texto_ayuda[i - 1]

        resultado = "\n".join(filas)
        print(resultado)

    def mostrar_piezas_movibles(self, posiciones: list[Vector], turno: int) -> str:
        piezas_movibles: str = ""
        if turno == 1:
            piezas_movibles += "Mueven blancas:\n"
        else:
            piezas_movibles += "Mueven negras:\n"
        
        for posicion in posiciones:
            id_casilla: str = self.__diccionario_columna[int(posicion.coord_x)] + str(int(posicion.coord_y) + 1)
            piezas_movibles += id_casilla + "  "
        print(piezas_movibles)

        pieza_a_mover: str = ""
        while pieza_a_mover not in piezas_movibles.split() and pieza_a_mover not in self.__palabras_clave:
            pieza_a_mover = input("Elige pieza a mover: ").lower()
            if pieza_a_mover not in piezas_movibles.split() and pieza_a_mover not in self.__palabras_clave:
                print("Esa no es una posición válida.")

        return pieza_a_mover.lower()
    
    def mostrar_movimientos(self, posiciones: list[str], primer_movimiento: bool) -> str:
        movimientos_posibles: str = "  ".join(posiciones)
        print(movimientos_posibles)

        posicion_a_mover: str = ""
        if primer_movimiento:
            while posicion_a_mover not in posiciones and posicion_a_mover != "atras" and posicion_a_mover not in self.__palabras_clave:
                posicion_a_mover = input("Elige posición para mover la pieza (o escribe \"atras\" para elegir otra pieza): ").lower()
                if posicion_a_mover not in posiciones and posicion_a_mover != "atras" and posicion_a_mover not in self.__palabras_clave:
                    print("Esa no es una posición válida.")
        else:
            while posicion_a_mover not in posiciones and posicion_a_mover not in self.__palabras_clave[:2]:
                posicion_a_mover = input("Puedes seguir capturando. Elige posición para mover la pieza: ").lower()
                if posicion_a_mover == "guardar":
                    print(f"Solo se puede guardar al principio del turno")
                elif posicion_a_mover not in posiciones and posicion_a_mover not in self.__palabras_clave[:2]:
                    print("Esa no es una posición válida.")

        return posicion_a_mover
    
    def fin_de_juego(self, perdedor: int):
        if perdedor == 1:
            print("------------------")
            print("Ganan las negras")
            print("------------------")
        elif perdedor == 2:
            print("------------------")
            print("Ganan las blancas")
            print("------------------")


if __name__ == "__main__":
    pass
