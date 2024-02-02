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
    
    def reducir_a_unidad(self) -> object:
        coord_x: int = 1
        coord_y: int = 1

        if self.coord_x < 0:
            coord_x = -1
        
        if self.coord_y < 0:
            coord_y = -1

        return Posicion(coord_x, coord_y)

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

    try:
        print(Posicion(1, 2) + 2)
    except Exception:
        print("ERROR")
