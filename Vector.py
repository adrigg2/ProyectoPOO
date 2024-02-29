from dataclasses import dataclass
from math import sqrt

@dataclass
class Vector:
    coord_x: float
    coord_y: float

    @property
    def modulo(self):
        return sqrt(self.coord_x ** 2 + self.coord_y ** 2)

    def __add__(self, __value: object) -> object:
        if isinstance(__value, Vector):
            return Vector(self.coord_x + __value.coord_x, self.coord_y + __value.coord_y)
        raise ValueError("No se puede sumar Vector con otros objetos.")
    
    def __sub__(self, __value: object) -> object:
        if isinstance(__value, Vector):
            return self + Vector(-__value.coord_x, -__value.coord_y)
        raise ValueError("No se puede restar Vector con otros objetos.")
    
    def __mul__(self, __value: object) -> object:
        if isinstance(__value, Vector):
            return Vector(self.coord_x * __value.coord_x, self.coord_y * __value.coord_y)
        if isinstance(__value, int) or isinstance(__value, float):
            return Vector(self.coord_x * __value, self.coord_y * __value)
        raise ValueError("Solo se puede multiplicar Vector por otra Vector o por un número.")
    
    def __copy__(self) -> object:
        return Vector(self.coord_x, self.coord_y)
    
    def __lt__(self, __value: object) -> object:
        if isinstance(__value, Vector):
            return self.modulo < __value.modulo
        raise ValueError("No se puede comparar Vector con otros objetos")
    
    def __gt__(self, __value: object) -> object:
        if isinstance(__value, Vector):
            return not self < __value
        raise ValueError("No se puede comparar Vector con otros objetos")
    
    def producto_escalar(self, __value: object) -> float:
        if isinstance(__value, Vector):
            return self.coord_x * __value.coord_x + self.coord_y * __value.coord_y
        raise ValueError("El producto escalar solo puede realizarse entre 2 vectores.")

    def normalizar(self) -> object:
        return Vector(self.coord_x / self.modulo, self.coord_y / self.modulo)

if __name__ == "__main__":
    pos = Vector(1, 1)
    print(pos)

    pos += Vector(1, 1)
    print(pos)

    pos = Vector(1, 1)
    pos2 = Vector(2, 2)

    pos3 = pos - pos2
    print(pos)
    print(pos2)
    print(pos3)

    print(pos != pos2)

    pos = Vector(2, 2)

    print(pos != pos2)

    try:
        print(Vector(1, 2) + 2)
    except Exception:
        print("ERROR")

    print("---------------------")
    p1 = Vector(5, 5)
    p2 = Vector(4, 4)
    p3 = Vector(7, 7)

    print(p1.normalizar() * sqrt(2)) #type: ignore

    lista = [
        Vector(1, 1),
        Vector(2, 2)
    ]

    print(Vector(1, 1) in lista)
