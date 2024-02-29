from Juego import Juego
from os import system

# Función para permitir que las terminales de Windows (cmd y powershell) muestren color
system('color')

if __name__ == "__main__":
    juego = Juego()
    juego.inicio()
