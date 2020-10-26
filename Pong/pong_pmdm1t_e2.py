import pygame

pygame.init()  # Siempre hay que inicializar el pygame al principio del programa

# region variables
tamanoPantalla = 960, 720  # Elegimos el tamano de la pantalla (ancho x alto)
puntuacionJugador = 0  # Puntuacion del jugador
puntuacionOrdenador = 0  # Puntuacion del ordenador
screen = pygame.display.set_mode(tamanoPantalla)  # Establecer tamano de la pantalla
pygame.display.set_caption("Juego de Ping-Pong")  # Titulo de la ventana

anchoPantalla = 960  # Ancho de la ventana
altoPantalla = 720  # Altura de la ventana
colorFondo = 51, 153, 255  # Color de fondo para la pantalla (R,G,B)

sonidoPunto = pygame.mixer.Sound("Sonidos/punto.ogg")  # Creamos una variable que guarde el sonido de anotar un punto
sonidoRebote = pygame.mixer.Sound("Sonidos/rebote.ogg")  # Creamos una variable que guarde el sonido de rebote

font = pygame.font.Font(None, 32)  # Creamos una fuente y seleccionamos su tamaño
titulo = font.render("Juego de Ping-Pong", 1, (0, 0, 0))  # Creamos el 'titulo' para la ventana
marcadorJugador = font.render(str(puntuacionJugador), 1, (0, 0, 0))  # Creamos el marcador del jugador
marcadorOrdenador = font.render(str(puntuacionOrdenador), 1, (0, 0, 0))  # Creamos el marcador del ordenador

ball = pygame.image.load("Imagenes/ball.png")  # Creamos un objeto 'Ball' desde una imagen
ballCollider = ball.get_rect()  # Obtenemos el area de 'Ball'
ballCollider.center = (int(anchoPantalla / 2), int(altoPantalla / 2))  # Sacamos la bola desde el centro de la pantalla
ballSpeed = [1, 1]  # Velocidad de la bola (velocidadX,velocidadY)

net = pygame.image.load("Imagenes/net.png")  # Creamos un objeto 'Net' desde una imagen
netCollider = net.get_rect()  # Obtenemos el area de 'Net'
netCollider.move_ip(480, 0)  # Muevo a 'Net' al centro de la pantalla (posicionX,posicionY)

playerShovell = pygame.image.load("Imagenes/shovell.png")  # Creamos un objeto 'Pala para el jugador' desde una imagen
playerShovellCollider = playerShovell.get_rect()  # Obtenemos el area de la 'Pala para el jugador'
playerShovellCollider.move_ip(25, 360)  # Muevo la 'Pala para el jugador' al lado izquierdo de la pantalla

computerShovell = pygame.image.load("Imagenes/shovell.png")  # Creamos un objeto 'Pala para el ordenador'
computerShovellCollider = computerShovell.get_rect()  # Obtenemos el area de la 'Pala para el ordenador'
computerShovellCollider.move_ip(935, 160)  # Muevo la 'Pala para el ordenador' al lado derecho de la pantalla

jugando = True  # Booleano que sera verdadero si el juego esta en ejecucion
# endregion

# region funciones

def renderizarElementos():
    screen.fill(colorFondo)  # Renderizo el fondo de la ventana con el color 'colorFondo'
    screen.blit(titulo, (370, 0))  # Renderizo el letrero del titulo
    screen.blit(marcadorJugador, (340, 25))  # Renderizo el marcador del jugador (izquierda)
    screen.blit(marcadorOrdenador, (590, 25))  # Renderizo el marcador del ordenador (derecha)
    screen.blit(net, netCollider)  # Renderizo la red
    screen.blit(ball, ballCollider)  # Renderizo la bola
    screen.blit(playerShovell, playerShovellCollider)  # Renderizo la pala del jugador
    screen.blit(computerShovell, computerShovellCollider)  # Renderizo la pala del ordenador
    pygame.display.flip()  # Refresco la pantalla


def controlOrdenador():
    if ballCollider.y < computerShovellCollider.y:  # Si la bola esta en una posicion mas baja que la bola
        computerShovellCollider.y -= 1  # Se mueve la pala del ordenador abajo
    elif ballCollider.y > computerShovellCollider.y:  # Si la bola esta en una posicion mas alta que la bola
        computerShovellCollider.y += 1  # Se mueve la pala del ordenador arriba


def controlJugador(fplayerShovellCollider):
    keys = pygame.key.get_pressed()  # Compruebo si se ha pulsado alguna tecla
    if keys[pygame.K_UP]:  # Si pulsamos la tecla arriba
        fplayerShovellCollider = fplayerShovellCollider.move(0, -1)  # Movemos arriba la 'Pala para el jugador'
    elif keys[pygame.K_DOWN]:  # Si pulsamos la tecla abajo
        fplayerShovellCollider = fplayerShovellCollider.move(0, 1)  # Movemos abajo la 'Pala para el jugador'

    return fplayerShovellCollider


def ejecucionJuego(fjugando):
    pygame.time.delay(3)  # Tiempo de espera para el refresco de pantalla en milisegundos
    for event in pygame.event.get():  # Capturamos los eventos que se han producido
        if event.type == pygame.QUIT:  # Si el evento es salir de la ventana
            fjugando = False  # Quitamos el juego

    return fjugando


def rebotePala():
    if computerShovellCollider.colliderect(ballCollider):  # Si hay colision de la 'Pala para el jugadr' con 'Ball'
        pygame.mixer.Sound.play(sonidoRebote)  # Reproducimos el sonido de rebote
        ballSpeed[0] = -ballSpeed[0]  # Invertimos la velocidadX de la bola haciendo que rebote hacia el otro lado
    elif playerShovellCollider.colliderect(ballCollider):  # Si hay colision de la 'Pala para el ordenador' con 'Ball'
        pygame.mixer.Sound.play(sonidoRebote)  # Reproducimos el sonido de rebote
        ballSpeed[0] = -ballSpeed[0]  # Invertimos la velocidadX de la bola haciendo que rebote hacia el otro lado


def reboteBorde(fPuntuacionOrdenador, fMarcadorOrdenador, fPuntuacionJugador, fMarcadorJugador):
    if ballCollider.x <= 0:  # Si la bola toca el borde izquierdo de la pantalla
        pygame.mixer.Sound.play(sonidoPunto)  # Reproducimos el sonido de marcar un punto
        fPuntuacionOrdenador = fPuntuacionOrdenador + 1  # Sumamos un punto al score del ordenador
        ballCollider.center = (int(anchoPantalla / 2), int(altoPantalla / 2))  # Se reinicia la posicion de la bola al centro para jugar otro punto
        fMarcadorOrdenador = font.render(str(fPuntuacionOrdenador), 1, (0, 0, 0))  # Cambiamos el valor del marcador de los puntos del ordenador

    elif ballCollider.x + ballCollider.width >= anchoPantalla:  # Si la bola toca el borde derecho de la pantalla
        pygame.mixer.Sound.play(sonidoPunto)  # Reproducimos el sonido de marcar un punto
        fPuntuacionJugador = fPuntuacionJugador + 1  # Sumamos un punto al score del jugador
        ball.center = (anchoPantalla / 2, altoPantalla / 2)  # Reiniciamos la bola al centro
        fMarcadorJugador = font.render(str(fPuntuacionJugador), 1, (0, 0, 0))  # Actualizamos los puntos del jugador

    elif ballCollider.y <= 0:  # Si la bola toca el borde inferior de la pantalla
        pygame.mixer.Sound.play(sonidoRebote)  # Reproducimos el sonido de rebote
        ballSpeed[1] = -ballSpeed[1]  # Invertimos su velocidad haciendo que rebote hacia arriba

    elif ballCollider.y + ballCollider.height >= altoPantalla:  # Si la bola toca el borde superior de la pantalla
        pygame.mixer.Sound.play(sonidoRebote)  # Reproducimos el sonido de rebote
        ballSpeed[1] = -ballSpeed[1]  # Invertimos su velocidad haciendo que rebote hacia abajo

    return fMarcadorOrdenador, fMarcadorJugador

# endregion

# region enPartida

while jugando:  # Mientras el juego se este ejecutando

    jugando = ejecucionJuego(jugando)

    playerShovellCollider = controlJugador(playerShovellCollider)

    rebotePala()

    controlOrdenador()

    ballCollider = ballCollider.move(ballSpeed)  # Movemos 'Ball' segun la velocidad establecida

    marcadorOrdenador, marcadorJugador = reboteBorde(puntuacionOrdenador, marcadorOrdenador, puntuacionJugador, marcadorJugador)

    renderizarElementos()

# endregion

pygame.quit()  # Salgo de la aplicacion
