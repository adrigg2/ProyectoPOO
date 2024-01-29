from dataclasses import dataclass

@dataclass
class Posicion:
    coord_x: int
    coord_y: int

    def __add__(self, __value: object) -> object:
        if type(__value) == Posicion:
            return Posicion(self.coord_x + __value.coord_x, self.coord_y + __value.coord_y)
        raise Exception("No se puede sumar posición con otros objetos.")
    
    def __sub__(self, __value: object) -> object:
        if type(__value) == Posicion:
            return self + Posicion(-__value.coord_x, -__value.coord_y)
        raise Exception("No se puede restar posición con otros objetos.")
    
    def __mul__(self, __value: object) -> object:
        if type(__value) == Posicion:
            return Posicion(self.coord_x * __value.coord_x, self.coord_y * __value.coord_y)
        raise Exception("No se puede multiplicar posición por otros objetos.")
    
    def __copy__(self) -> object:
        return Posicion(self.coord_x, self.coord_y)

if __name__ == "__main__":
    pos = Posicion(1, 1)
    print(pos)

    pos += Posicion(1, 1)
    print(pos)

    pos = Posicion(1, 1)
    pos2 = Posicion(2, 2)

    pos3 = pos - pos2
    print(pos)
    print(pos2)
    print(pos3)

    print(pos != pos2)

    pos = Posicion(2, 2)

    print(pos != pos2)
