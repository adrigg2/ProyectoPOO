from Posicion import Posicion

class Vista:
    piezas: dict[int, str]
    diccionario_columna: dict[int, str]

    def __init__(self, piezas: dict[int, str]) -> None:
        self.piezas = piezas
        self.diccionario_columna = {
            0 : 'a',
            1 : 'b',
            2 : 'c',
            3 : 'd',
            4 : 'e',
            5 : 'f',
            6 : 'g',
            7 : 'h'
        }

    def bienvenida(self) -> None:
        print("Bienvenid@ al juego de las damas\n")
    
    def intrucciones(self) -> None:
        input("Presiona enter para continuar")

    def mostrar_tablero(self, casillas_tablero: list[list[int]]) -> None:
        print()
        resultado = ""
        for fila in range(len(casillas_tablero) - 1, -1, -1):
            resultado += f"{fila + 1}\t"
            for casilla in casillas_tablero[fila]:
                if casilla == 0:
                    resultado += "·  "
                else:
                    resultado += f"{self.piezas[casilla]}  "
            if fila == 4:
                resultado += "\t PARA ABANDONAR LA PARTIDA"
            elif fila == 5:
                resultado += "\t ESCRIBE \"ABANDONAR\""
            elif fila == 2:
                resultado += "\t PARA REINICIAR LA PARTIDA"
            elif fila == 3:
                resultado += "\t ESCRIBE \"REINICIAR\""
            resultado += "\n"
        resultado += "\n\ta  b  c  d  e  f  g  h\n"
        print(resultado)

    def mostrar_piezas_movibles(self, posiciones: list[Posicion]) -> str:
        resultado: str = ""
        for posicion in posiciones:
            id_casilla = self.diccionario_columna[posicion.coord_x] + str(posicion.coord_y + 1)
            resultado += id_casilla + "  "
        print(resultado)

        pieza_a_mover: str = ""
        while pieza_a_mover.lower() not in resultado.split():
            pieza_a_mover = input("Elige pieza a mover: ")
            if pieza_a_mover.lower() not in resultado.split():
                print("Esa no es una posición válida.")

        return pieza_a_mover.lower()
    
    def mostrar_movimientos(self, posiciones: list[str]) -> str:
        resultado: str = ""
        for posicion in posiciones:
            resultado += posicion
            resultado += "  "
        print(resultado)

        posicion_a_mover: str = ""
        while posicion_a_mover.lower() not in resultado.split() and posicion_a_mover.lower() != "atras" and posicion_a_mover.upper() != "ABANDONAR":
            posicion_a_mover = input("Elige posición para mover la pieza (o escribe \"atras\" para elegir otra pieza): ")
            if posicion_a_mover.lower() not in resultado.split() and posicion_a_mover.lower() != "atras" and posicion_a_mover.upper() != "ABANDONAR":
                print("Esa no es una posición válida.")

        return posicion_a_mover.lower()
    
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
