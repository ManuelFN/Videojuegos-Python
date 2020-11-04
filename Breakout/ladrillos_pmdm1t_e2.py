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

class Pelota:
    def __init__(self, fichero_imagen):
        # --- Atributos de la Clase ---

        # Imagen de la Pelota
        self.imagen = pygame.image.load(fichero_imagen).convert_alpha()

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
            # self.dir_y = -self.dir_y
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
            pelota.dir_x = -pelota.dir_x
            pelota.dir_y = -pelota.dir_y


# Inicialización de Pygame, creación de la ventana, título y control de reloj.
pygame.init()

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Destrozando ladrillos")
clock = pygame.time.Clock()

pelota = Pelota("imagenes/ball.png")

# Grupo de sprites, instanciación del objeto jugador.
sprites = pygame.sprite.Group()
pala = Jugador()
sprites.add(pala)

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

    font = pygame.font.Font(None, 34)
    text = font.render("Puntuación: " + str(puntuacion), 1, BLANCO)
    pantalla.blit(text, (20, 10))
    text = font.render("Vidas: " + str(vidas), 1, BLANCO)
    pantalla.blit(text, (650, 10))

    # Actualiza el contenido de la pantalla.
    pygame.display.flip()

pygame.quit()
