import sys
import pygame

from config import (
    ANCHO, ALTO, FPS, TITULO,
    EVENTO_TIMER, INTERVALO_TIMER,
    FUENTE_PATH, FUENTE_SIZE,
    SND_CORRECTO, SND_INCORRECTO, VOL_INCORRECTO,
)
import juego
from pantallas import (
    cargar_recursos,
    dibujar_pantalla_cantidad,
    dibujar_pantalla_nombres,
    dibujar_sala,
    dibujar_profesora,
    mostrar_resultados,
)

# ── Inicializacion ────────────────────────────────────────────────────────────
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption(TITULO)
fuente = pygame.font.Font(FUENTE_PATH, FUENTE_SIZE)
clock  = pygame.time.Clock()

recursos = cargar_recursos(fuente)

sonido_correcto   = pygame.mixer.Sound(SND_CORRECTO)
sonido_incorrecto = pygame.mixer.Sound(SND_INCORRECTO)
sonido_incorrecto.set_volume(VOL_INCORRECTO)

pygame.time.set_timer(EVENTO_TIMER, INTERVALO_TIMER)

e = juego.estado


# ── Funciones antes del loop ──────────────────────────────────────────────────
def manejar_tecla_configuracion(evento):
    if e["cantidad_jugadores"] == 0:
        if evento.key == pygame.K_RETURN:
            juego.confirmar_cantidad(e["entrada_texto"])
        elif evento.key == pygame.K_BACKSPACE:
            e["entrada_texto"] = e["entrada_texto"][:-1]
        else:
            e["entrada_texto"] += evento.unicode

    elif len(e["jugadores"]) < e["cantidad_jugadores"]:
        if evento.key == pygame.K_RETURN:
            juego.confirmar_nombre(e["entrada_texto"])
        elif evento.key == pygame.K_BACKSPACE:
            e["entrada_texto"] = e["entrada_texto"][:-1]
        else:
            e["entrada_texto"] += evento.unicode


def manejar_tecla_juego(evento):
    if e["respondio"]:
        return 

    if evento.key == pygame.K_RETURN:
        confirmar_respuesta()
    elif evento.key == pygame.K_BACKSPACE:
        e["texto_usuario"] = e["texto_usuario"][:-1]
    else:
        e["texto_usuario"] += evento.unicode


def confirmar_respuesta():
    juego.evaluar_respuesta(e["texto_usuario"])
    if e["respuesta_correcta"]:
        sonido_correcto.play()
    else:
        sonido_incorrecto.play()


def manejar_click(pos):
    boton        = recursos["boton_confirmar"]
    juego_activo = len(e["jugadores"]) == e["cantidad_jugadores"]
    if juego_activo and not e["respondio"] and boton.collidepoint(pos):
        confirmar_respuesta()


def avanzar_si_corresponde():
    if not e["respondio"]:
        return

    tiempo_transcurrido = pygame.time.get_ticks() - e["tiempo_respuesta"]
    if tiempo_transcurrido > 1000:
        termino = juego.avanzar()
        if termino:
            stats = juego.calcular_estadisticas()
            mostrar_resultados(pantalla, recursos, e["jugadores"], stats)


# ── Loop principal ────────────────────────────────────────────────────────────
while True:
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            en_configuracion = (
                e["cantidad_jugadores"] == 0
                or len(e["jugadores"]) < e["cantidad_jugadores"]
            )
            if en_configuracion:
                manejar_tecla_configuracion(evento)
            else:
                manejar_tecla_juego(evento)

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            manejar_click(pygame.mouse.get_pos())

        if evento.type == EVENTO_TIMER:
            juego_activo = len(e["jugadores"]) == e["cantidad_jugadores"]
            if juego_activo:
                juego.actualizar_tiempo()

    # ── Avance de turno ───────────────────────────────────────────────────────
    juego_activo = len(e["jugadores"]) == e["cantidad_jugadores"]
    if juego_activo:
        avanzar_si_corresponde()
        juego.animar_profesora()

    # ── Dibujo ────────────────────────────────────────────────────────────────
    if e["cantidad_jugadores"] == 0:
        dibujar_pantalla_cantidad(pantalla, recursos, e["entrada_texto"], e["error_mensaje"])

    elif len(e["jugadores"]) < e["cantidad_jugadores"]:
        dibujar_pantalla_nombres(pantalla, recursos, e["jugadores"], e["entrada_texto"], e["error_mensaje"])

    else:
        dibujar_sala(pantalla, recursos,
                     e["pregunta_actual"], e["texto_usuario"],
                     e["segundos_restantes"], e["jugadores"],
                     e["jugador_actual"], e["intentos_restantes"],
                     e["respondio"], e["respuesta_correcta"])

        dibujar_profesora(pantalla, recursos, e["respondio"], e["respuesta_correcta"], e["pos_x_profesora"])

    pygame.display.flip()
    clock.tick(FPS)