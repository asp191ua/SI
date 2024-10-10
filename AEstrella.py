import heapq  # Para gestionar la lista de frontera como una cola de prioridad
from casilla import *
from nodo import *
import math

class AEstrella:
    
     # Constructor
    def __init__(self, mapi, inicio, meta, tipo_heuristica = 0):
        self.mapi = mapi
        self.inicio = inicio
        self.meta = meta
        self.tipo_heuristica = tipo_heuristica
        

    # Funcion para validar que sea una casilla dentro del mapa y no sea un muro
    def validar_casilla (self, fila, col):
        """Verifica si la casilla está dentro de los límites del mapa y no es un muro."""
        return (0 <= fila < self.mapi.getAlto() and
                0 <= col < self.mapi.getAncho() and
                self.mapi.getCelda(fila, col) != 1)  # Si no es muro

    def hijos(self, nodo):
        hijos = []
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        
        for x in direcciones:
            fila = nodo.casilla.getFila() + x[0]
            col = nodo.casilla.getCol() + x[1]
            
            if self.validar_casilla(fila, col): 
                hijos.append(Casilla(fila, col))
                
        return hijos


    def coste(self, direccion):
        horizontal_vertical = {(1, 0), (0, 1), (-1, 0), (0, -1)}
        
        if direccion in horizontal_vertical:
            return 1
        else:
            return 1.5

    def tipo_calorias(self, casilla):
        gasto = self.mapi.getCelda(casilla.getFila(), casilla.getCol())
        
        if gasto == 0:  
            return 2
        
        elif gasto == 4:  
            return 4
        
        elif gasto == 5:
            return 6
        
        else: 
            return 1
        
    def calorias(self, nodo):
        calorias_consumidas = 0
        
        while nodo.padre is not None:
            calorias_consumidas = calorias_consumidas + self.tipo_calorias(nodo.casilla)
            nodo = nodo.padre
            
        return calorias_consumidas

    
    # HEURÍSTICAS
        
    # Distancia de Manhattan
    def heuristica_manhattan (self, casilla_origen, casilla_final):
        return abs(casilla_final.getCol() - casilla_origen.getCol()) + abs(casilla_final.getFila() - casilla_origen.getFila())  
     
    # Distancia Euclídea
    def heuristica_euclidea (self, casilla_origen, casilla_final):
        return math.sqrt((casilla_final.getCol() - casilla_origen.getCol())**2 + (casilla_final.getFila() - casilla_origen.getFila())**2)
        
    def chebyshev(self, casilla_origen, casilla_final):
        return max(abs(casilla_final.getCol() - casilla_origen.getCol()), abs(casilla_final.getFila() - casilla_origen.getFila()))
        
    
    # función para calcular la heurística según el tipo
    def heuristica(self, casilla_origen, casilla_final):
        
        if self.tipo_heuristica == 0:
            return 0  
        
        elif self.tipo_heuristica == 1:
            return self.heuristica_manhattan(casilla_origen, casilla_final)  
        
        elif self.tipo_heuristica == 2:
            return self.heuristica_euclidea(casilla_origen, casilla_final)  
        

    def estrella(self):


        casilla_inicial = Nodo(self.inicio, g=0, h=self.heuristica(self.inicio, self.meta), calorias=0)
        casilla_meta = Nodo(self.meta)
        
        # Matriz nodos explorados
        matriz_explorados = [] 
        for i in range(self.mapi.getAlto()):        
            matriz_explorados.append([])
            
            for j in range(self.mapi.getAncho()):            
                matriz_explorados[i].append(-1)
            
        nodos_explorados = -1
        
        lista_frontera = []
        heapq.heappush(lista_frontera, casilla_inicial)
        lista_interior = []

        while lista_frontera != []:
            
            casilla_actual = heapq.heappop(lista_frontera)

            lista_interior.append(casilla_actual)
            nodos_explorados += 1
            x, y = casilla_actual.casilla.getCol(), casilla_actual.casilla.getFila()
            matriz_explorados[y][x] = nodos_explorados
            
            # Si el nodo actual es el nodo meta, se ha encontrado el camino
            if casilla_actual == casilla_meta:
                
                print("Nodos explorados")
                for i in matriz_explorados:
                    print(i)
                
                return self.construye_camino(casilla_actual), casilla_actual.g, self.calorias(casilla_actual)

            

            # Expande los nodos vecinos
            for m in self.hijos(casilla_actual):
                fila = m.getFila()  
                col = m.getCol() 

                # Calcula el coste de movimiento
                coste_x = col - casilla_actual.casilla.getCol()
                coste_y = fila - casilla_actual.casilla.getFila()
                coste_movimiento = self.coste((coste_x, coste_y))

                gm = coste_movimiento + casilla_actual.g
                nodo_vecino = Nodo(m, g=gm, h=self.heuristica(m, self.meta), padre=casilla_actual)

                # Si el nodo vecino ya está en la lista interior, continúa
                if nodo_vecino in lista_interior:
                    continue

                # Si el nodo vecino no está en la frontera o tiene un menor coste, añádelo a la frontera
                if nodo_vecino not in lista_frontera:
                    # Almacenamos el valor de f, g, h y padre en el nodo
                    m.f = nodo_vecino.g + nodo_vecino.h  
                    m.g = nodo_vecino.g                 
                    m.h = nodo_vecino.h                
                    m.padre = casilla_actual            

                    # Añadimos el nodo a la lista de frontera 
                    heapq.heappush(lista_frontera, nodo_vecino)
                    
                    
                # Si ya está en la lista de frontera, pero encontramos un mejor camino
                else:
                   
                    for nodo in lista_frontera:
                        if nodo_vecino.casilla.getFila() == nodo.casilla.getFila() and nodo_vecino.casilla.getCol() == nodo.casilla.getCol():
                            if nodo_vecino.g < nodo.g:
                                nodo.g = nodo_vecino.g
                                nodo.f = nodo.g + nodo.h
                                nodo.padre = casilla_actual
                            

        # Si no se encuentra un camino
        return None, -1, 0


    def construye_camino(self, nodo):
        camino = []
        while nodo is not None:
            camino.append(nodo.casilla)
            nodo = nodo.padre
        return camino[::-1]
