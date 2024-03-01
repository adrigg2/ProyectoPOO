from dataclasses import dataclass
from math import sqrt

@dataclass
class Vector:
    coord_x: float
    coord_y: float

    @property
    def modulo(self):
        return sqrt(self.coord_x ** 2 + self.coord_y ** 2)

    # Método que define la suma de 2 vectores como un vector cuyas coordenadas son la suma de las de los 2 primeros
    def __add__(self, __value: object) -> object:
        if isinstance(__value, Vector):
            return Vector(self.coord_x + __value.coord_x, self.coord_y + __value.coord_y)
        raise ValueError("No se puede sumar Vector con otros objetos.")
    
    # Método que define la resta de 2 vectores como la suma del primero con el opuesto del segundo
    def __sub__(self, __value: object) -> object:
        if isinstance(__value, Vector):
            return self + Vector(-__value.coord_x, -__value.coord_y)
        raise ValueError("No se puede restar Vector con otros objetos.")
    
    # Método que define el producto de 2 vectores como un vector cuyas coordenadas son el pruducto de las de los 2 primeros
    # y el producto de 1 vector con un número como un vector cuyas coordenadas son el producto del número por las del primero
    def __mul__(self, __value: object) -> object:
        if isinstance(__value, Vector):
            return Vector(self.coord_x * __value.coord_x, self.coord_y * __value.coord_y)
        if isinstance(__value, int) or isinstance(__value, float):
            return Vector(self.coord_x * __value, self.coord_y * __value)
        raise ValueError("Solo se puede multiplicar Vector por otra Vector o por un número.")
    
    # Método que define la copia de un vector como un vector cuyas coordenadas son iguales al original
    def __copy__(self) -> object:
        return Vector(self.coord_x, self.coord_y)
    
    # Método que define que un vector es menor que otro si su módulo es menor que el del otro
    def __lt__(self, __value: object) -> object:
        if isinstance(__value, Vector):
            return self.modulo < __value.modulo
        raise ValueError("No se puede comparar Vector con otros objetos")
    
    # Método que define que un vector es mayor que otro si no es menor
    def __gt__(self, __value: object) -> object:
        if isinstance(__value, Vector):
            return not self < __value
        raise ValueError("No se puede comparar Vector con otros objetos")
    
    # Método que recibe dos instancias de la clase y devuelve su producto escalar
    def producto_escalar(self, __value: object) -> float:
        if isinstance(__value, Vector):
            return self.coord_x * __value.coord_x + self.coord_y * __value.coord_y
        raise ValueError("El producto escalar solo puede realizarse entre 2 vectores.")

    # Método que modifica al vector para que su módulo sea 1
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
