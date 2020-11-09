import random

import pygame
import sys
from pygame.locals import *

# Tamaño de pantalla
ANCHO = 800
ALTO = 600

# Variable de puntuación y vida
puntuacion = 0
vidas = 3

# FPS
FPS = 60

# Paleta de colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
H_FA2F2F = (250, 47, 47)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AZUL_OSCURO = (36, 90, 190)
H_50D2FE = (94, 210, 254)

# Tamaño de los bloques break-out
largo_bloque = 87
alto_bloque = 28


class Bloque(pygame.sprite.Sprite):
    # Esta clase representa a cada bloque que será golpeado por la pelota

    def __init__(self, color, x, y):
        # Constructor. Pasa el color del bloque y su posición x, y.

        # Llama al constructor de la clase padre (Sprite)
        super().__init__()

        # Crea una imagen del bloque de tamaño apropiado
        # El largo y alto son enviados como una lista al primer parámetro.
        self.image = pygame.Surface([largo_bloque, alto_bloque])

        # Rellenamos la imagen con el color apropiado
        self.image.fill(color)

        # Extraemos el objeto rectángulo que posee las dimensiones de la imagen
        self.rect = self.image.get_rect()

        # Movemos la esquina superior izquierda del rectángulo a las coordenadas x,y.
        # Aquí es donde aparecerá nuestro bloque.
        self.rect.x = x
        self.rect.y = y


class Pelota:
    def __init__(self, fichero_imagen):
        # --- Atributos de la Clase ---

        # Imagen de la Pelota
        self.imagen = pygame.image.load(fichero_imagen).convert_alpha()
        self.imagen = pygame.transform.scale(self.imagen, (30, 30))

        self.imagenCollider = self.imagen.get_rect()

        # Dimensiones de la Pelota
        self.ancho, self.alto = self.imagen.get_size()

        # Posición de la Pelota
        self.x = int(ANCHO / 2)
        self.y = int(ALTO / 2)

        # Dirección de movimiento de la Pelota
        self.dir_x = random.choice([-4, 4])
        self.dir_y = random.choice([-4, 4])

    def mover(self):
        self.x += self.dir_x
        self.y += self.dir_y

    def rebotar(self):

        sonido = pygame.mixer.Sound("sonidos/sonido_punto.wav")

        if self.x <= 0:
            self.dir_x = -self.dir_x
            pygame.mixer.Sound.play(sonido)
        if self.x + self.ancho >= ANCHO:
            self.dir_x = -self.dir_x
            pygame.mixer.Sound.play(sonido)
        if self.y <= 0:
            self.dir_y = -self.dir_y
            pygame.mixer.Sound.play(sonido)
        if self.y + self.alto >= ALTO:
            global vidas
            # Restamos una vida
            vidas -= 1
            # Si llega a 0 le imprimimos que ha perdido y si quiere volver a intentarlo que presione la tecla 'R'
            if vidas == 0:
                # Creamos los tipos de fuente para los letreros que vamos a poner
                font = pygame.font.Font(None, 74)
                font2 = pygame.font.Font(None, 34)
                # Creamos los letreros con sus respectivos tamaños y posiciones
                text = font.render("HAS PERDIDO", 1, BLANCO)
                texto2 = font2.render("Presiona R para reiniciar", 1, BLANCO)
                text_rect = text.get_rect(center=(ANCHO / 2, ALTO / 2))
                # Los imprimos por pantalla
                pantalla.blit(texto2, (263, 325))
                pantalla.blit(text, text_rect)
                pygame.display.flip()

                # Realizamos una comprobación al jugador de si quiere reiniciar el juego tras haber perdido

                while True:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == KEYDOWN and event.key == K_r:
                            vidas = 4
                            return

            self.reiniciar()
            pygame.mixer.Sound.play(sonido)

    def reiniciar(self):
        self.x = int(ANCHO / 2)
        self.y = int(ALTO / 2)
        self.dir_x = -self.dir_x
        self.dir_y = random.choice([-4, 4])


class Jugador(pygame.sprite.Sprite):
    # Sprite del jugador
    def __init__(self):
        # Heredamos el init de la clase Sprite de Pygame
        super().__init__()
        # Rectángulo (jugador)
        self.image = pygame.Surface((110, 15))
        self.image.fill(H_FA2F2F)
        # Obtiene el rectángulo (sprite)
        self.rect = self.image.get_rect()
        # Posición del rectángulo (sprite)
        self.rect.x = 345
        self.rect.y = 500

    # Actualiza esto cada vuelta de bucle.
    def update(self):

        sonido = pygame.mixer.Sound("sonidos/sonido_punto.wav")

        # Velocidad predeterminada cada vuelta del bucle si no pulsas nada
        self.velocidad_x = 0

        # Mantiene las teclas pulsadas
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:  # Tecla A o Flechita izquierda
            self.velocidad_x = -10

        # Mueve el personaje hacia la derecha
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:  # Tecla D o Flechita derecha
            self.velocidad_x = 10

        # Actualiza la velocidad de la pala
        self.rect.x += self.velocidad_x

        # Limita el margen izquierdo
        if self.rect.left < 0:
            self.rect.left = 0
            pygame.mixer.Sound.play(sonido)

        # Limita el margen derecho
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
            pygame.mixer.Sound.play(sonido)

        # Limita el margen superior
        if self.rect.top < 0:
            self.rect.top = 0

        # Limita el margen inferior
        if self.rect.bottom < 0:
            self.rect.bottom = 0

    def golpear(self, pelota):
        if (
                self.rect.x + 110 > pelota.x > self.rect.x
                and pelota.y + pelota.alto > self.rect.y
                and pelota.y < self.rect.y + 15
        ):
            pelota.dir_y = -pelota.dir_y

def main():
    # Inicialización de Pygame, creación de la ventana, título y control de reloj.
    pygame.init()

    global pantalla

    pantalla = pygame.display.set_mode((ANCHO, ALTO))

    pygame.display.set_caption("Destrozando ladrillos")
    clock = pygame.time.Clock()

    pelota = Pelota("imagenes/bola2.png")

    # Grupo de sprites, instanciación del objeto jugador.
    sprites = pygame.sprite.Group()
    pala = Jugador()
    sprites.add(pala)
    bloques = pygame.sprite.Group()

    # La parte superior del bloque (posición y)
    top = 80

    # Número de bloques a crear
    numero_de_bloques = 8

    # Cinco filas de bloques
    for fila in range(5):
        # 32 columnas de bloques
        for columna in range(1, numero_de_bloques):
            # Crea un bloque (color,x,y)
            bloque = Bloque(AZUL, columna * (largo_bloque + 2) + 1, top)
            bloques.add(bloque)
            sprites.add(bloque)
        # Mueve  hacia abajo el borde superior de la siguiente fila
        top += alto_bloque + 2

    # Bucle de juego
    ejecutando = True
    while ejecutando:

        pelota.mover()
        pelota.rebotar()
        pala.golpear(pelota)

        # Especifica la velocidad del bucle de juego
        clock.tick(FPS)

        # Eventos
        for event in pygame.event.get():
            # Se cierra y termina el bucle
            if event.type == pygame.QUIT:
                ejecutando = False

        # Actualización de sprites
        sprites.update()

        # Fondo de pantalla, dibujo de sprites y formas geométricas.
        pantalla.fill(NEGRO)
        sprites.draw(pantalla)
        pantalla.blit(pelota.imagen, (round(pelota.x), round(pelota.y)))
        pygame.draw.line(pantalla, H_50D2FE, (400, 0), (400, 800), 1)
        pygame.draw.line(pantalla, VERDE, (0, 300), (800, 300), 1)
        icono = pygame.image.load("imagenes/pong_icono.png")
        pygame.display.set_icon(icono)

        # Imprimimos los textos de puntuación y vidas

        font = pygame.font.Font(None, 34)
        text = font.render("Puntuación: " + str(puntuacion), 1, BLANCO)
        pantalla.blit(text, (20, 10))
        text = font.render("Vidas: " + str(vidas), 1, BLANCO)
        pantalla.blit(text, (650, 10))

        # Comprueba las colisiones entre las pelotas y los bloques
        # bloquesmuertos = pygame.sprite.spritecollide(pelota, bloques, True)

        # Si le damos a un bloque, botamos las pelotas
        # if len(bloquesmuertos) > 0:
            #pelota.botar(0)

            # El juego se termina si todos los bloques desaparecen.
            # if len(bloques) == 0:
                # game_over = True

        # Actualiza el contenido de la pantalla.
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
