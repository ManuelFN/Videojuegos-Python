import math  # Importamos la libreria math para usar sus funciones
import random

import pygame  # Importamos la libreria pygame para usar sus funciones

# Paleta de colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
H_FA2F2F = (250, 47, 47)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AZUL_OSCURO = (36, 90, 190)
H_50D2FE = (94, 210, 254)


# region clases
class Bloque(pygame.sprite.Sprite):  # Creamos la clase 'Bloque' que derivara de la clase Sprite

    def __init__(self, x, y):  # Creamos el constructor y le pasamos como parametros la posicionX y posicionY

        super().__init__()  # Heredamos el constructor de Sprite

        self.image = pygame.image.load("Imagenes/ladrillo.png")  # Cargamos la imagen para la apariencia del bloque
        self.rect = self.image.get_rect()  # Obtenemos el area del bloque

        self.rect.x = x  # Establecemos la posicionX del bloque el mismo valor que el parametro X
        self.rect.y = y  # Establecemos la posicionY del bloque el mismo valor que el parametro Y


class Pelota(pygame.sprite.Sprite):  # Creamos la clase 'Pelota' que derivara de la clase Sprite

    velocidad = 6.0  # Velocidad de la pelota

    x = 300  # Posicion X inicial
    y = 320  # Posicion Y inicial

    rumbo = 200  # Rumbo de la pelota

    largo = 25  # Largo de la pelota
    alto = 25  # Alto de la pelota

    def __init__(self):  # Creamos el constructor de Pelota

        super().__init__()  # Heredamos el constructor de Sprite

        self.image = pygame.image.load("Imagenes/ball.png")  # Cargamos la imagen para dar apariencia a la pelota
        self.rect = self.image.get_rect()  # Obtenemos el area de la pelota

        self.alto_pantalla = pygame.display.get_surface().get_height()  # Obtenemos el alto de la pantalla
        self.ancho_pantalla = pygame.display.get_surface().get_width()  # Obtenemos el largo de la pantalla

    def botar(self, diff):  # Creamos la funcion botar a la que le pasamos como parametro la variable diff
        self.rumbo = (180 - self.rumbo) % 360  # Actualizamos el valor de rumbo
        self.rumbo -= diff  # Restamos a rumbo el valor de diff

    def update(self):  # Creamos la funcion update
        rumbo_radianes = math.radians(self.rumbo)  # Creamos la variable rumbo_radianes a partir del atributo rumbo del objeto

        self.x += self.velocidad * math.sin(rumbo_radianes)  # Cambia la posición X según la velocidad y el rumbo
        self.y -= self.velocidad * math.cos(rumbo_radianes)  # Cambia la posición Y según la velocidad y el rumbo

        self.rect.x = int(self.x)  # Actualiza la posicion X
        self.rect.y = int(self.y)  # Actualiza la posicion Y

        if self.y <= 0:  # Si la pelota toca el borde superior
            self.botar(0)
            self.y = 1

        if self.x <= 0:  # Si la pelota toca el borde izquierdo
            self.rumbo = (360 - self.rumbo) % 360
            self.x = 1

        if self.x > self.ancho_pantalla - self.largo:  # Si la pelota toca el borde derecho
            self.rumbo = (360 - self.rumbo) % 360
            self.x = self.ancho_pantalla - self.largo - 1

        if self.y > 600:  # Si la pelota toca el borde inferior
            pygame.mixer.Sound.play(sonidoPerderVida) # Se reproduce el sonido
            self.reiniciar() # Se reinicia la pelota

    # Función para reiniciar la pelota a su ubicación inicial si tocará el borde inferior
    
    def reiniciar(self):
        self.x = 300
        self.y = 320


class Protagonista(pygame.sprite.Sprite):  # Creamos la clase protagonista (pala) que deriva de la clase Sprite

    def __init__(self):  # Creamos el constructor
        super().__init__()  # Heredamos el constructor de Sprite

        self.largo = 100  # Establecemos el largo del objeto
        self.alto = 30  # Establecemos el alto del objeto

        self.image = pygame.image.load("Imagenes/shovell.png")  # Cargamos la imagen para darle apariencia al objeto
        # self.image = pygame.transform.scale(self.image, (120, 18))
        self.rect = self.image.get_rect()  # Obtenemos el area del objeto

        self.alto_pantalla = pygame.display.get_surface().get_height()  # Obtenemos el alto de la pantalla
        self.largo_pantalla = pygame.display.get_surface().get_width()  # Obtenemos el largo de la pantalla

        self.rect.x = 300  # PosicionX incial
        self.rect.y = self.alto_pantalla - self.alto - 5  # PosicionY inicial

    def update(self):  # Creamos la funcion update

        keys = pygame.key.get_pressed()  # Variable que permite saber si pulsamos alguna tecla
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # Si pulsamos la tecla '<--' o 'a'
            self.rect.x = self.rect.x - 10  # Movemos la pala a la izquierda
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # Si pulsamos la tecla '-->' o 'd'
            self.rect.x = self.rect.x + 10  # Movemos la pala a la derecha

        # Limita el margen izquierdo para que no pueda avanzar la pala
        if self.rect.left < 0:
            self.rect.left = 0

        # Limita el margen derecho para que no pueda avanzar la pala
        if self.rect.right > self.largo_pantalla:
            self.rect.right = self.largo_pantalla

# endregion

pygame.init()

icono = pygame.image.load("imagenes/icono.png")
pygame.display.set_icon(icono)

# region variables
pygame.display.set_caption("Juego de romper ladrillos")  # Establecemos el titulo de la ventana
pantalla = pygame.display.set_mode([800, 600])  # Estalbecemos el tamano de la pantalla (ancho x alto)
fondo_pantalla = pygame.Surface(pantalla.get_size())  # Obtenemos la superficie del fondo de la pantalla

puntuacion = 0  # Puntuacion del jugador
vidas = 3  # Vidas del jugador

fuente = pygame.font.Font(None, 100)  # Creamos una fuente y seleccionamos su tamaño
font = pygame.font.Font(None, 34)  # Creamos una fuente y seleccionamos su tamaño
font2 = pygame.font.Font(None, 29)  # Creamos una fuente y seleccionamos su tamaño

marcadorPuntos = font.render("Puntuación: " + str(puntuacion), 1, BLANCO)  # Creamos el marcador de los puntos por romper ladrillos
marcadorVidas = font.render("Vidas: " + str(vidas), 1, BLANCO)  # Creamos el marcador de las vidas restantes
marcadorTitulo = font2.render("JUEGA A ROMPER LADRILLOS", 1, BLANCO)  # Creamos el marcador del titulo del juego

# Sonidos

sonidoRebote = pygame.mixer.Sound("Sonidos/rebote.ogg")  # Creamos una variable que guarde el sonido de rebote
sonidoPunto = pygame.mixer.Sound("Sonidos/punto.ogg")  # Creamos una variable que guarde un sonido
sonidoVictoria = pygame.mixer.Sound("Sonidos/victoria.ogg")  # Creamos una variable que guarde el sonido para cuando ganas
sonidoDerrota = pygame.mixer.Sound("Sonidos/derrota.ogg")  # Creamos una variable que guarde el sonido para cuando pierdes
sonidoExplosion = pygame.mixer.Sound("Sonidos/explosion.ogg")  # Creamos una variable que guarde el sonido de rebote con los bloques
sonidoPerderVida = pygame.mixer.Sound("Sonidos/perder_vida.ogg")  # Creamos una variable que guarde el sonido de rebote con los bloques

bloques = pygame.sprite.Group()  # Creamos un grupo de sprites llamado para los bloques
pelotas = pygame.sprite.Group()  # Creamos un grupo de sprites para la pelota
todos_los_sprites = pygame.sprite.Group()  # Creamos un grupo de sprites para todos los grupos de sprites

protagonista = Protagonista()  # Creamos la pala
todos_los_sprites.add(protagonista)  # Anadimos a el grupo de todos los sprites el sprite de la pala

pelota = Pelota()  # Creamos la pelota
pelotas.add(pelota)  # Anadimos al grupo de sprites de pelotas la pelota
todos_los_sprites.add(pelota)  # Anadimos la pelota al grupo de sprites para todos los sprites

separacionSuperior = 80  # Separacion del borde superior respecto a la primera fila de bloques

for fila in range(5):  # Por cada fila de bloques (5)
    for columna in range(8):  # Por cada columna en cada fila (8)
        bloque = Bloque(columna * (90 + 2) + 35, separacionSuperior)  # Creamos un bloque (posicionX, posicionY)
        bloques.add(bloque)  # Anadimos el bloque creado al grupo de sprites de todos los bloques
        todos_los_sprites.add(bloque)  # Anadimos el bloque creado al grupo de sprites de todos los sprites
    separacionSuperior += 35  # Cuando cambiamos de fila aumentamos la separacion superior para que no se pisen las filas entre ellas

reloj = pygame.time.Clock()  # Creamos una variable para establecer un limite de FPS
game_over = False  # Creamos una variable para saber si hemos perdido
game_win = False  # Creamos una variable para saber si hemos ganado
salir_programa = False  # Creamos una variable para saber si hemos salido del programa


# endregion

# region funciones

def ejecucionJuego(fsalir, fvidas, fmarcadorvidas):  # Funcion que comprobara si hemos salido del juego y controla el refresco de pantalla
    reloj.tick(60)  # Limitamos los FPS de la aplicacion
    pantalla.fill((51, 153, 255))  # Pintamos el fondo de la pantalla del color indicado (R,G,B)

    for evento in pygame.event.get():  # Por cada evento que suceda en la aplicacion
        if evento.type == pygame.QUIT:  # Si el evento es cerrar la ventana
            fsalir = True  # fsalir pasa a ser verdadero

    if pelota.y > 595:  # Si la pelota toca el borde inferior de la pantalla
        fvidas = fvidas - 1  # Restamos una vida
        fmarcadorvidas = font.render("Vidas: " + str(fvidas), 1, BLANCO)  # Actualizamos las vidas del jugador
        if vidas <= 1:  # Si acabamos de gastar la ultima vida
            texto = fuente.render("HAS PERDIDO", True, ROJO)  # Mostramos que hemos perdido la partida
            pantalla.blit(texto, (180, 270))  # Renderizamos el texto de derrota
            pygame.mixer.Sound.play(sonidoDerrota)
            pygame.time.wait(2000)  # Esperamos
            fsalir = True  # Fsalir pasa a ser verdadero

    if game_over:  # Si hemos perdido
        texto = fuente.render("HAS PERDIDO", True, ROJO)  # Creamos el texto de derrota
        pantalla.blit(texto, (180, 270))  # Renderizamos el texto
        pygame.mixer.Sound.play(sonidoDerrota)
        pygame.time.wait(2000)  # Esperamos un segundo
        fsalir = True  # fsalir pasa a ser verdadero y salimos del programa
    elif game_win:  # Si hemos ganado
        texto = fuente.render("HAS GANADO", True, VERDE)  # Creamos el texto de victoria
        pantalla.blit(texto, (180, 270))  # Renderizamos el texto
        pygame.mixer.Sound.play(sonidoVictoria)
        pygame.time.wait(2500)  # Esperamos
        fsalir = True  # fsalir pasa a ser verdadero y salimos del programa

    return fsalir, fvidas, fmarcadorvidas  # Deuelve el estado de la variable fJugando


def renderizarElementos():  # Funcion que se encarga de refrescar todos los elementos en pantalla
    todos_los_sprites.draw(pantalla)  # Renderizo el grupo de todos los sprites en la pantalla
    pantalla.blit(marcadorPuntos, (50, 20))  # Renderizo el marcador de los puntos por romper ladrillos
    pantalla.blit(marcadorTitulo, (270, 20))  # Renderizo el marcador del titulo del juego
    pantalla.blit(marcadorVidas, (640, 20))  # Renderizo el marcador de las vidas
    pygame.display.flip()  # Actualizo toda la pantalla


def colisiones(fvictoria, fpuntuacion, fmarcadorpuntos):  # Funcion que detectara las colisiones de los diferentes elementos del programa
    if pygame.sprite.spritecollide(protagonista, pelotas, False):  # Si la pala colisiona con la pelota (unico elemento dentro del grupo pelotas)
        pygame.mixer.Sound.play(sonidoRebote)  # Reproducimos el sonido de rebote
        diff = (protagonista.rect.x + protagonista.largo / 2) - (pelota.rect.x + pelota.largo / 2)  # Actualizamos el valor de diff
        pelota.rect.y = pantalla.get_height() - 30 - 30 - 1  # Rebota encima de la pala
        pelota.botar(diff)  # Cambiamos la direccion de la pelota

    if pygame.sprite.spritecollide(pelota, bloques, True):  # Si pelota colisiona con algun elemento dentro de el grupo bloques
        pygame.mixer.Sound.play(sonidoExplosion)  # Reproducimos el sonido de rebote
        fpuntuacion += 1  # Sumamos un punto al jugador
        fmarcadorpuntos = font.render("Puntuación: " + str(fpuntuacion), 1, BLANCO)  # Actualizamos los puntos del jugador
        pelota.botar(0)  # Cambiamos la direccion de la pelota
    elif len(bloques) == 0:  # Si no quedan mas bloques por destruir
        fvictoria = True  # fvictoria pasa a ser verdadero

    return fvictoria, fpuntuacion, fmarcadorpuntos  # Devolvemos el valor de fvictoria, fpuntuacion y fmarcadorpuntos


# endregion

# region ejecucion

while not salir_programa:  # Mientras no salgamos del programa

    salir_programa, vidas, marcadorVidas = ejecucionJuego(salir_programa, vidas, marcadorVidas)  # Controlamos si nos hemos quedado sin vidas y si salimos del programa

    protagonista.update()  # Actualizamos la posicion de la pala
    pelota.update()

    game_win, puntuacion, marcadorPuntos = colisiones(game_win, puntuacion, marcadorPuntos)  # Controlamos la puntuacion y si hemos ganado (destruido todos los bloques)

    renderizarElementos()  # Llamamos a la funcion para renderizar los elementos en pantalla

# endregion

pygame.quit()  # Quitamos pygame
