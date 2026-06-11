import pygame
import sys

from config import (
    ANCHO, ALTO,
    NEGRO, BLANCO, ROSACLARO, VERDE, ROJO, VERDEPIZARRON,
    IMG_FONDO, IMG_MENU, IMG_END,
    IMG_PROFE, IMG_PROFE_B, IMG_PROFE_M,
)
from preguntas import SALAS


# ── Carga de recursos ────────────────────────────────────────────────────────

def cargar_recursos(fuente):
    recursos = {} #recursos es un diccionario para poder organizar mejor el codigo

    recursos["fondo"]     = cargar(IMG_FONDO, (ANCHO, ALTO))
    recursos["fondomenu"] = cargar(IMG_MENU,  (ANCHO + 50, ALTO + 100))
    recursos["fondoend"]  = cargar(IMG_END,   (ANCHO, ALTO))

    tam_profe = (550, 650)

    recursos["profesora"]     = cargar(IMG_PROFE,   tam_profe)
    recursos["profesorabien"] = cargar(IMG_PROFE_B, tam_profe)
    recursos["profesoramal"]  = cargar(IMG_PROFE_M, tam_profe)

    recursos["boton_confirmar"] = pygame.Rect(100, 240, 200, 50)
    recursos["fuente"]          = fuente

    return recursos


def cargar(ruta, tamanio): #cargar es una funcion que ayuda para no tener que hacer lo de abajo 20 veces por cada imagen
    imagen = pygame.image.load(ruta)
    return pygame.transform.scale(imagen, tamanio)


# ── Pantallas de configuracion ───────────────────────────────────────────────

def dibujar_pantalla_cantidad(pantalla, recursos, entrada_texto, error_mensaje): # primera pantalla, donde se muestra la cantidad de jugadores
    pantalla.fill(ROSACLARO)                                                     # que va a haber 
    pantalla.blit(recursos["fondomenu"], (-50, 10))

    fuente = recursos["fuente"] # esto se hace para hacer mas legible el codigo

    txt1 = fuente.render("Ingrese la cantidad de jugadores (1 a 10):", True, NEGRO)
    pantalla.blit(txt1, (150, 150)) 

    pygame.draw.rect(pantalla, BLANCO, (200, 200, 400, 40))
    txt2 = fuente.render(entrada_texto, True, NEGRO)
    pantalla.blit(txt2, (380, 205))

    if len(error_mensaje) > 0: #se verifica si hay un error
        err = fuente.render(error_mensaje, True, ROJO) # si lo hay se dibuja en rojo
        pantalla.blit(err, (175, 250)) # se posiciona el error en la pantalla


def dibujar_pantalla_nombres(pantalla, recursos, jugadores, entrada_texto, error_mensaje):
    pantalla.fill(ROSACLARO)
    pantalla.blit(recursos["fondomenu"], (-50, 10))

    fuente  = recursos["fuente"]
    numero  = len(jugadores) + 1 # Le sumo 1 porque necesito mostrar el número del próximo jugador que voy a cargar.

    txt1 = fuente.render(f"Jugador {numero}, ingrese su nombre:", True, NEGRO)
    pantalla.blit(txt1, (225, 150))

    pygame.draw.rect(pantalla, BLANCO, (200, 200, 400, 40))
    txt2 = fuente.render(entrada_texto, True, NEGRO)
    pantalla.blit(txt2, (200, 200))

    if len(error_mensaje) > 0:
        err = fuente.render(error_mensaje, True, ROJO)
        pantalla.blit(err, (215, 250))


# ── Pantalla de juego ────────────────────────────────────────────────────────

def dibujar_sala(pantalla, recursos, pregunta_actual, texto_usuario,
                 segundos_restantes, jugadores, jugador_actual,
                 intentos_restantes, respondio, respuesta_correcta):
    pantalla.fill(ROSACLARO)
    pantalla.blit(recursos["fondo"], (0, 0))

    fuente  = recursos["fuente"]
    sala    = SALAS[pregunta_actual] 
    jugador = jugadores[jugador_actual]

    # Pregunta
    texto_preg = fuente.render(sala["pregunta"], True, BLANCO)
    pantalla.blit(texto_preg, (100, 100))

    # Campo de respuesta
    pygame.draw.rect(pantalla, BLANCO, (100, 180, 200, 40))
    input_render = fuente.render(texto_usuario, True, VERDEPIZARRON)
    pantalla.blit(input_render, (110, 185))

    # Tiempo
    reloj_txt = fuente.render(f"Tiempo: {segundos_restantes}s", True, ROJO)
    pantalla.blit(reloj_txt, (350, 160))

    # Turno
    turno_txt = fuente.render(f"Turno de: {jugador['nombre']}", True, BLANCO)
    pantalla.blit(turno_txt, (350, 210))

    # Intentos
    intentos_txt = fuente.render(f"Intentos: {intentos_restantes}", True, BLANCO)
    pantalla.blit(intentos_txt, (350, 260))

    # Resultado de la respuesta
    if respondio == True:
        if respuesta_correcta == True:
            msg   = "¡Correcto!"
            color = VERDE
        else:
            msg   = "Incorrecto"
            color = ROJO
        txt = fuente.render(msg, True, color)
        pantalla.blit(txt, (145, 300))

    # Boton confirmar
    dibujar_boton(pantalla, recursos)


def dibujar_boton(pantalla, recursos):
    boton  = recursos["boton_confirmar"]
    fuente = recursos["fuente"]
    pygame.draw.rect(pantalla, VERDE, boton, border_radius=10)
    texto = fuente.render("Confirmar", True, BLANCO)
    pantalla.blit(texto, (boton.x + 40, boton.y + 10))


def dibujar_profesora(pantalla, recursos, respondio, respuesta_correcta, pos_x_profesora):
    if respondio == True:
        if respuesta_correcta == True:
            pantalla.blit(recursos["profesorabien"], (300, 150))
        else:
            pantalla.blit(recursos["profesoramal"], (300, 150))
    else:
        pantalla.blit(recursos["profesora"], (int(pos_x_profesora), 150))


# ── Pantalla de resultados ───────────────────────────────────────────────────

def mostrar_resultados(pantalla, recursos, jugadores, stats):
    pantalla.fill(ROSACLARO)
    pantalla.blit(recursos["fondoend"], (0, 0))

    fuente = recursos["fuente"]

    # Título
    titulo = fuente.render("Puntajes Finales", True, BLANCO)
    pantalla.blit(titulo, (300, 30))

    # Encabezado de la tabla
    encabezado = fuente.render("Jugador   /   Salas   / Total / Estado", True, BLANCO)
    pantalla.blit(encabezado, (185, 80))
    pos_y = 130

    for jugador in jugadores:

        salas_txt = ""
        for puntaje in jugador["puntajes_sala"]:
            salas_txt += str(puntaje) + " "

        if jugador["completo"] == True:
            estado_txt = "Completo"
        else:
            estado_txt = "No completo"

        linea = fuente.render(
            f"{jugador['nombre']} / {salas_txt} / {jugador['puntos']} / {estado_txt}",
            True,
            BLANCO
        )

        pantalla.blit(linea, (180, pos_y))
        pos_y += 30
        

    
    
    pos_x = 185
    # Mayor puntaje
    pantalla.blit(fuente.render("Mayor puntaje:", True, BLANCO), (185, 300))
    for nombre in stats["ganadores_puntaje"]:
        pantalla.blit(fuente.render(nombre, True, VERDE), (pos_x, 340))
        pos_x += 70
        
    pos_x = 185
    # Mas salas superadas
    pantalla.blit(fuente.render("Mas salas superadas:", True, BLANCO), (185, 380))
    for nombre in stats["ganadores_salas"]:
        pantalla.blit(fuente.render(nombre, True, VERDE), (pos_x, 420))
        pos_x += 70
        
    pos_x = 185
    # No superaron la primera sala
    pantalla.blit(fuente.render("No pasaron la primera sala:", True, BLANCO), (185, 460))
    for nombre in stats["no_pasaron_primera"]:
        pantalla.blit(fuente.render(nombre, True, ROJO), (pos_x, 500))
        pos_x += 70
       

    pygame.display.flip()
    pygame.time.wait(10000)
    pygame.quit()
    sys.exit()
