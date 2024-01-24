class Posicion:
    coord_x: int
    coord_y: int

    def __init__(self, coord_x: int, coord_y: int) -> None:
        self.coord_x = coord_x
        self.coord_y = coord_y

    def __add__(self, __value: object) -> object:
        if type(__value) == Posicion:
            return Posicion(self.coord_x + __value.coord_x, self.coord_y + __value.coord_y)
        raise Exception("No se puede sumar posición con otros objetos.")
    
    def __eq__(self, __value: object) -> bool:
        if type(__value) == Posicion:
            return self.coord_x == __value.coord_x and self.coord_y == __value.coord_y
        raise Exception("No se puede comparar posición con otros objetos.")
    
    def __ne__(self, __value: object) -> bool:
        if type(__value) == Posicion:
            return self.coord_x != __value.coord_x or self.coord_y != __value.coord_y
        raise Exception("No se puede comparar posición con otros objetos.")

    def __str__(self) -> str:
        return f"x: {self.coord_x} y: {self.coord_y}"

if __name__ == "__main__":
    pos = Posicion(1, 1)
    print(pos)

    pos += Posicion(1, 1)
    print(pos)

    pos = Posicion(1, 1)
    pos2 = Posicion(2, 2)

    pos3 = pos + pos2
    print(pos)
    print(pos2)
    print(pos3)
