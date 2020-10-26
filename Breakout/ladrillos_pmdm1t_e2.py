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

        sonidoColision = pygame.mixer.Sound("sonidos/colision.wav")

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
            pygame.mixer.Sound.play(sonidoColision)

        # Limita el margen derecho
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
            pygame.mixer.Sound.play(sonidoColision)

        # Limita el margen superior
        if self.rect.top < 0:
            self.rect.top = 0
            pygame.mixer.Sound.play(sonidoColision)

        # Limita el margen inferior
        if self.rect.bottom < 0:
            self.rect.bottom = 0
            pygame.mixer.Sound.play(sonidoColision)

        # colision = pygame.sprite.spritecollideany(ball, sprites)

        # if colision:
            # if colision == jugador:
                # self.rect.x == self.dx
                # self.dx *= -1
                # self.dx *= random.choice([0, 1])


    def rebotePala(self):

        colision_jugador = self.get_rect()  # Obtenemos el area de la 'Pala para el jugador'

        if colision_jugador.colliderect(ballCollider):  # Si hay colision de la 'Pala para el ordenador' con 'Ball'
            # pygame.mixer.Sound.play(sonidoRebote)  # Reproducimos el sonido de rebote
            ballSpeed[1] = -ballSpeed[1]  # Invertimos la velocidadX de la bola haciendo que rebote hacia el otro lado

# Inicialización de Pygame, creación de la ventana, título y control de reloj.
pygame.init()

def reboteBorde(puntuacion, vidas):

    sonidoColision = pygame.mixer.Sound("sonidos/colision.wav")

    if ballCollider.x <= 0:  # Si la bola toca el borde izquierdo de la pantalla
        pygame.mixer.Sound.play(sonidoColision)  # Reproducimos el sonido de marcar un punto
        ballCollider.center = (int(ANCHO / 2), int(ALTO / 2))  # Se reinicia la posicion de la bola al centro para jugar otro punto
        ballSpeed[1] = -ballSpeed[1]  # Invertimos su velocidad haciendo que rebote hacia arriba
        # fMarcadorOrdenador = font.render(str(fPuntuacionOrdenador), 1, (0, 0, 0))  # Cambiamos el valor del marcador de los puntos del ordenador

    if ballCollider.x + ballCollider.width >= ANCHO:  # Si la bola toca el borde derecho de la pantalla
        pygame.mixer.Sound.play(sonidoColision)  # Reproducimos el sonido de marcar un punto
        ballSpeed[1] = -ballSpeed[1]  # Invertimos su velocidad haciendo que rebote hacia arriba
        # fMarcadorJugador = font.render(str(puntuacion), 1, (0, 0, 0))  # Actualizamos los puntos del jugador

    if ballCollider.y <= 0:  # Si la bola toca el borde inferior de la pantalla
        pygame.mixer.Sound.play(sonidoColision)  # Reproducimos el sonido de rebote
        ball.center = (ANCHO / 2, ALTO / 2)  # Reiniciamos la bola al centro
        vidas = vidas - 1

    if ballCollider.y + ballCollider.height >= ALTO:  # Si la bola toca el borde superior de la pantalla
        pygame.mixer.Sound.play(sonidoColision)  # Reproducimos el sonido de rebote
        ballSpeed[1] = -ballSpeed[1]  # Invertimos su velocidad haciendo que rebote hacia abajo

    return puntuacion, vidas

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Destrozando ladrillos")
clock = pygame.time.Clock()

# ball = pygame.draw.circle(pantalla, ROJO, (10, 10), 5)
ball = pygame.image.load("imagenes/bola3.png")  # Creamos un objeto 'Ball' desde una imagen
ball = pygame.transform.scale(ball, (27, 27))
ballCollider = ball.get_rect()  # Obtenemos el area de 'Ball'
ballCollider.center = (int(ANCHO / 2), int(ALTO / 2))  # Sacamos la bola desde el centro de la pantalla
ballSpeed = [1, 1]  # Velocidad de la bola (velocidadX,velocidadY)

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
    puntuacion, vidas = reboteBorde(puntuacion, vidas)

    # Fondo de pantalla, dibujo de sprites y formas geométricas.
    pantalla.fill(AZUL_OSCURO)
    sprites.draw(pantalla)
    pygame.draw.line(pantalla, H_50D2FE, (400, 0), (400, 800), 1)
    pygame.draw.line(pantalla, VERDE, (0, 300), (800, 300), 1)
    icono = pygame.image.load("imagenes/pong_icono.png")
    pygame.display.set_icon(icono)

    font = pygame.font.Font(None, 34)
    texto_puntuacion = font.render("Puntuación: " + str(puntuacion), 1, BLANCO)
    pantalla.blit(texto_puntuacion, (20, 10))
    texto_vidas = font.render("Vidas: " + str(vidas), 1, BLANCO)
    pantalla.blit(texto_vidas, (650, 10))
    ballCollider = ballCollider.move(ballSpeed)  # Movemos 'Ball' segun la velocidad establecida
    pantalla.blit(ball, ballCollider)

    # Actualiza el contenido de la pantalla.
    pygame.display.flip()

pygame.quit()
