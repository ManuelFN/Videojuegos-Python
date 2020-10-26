import pygame
import sys
from pygame.locals import *

# Tamaño de pantalla
ANCHO = 800
ALTO = 600

# Variable de puntuación y vida
score = 0
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

        sonidoPunto = pygame.mixer.Sound("sonidos/sonido_punto.wav")

        # Velocidad predeterminada cada vuelta del bucle si no pulsas nada
        self.velocidad_x = 0

        # Mantiene las teclas pulsadas
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:  # Tecla A o Flechita izquierda
            self.velocidad_x = -10

        # Mueve el personaje hacia la derecha
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:  # Tecla D o Flechita derecha
            self.velocidad_x = 10

        # Actualiza la velocidad del personaje
        self.rect.x += self.velocidad_x

        # Limita el margen izquierdo
        if self.rect.left < 0:
            self.rect.left = 0
            pygame.mixer.Sound.play(sonidoPunto)

        # Limita el margen derecho
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
            pygame.mixer.Sound.play(sonidoPunto)

        # Limita el margen superior
        if self.rect.top < 0:
            self.rect.top = 0

        # Limita el margen inferior
        if self.rect.bottom < 0:
            self.rect.bottom = 0


# Inicialización de Pygame, creación de la ventana, título y control de reloj.
pygame.init()

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Destrozando ladrillos")
clock = pygame.time.Clock()

ball = pygame.image.load("imagenes/ball.png")  # Creamos un objeto 'Ball' desde una imagen
ballCollider = ball.get_rect()  # Obtenemos el area de 'Ball'
ballCollider.center = (int(ANCHO / 2), int(ALTO / 2))  # Sacamos la bola desde el centro de la pantalla
ballSpeed = [1, 1]  # Velocidad de la bola (velocidadX,velocidadY)

# ballrect = ball.get_rect()

# ballrect = ballrect.move(ANCHO // 2, ALTO // 2)

# pantalla.blit(ball, ballrect)

# Grupo de sprites, instanciación del objeto jugador.
sprites = pygame.sprite.Group()
jugador = Jugador()
sprites.add(jugador)

# Bucle de juego
ejecutando = True
while ejecutando:

    # Especifica la velocidad del bucle de juego
    clock.tick(FPS)

    # Eventos
    for event in pygame.event.get():
        # Se cierra y termina el bucle
        if event.type == pygame.QUIT:
            ejecutando = False

    # Actualización de sprites
    sprites.update()

    # colision = pygame.sprite.spritecollide(jugador, bola, False)

    # Fondo de pantalla, dibujo de sprites y formas geométricas.
    pantalla.fill(AZUL_OSCURO)
    sprites.draw(pantalla)
    pygame.draw.line(pantalla, H_50D2FE, (400, 0), (400, 800), 1)
    pygame.draw.line(pantalla, VERDE, (0, 300), (800, 300), 1)
    icono = pygame.image.load("imagenes/pong_icono.png")
    pygame.display.set_icon(icono)

    font = pygame.font.Font(None, 34)
    text = font.render("Puntuación: " + str(score), 1, BLANCO)
    pantalla.blit(text, (20, 10))
    text = font.render("Vidas: " + str(vidas), 1, BLANCO)
    pantalla.blit(text, (650, 10))

    # Actualiza el contenido de la pantalla.
    pygame.display.flip()

pygame.quit()
