import sys, pygame
from casilla import *
from mapa import *
from pygame.locals import *
from nodo import *
from AEstrella import *
from AEstrellaEpsilon import *


MARGEN=5
MARGEN_INFERIOR=60
TAM=30
NEGRO=(0,0,0)
HIERBA=(250, 180, 160)
MURO=(30, 70, 140)
AGUA=(173, 216, 230) 
ROCA=(110, 75, 48)
AMARILLO=(255, 255, 0) 

# ---------------------------------------------------------------------
# Funciones
# ---------------------------------------------------------------------

# Devuelve si una casilla del mapa se puede seleccionar como destino o como origen
def bueno(mapa, pos):
    res= False
    
    if mapa.getCelda(pos.getFila(),pos.getCol())==0 or mapa.getCelda(pos.getFila(),pos.getCol())==4 or mapa.getCelda(pos.getFila(),pos.getCol())==5:
       res=True
    
    return res
    
# Devuelve si una posición de la ventana corresponde al mapa
def esMapa(mapa, posicion):
    res=False     
    
    if posicion[0] > MARGEN and posicion[0] < mapa.getAncho()*(TAM+MARGEN)+MARGEN and \
    posicion[1] > MARGEN and posicion[1] < mapa.getAlto()*(TAM+MARGEN)+MARGEN:
        res= True       
    
    return res
    
#Devuelve si se ha pulsado algún botón
def pulsaBoton(mapa, posicion):
    res=-1
    
    if posicion[0] > (mapa.getAncho()*(TAM+MARGEN)+MARGEN)//2-65 and posicion[0] < (mapa.getAncho()*(TAM+MARGEN)+MARGEN)//2-15 and \
       posicion[1] > mapa.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapa.getAlto()*(TAM+MARGEN)+MARGEN:
        res=1
    elif posicion[0] > (mapa.getAncho()*(TAM+MARGEN)+MARGEN)//2+15 and posicion[0] < (mapa.getAncho()*(TAM+MARGEN)+MARGEN)//2+65 and \
       posicion[1] > mapa.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapa.getAlto()*(TAM+MARGEN)+MARGEN:
        res=2

    
    return res
   
# Construye la matriz para guardar el camino
def inic(mapa):    
    cam=[]
    for i in range(mapa.alto):        
        cam.append([])
        for j in range(mapa.ancho):            
            cam[i].append('.')
    
    return cam

        
# función principal
def main():
    pygame.init()    
    
    reloj=pygame.time.Clock()
    
    if len(sys.argv)==1: #si no se indica un mapa coge mapa.txt por defecto
        file='mapa.txt'
    else:
        file=sys.argv[-1]
         
    mapa=Mapa(file)     
    camino=inic(mapa)   
    
    anchoVentana=mapa.getAncho()*(TAM+MARGEN)+MARGEN
    altoVentana= MARGEN_INFERIOR+mapa.getAlto()*(TAM+MARGEN)+MARGEN    
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension)
    pygame.display.set_caption("Practica 1")
    
    boton1=pygame.image.load("boton1.png").convert()
    boton1=pygame.transform.scale(boton1,[50, 30])
    
    boton2=pygame.image.load("boton2.png").convert()
    boton2=pygame.transform.scale(boton2,[50, 30])
    
    personaje=pygame.image.load("rabbit.png").convert()
    personaje=pygame.transform.scale(personaje,[TAM, TAM])
    
    objetivo=pygame.image.load("carrot.png").convert()
    objetivo=pygame.transform.scale(objetivo,[TAM, TAM])
    
    coste=-1
    cal=0
    running= True    
    origen=Casilla(-1,-1)
    destino=Casilla(-1,-1)
    
    while running:        
        #procesamiento de eventos
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                running=False 
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()      
                if pulsaBoton(mapa, pos)==1 or pulsaBoton(mapa, pos)==2:
                    if origen.getFila()==-1 or destino.getFila()==-1:
                        print('Error: No hay origen o destino')
                    else:
                        camino=inic(mapa)
                        if pulsaBoton(mapa, pos)==1:
                            a_star = AEstrella(mapa, origen, destino, tipo_heuristica=2)
                            caminos_nodos, coste, cal = a_star.estrella() 
                                     
                            if coste==-1:
                                print('Error: No existe un camino válido entre origen y destino')
                            
                            else:
                                for nodo in caminos_nodos:
                                    camino[nodo.getFila()][nodo.getCol()] = 'x'
                        # Segundo botón: Algoritmo A*ε
                        elif pulsaBoton(mapa, pos) == 2:
                            # Aquí se llama al algoritmo estrella_epsilon
                            a_star_epsilon = AEstrellaEpsilon(mapa, origen, destino, tipo_heuristica=2)
                            caminos_nodos, coste, cal = a_star_epsilon.estrella_epsilon(epsilon=1.1)  # Usa el valor de epsilon deseado

                            if coste == -1:
                                print('Error: No existe un camino válido entre origen y destino')
                            else:
                                for nodo in caminos_nodos:
                                    camino[nodo.getFila()][nodo.getCol()] = 'x'
                            
                elif esMapa(mapa,pos):                    
                    if event.button==1: #botón izquierdo                        
                        colOrigen=pos[0]//(TAM+MARGEN)
                        filOrigen=pos[1]//(TAM+MARGEN)
                        casO=Casilla(filOrigen, colOrigen)                        
                        if bueno(mapa, casO):
                            origen=casO
                        else: # se ha hecho click en una celda no accesible
                            print('Error: Esa casilla no es válida')
                    elif event.button==3: #botón derecho
                        colDestino=pos[0]//(TAM+MARGEN)
                        filDestino=pos[1]//(TAM+MARGEN)
                        casD=Casilla(filDestino, colDestino)                        
                        if bueno(mapa, casD):
                            destino=casD
                        else: # se ha hecho click en una celda no accesible
                            print('Error: Esa casilla no es válida')         
        
        #código de dibujo        
        #limpiar pantalla
        screen.fill(NEGRO)
        #pinta mapa
        for fil in range(mapa.getAlto()):
            for col in range(mapa.getAncho()):                
                if camino[fil][col]!='.':
                    pygame.draw.rect(screen, AMARILLO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif mapa.getCelda(fil,col)==0:
                    pygame.draw.rect(screen, HIERBA, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif mapa.getCelda(fil,col)==4:
                    pygame.draw.rect(screen, AGUA, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif mapa.getCelda(fil,col)==5:
                    pygame.draw.rect(screen, ROCA, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)                                    
                elif mapa.getCelda(fil,col)==1:
                    pygame.draw.rect(screen, MURO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    
        #pinta origen
        screen.blit(personaje, [(TAM+MARGEN)*origen.getCol()+MARGEN, (TAM+MARGEN)*origen.getFila()+MARGEN])        
        #pinta destino
        screen.blit(objetivo, [(TAM+MARGEN)*destino.getCol()+MARGEN, (TAM+MARGEN)*destino.getFila()+MARGEN])       
        #pinta botón
        screen.blit(boton1, [anchoVentana//2-65, mapa.getAlto()*(TAM+MARGEN)+MARGEN+10])
        screen.blit(boton2, [anchoVentana//2+15, mapa.getAlto()*(TAM+MARGEN)+MARGEN+10])
        #pinta coste y energía
        if coste!=-1:            
            fuente= pygame.font.Font(None, 25)
            textoCoste=fuente.render("Coste: "+str(coste), True, AMARILLO)            
            screen.blit(textoCoste, [anchoVentana-90, mapa.getAlto()*(TAM+MARGEN)+MARGEN+15])
            textoEnergía=fuente.render("Cal: "+str(cal), True, AMARILLO)
            screen.blit(textoEnergía, [5, mapa.getAlto()*(TAM+MARGEN)+MARGEN+15])
            
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)
        
    pygame.quit()
    
#---------------------------------------------------------------------
if __name__=="__main__":
    main()
