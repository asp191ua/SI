class Nodo:
    def __init__(self, casilla, g=0, h=0, calorias = 0, padre=None):
        self.casilla = casilla 
        self.g = g  
        self.h = h  
        self.padre = padre 
        self.calorias = calorias
        self.f = self.g + self.h

 

    def __eq__(self, otro):
        return self.casilla.getFila() == otro.casilla.getFila() and self.casilla.getCol() == otro.casilla.getCol()

    def __lt__(self, otro):
        return self.f < otro.f

    def __repr__(self):
        return f"Nodo({self.casilla.getFila()}, {self.casilla.getCol()})"
