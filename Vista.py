class Vista:
    @staticmethod
    def bienvenida() -> None:
        print("Bienvenid@ al juego de las damas\n")
    
    @staticmethod
    def menu_principal() -> int:
        print("Elije una opción (escribiendo su número)")
        print("1. Intrucciones\n2. Jugar\n3. Salir")

        opcion_correcta: bool = False

        while not opcion_correcta:
            try:
                opcion: int = int(input())

                if opcion <= 0 or opcion > 3:
                    raise ValueError("Opción no válida")
            except ValueError:
                print("\nOpción no válida\n")
            else:
                opcion_correcta = True
        
        return opcion #type:ignore
    
    @staticmethod
    def intrucciones() -> None:
        input("Presiona enter para continuar")

if __name__ == "__main__":
    Vista.menu_principal()
