from Vector import Vector

class Tablero:
    __casillas: list[list[int]]
    __diccionario_columna: dict[str, int]

    @property
    def casillas(self) -> list[list[int]]:
        return self.__casillas

    def __init__(self, casillas: list[list[int]] = [[0 for x in range(8)] for y in range(8)]) -> None:
        self.__casillas = casillas
        self.__diccionario_columna = {
            'a' : 0,
            'b' : 1,
            'c' : 2,
            'd' : 3,
            'e' : 4,
            'f' : 5,
            'g' : 6,
            'h' : 7
        }
    
    # Método para mostrar el tablero sin formatear como cadena por pantalla
    def __str__(self) -> str:
        resultado: str = ""
        for i in range(len(self.__casillas)):
            for j in range(len(self.__casillas)):
                resultado += str(self.__casillas[i][j])
                resultado += "  "
            resultado += "\n"
        
        return resultado
    
    # Método para comprobar la ocupación de una casilla
    def comprobar_posicion(self, posicion: Vector) -> int:
        return self.__casillas[int(posicion.coord_y)][int(posicion.coord_x)]
    
    # Método para actualizar el tablero. Recibe la posición nueva de la pieza, su posición anterior y su id
    # Vacía la posición anterior y ocupa la nueva posición con la id de la pieza
    def actualizar_tablero(self, posicion: Vector, id: int, posicion_anterior: Vector = Vector(-1, -1)) -> None:
        if posicion_anterior != Vector(-1, -1):
            self.__casillas[int(posicion_anterior.coord_y)][int(posicion_anterior.coord_x)] = 0
        if posicion != Vector(-1, -1):
            self.__casillas[int(posicion.coord_y)][int(posicion.coord_x)] = id

    # Método para convertir una posición en notación de tablero a un vector
    def convertir_a_posicion(self, id_posicion: str) -> Vector:
        coordenadas: list[int] = []
        for letra in id_posicion:
            if letra.isalpha():
                coordenadas.append(self.__diccionario_columna[letra])
            elif letra.isnumeric():
                coordenadas.append(int(letra) - 1)
        return Vector(coordenadas[0], coordenadas[1])
    
    # Método para convertir una posición en Vector a una cadena en notación del tablero
    def codificar_posicion(self, posicion: Vector) -> str:
        columnas = list(self.__diccionario_columna.keys())
        resultado = columnas[int(posicion.coord_x)] + str(int(posicion.coord_y) + 1)
        return resultado
    
if __name__ == "__main__":
    tablero = Tablero()
    tablero.actualizar_tablero(Vector(1, 1), 1)
    print(tablero)
    input()
    tablero.actualizar_tablero(Vector(3, 4), 1)
    print(tablero)
    input()
    tablero.actualizar_tablero(Vector(2, 2), 1, Vector(1, 1))
    print(tablero)
