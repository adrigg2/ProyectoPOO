from Vector import Vector

class Tablero:
    casillas: list[list[int]]
    diccionario_columna: dict[str, int]

    def __init__(self) -> None:
        self.piezas = []
        self.casillas = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.diccionario_columna = {
            'a' : 0,
            'b' : 1,
            'c' : 2,
            'd' : 3,
            'e' : 4,
            'f' : 5,
            'g' : 6,
            'h' : 7
        }
    
    def __str__(self) -> str:
        resultado: str = ""
        for i in range(len(self.casillas)):
            for j in range(len(self.casillas)):
                resultado += str(self.casillas[i][j])
                resultado += "  "
            resultado += "\n"
        
        return resultado
    
    def comprobar_posicion(self, posicion: Vector):
        return self.casillas[int(posicion.coord_y)][int(posicion.coord_x)]
    
    def actualizar_tablero(self, posicion: Vector, jugador: int, posicion_anterior: Vector = Vector(-1, -1)):
        if posicion_anterior != Vector(-1, -1):
            self.casillas[int(posicion_anterior.coord_y)][int(posicion_anterior.coord_x)] = 0
        if posicion != Vector(-1, -1):
            self.casillas[int(posicion.coord_y)][int(posicion.coord_x)] = jugador

    def convertir_a_posicion(self, id_posicion: str):
        coordenadas: list[int] = []
        for letra in id_posicion:
            if letra.isalpha():
                coordenadas.append(self.diccionario_columna[letra])
            elif letra.isnumeric():
                coordenadas.append(int(letra) - 1)
        return Vector(coordenadas[0], coordenadas[1])
    
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
