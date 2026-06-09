import pygame
from config import MAX_INTENTOS, TIEMPO_LIMITE
from preguntas import SALAS

# ── Estado ────────────────────────────────────────────────────────────────────
estado = {
    "cantidad_jugadores": 0,
    "jugadores":          [],
    "entrada_texto":      "",
    "error_mensaje":      "",
    "pregunta_actual":    0,
    "jugador_actual":     0,
    "intentos_restantes": MAX_INTENTOS,
    "segundos_restantes": TIEMPO_LIMITE,
    "texto_usuario":      "",
    "respondio":          False,
    "respuesta_correcta": False,
    "tiempo_respuesta":   0,
    "pos_x_profesora":    300,
    "dir_profesora":      1,
    "tiempo_inicio":      0,
}


# ── Funciones de configuracion ────────────────────────────────────────────────
def crear_jugador(nombre):
    return {
        "nombre":        nombre,
        "puntos":        0,
        "puntajes_sala": [0] * len(SALAS),
        "completo":      False,
    }


def confirmar_cantidad(texto):
    if not texto.isdigit():
        estado["error_mensaje"] = "Entrada invalida. Ingrese un numero."
        return

    n = int(texto)
    if n < 1 or n > 10:
        estado["error_mensaje"] = "Debe ingresar un numero entre 1 y 10."
        return

    estado["cantidad_jugadores"] = n
    estado["entrada_texto"]      = ""
    estado["error_mensaje"]      = ""


def confirmar_nombre(texto):
    nombre = texto.strip()
    if len(nombre) == 0:
        estado["error_mensaje"] = "El nombre no puede estar vacio."
        return

    estado["jugadores"].append(crear_jugador(nombre))
    estado["entrada_texto"] = ""
    estado["error_mensaje"] = ""

    if len(estado["jugadores"]) == estado["cantidad_jugadores"]:
        estado["tiempo_inicio"] = pygame.time.get_ticks()


# ── Funciones de juego ────────────────────────────────────────────────────────
def evaluar_respuesta(texto):
    if estado["respondio"]:
        return

    respuesta_dada     = texto.lower().strip()
    indice                = estado["pregunta_actual"]
    respuesta_esperada = SALAS[indice]["respuesta"].lower()

    if respuesta_dada == respuesta_esperada:
        jugador = estado["jugadores"][estado["jugador_actual"]]
        puntos  = SALAS[indice]["puntaje"]
        jugador["puntos"]            += puntos
        jugador["puntajes_sala"][indice] = puntos
        estado["respuesta_correcta"]  = True
    else:
        estado["intentos_restantes"] -= 1
        estado["respuesta_correcta"]  = False

    estado["respondio"]        = True
    estado["tiempo_respuesta"] = pygame.time.get_ticks()


def tiempo_agotado():
    if not estado["respondio"]:
        estado["intentos_restantes"] -= 1
        estado["respuesta_correcta"]  = False
        estado["respondio"]           = True
        estado["tiempo_respuesta"]    = pygame.time.get_ticks()


def avanzar():
    # Devuelve True si el juego termino.
    if estado["respuesta_correcta"]:
        estado["pregunta_actual"]    += 1
        estado["intentos_restantes"]  = MAX_INTENTOS

        if estado["pregunta_actual"] >= len(SALAS):
            estado["pregunta_actual"] = 0
            return _siguiente_jugador()

    elif estado["intentos_restantes"] <= 0:
        estado["pregunta_actual"]    = 0
        estado["intentos_restantes"] = MAX_INTENTOS
        return _siguiente_jugador()

    _reiniciar_turno()
    return False


def _siguiente_jugador():
    # Devuelve True si el juego termino.
    estado["jugador_actual"] += 1

    if estado["jugador_actual"] >= len(estado["jugadores"]):
        _calcular_completos()
        return True

    _reiniciar_turno()
    return False


def _reiniciar_turno():
    estado["respondio"]          = False
    estado["respuesta_correcta"] = False
    estado["segundos_restantes"] = TIEMPO_LIMITE
    estado["tiempo_inicio"]      = pygame.time.get_ticks()


def _calcular_completos():
    for jugador in estado["jugadores"]:
        jugador["completo"] = all(p != 0 for p in jugador["puntajes_sala"])


def actualizar_tiempo():
    # Devuelve True si se agoto el tiempo.
    transcurrido = (pygame.time.get_ticks() - estado["tiempo_inicio"]) // 1000
    estado["segundos_restantes"] = max(TIEMPO_LIMITE - transcurrido, 0)

    if estado["segundos_restantes"] <= 0 and not estado["respondio"]:
        tiempo_agotado()
        return True

    return False


def animar_profesora():
    if not estado["respondio"]:
        estado["pos_x_profesora"] += estado["dir_profesora"] * 0.5
        if estado["pos_x_profesora"] > 310 or estado["pos_x_profesora"] < 290:
            estado["dir_profesora"] *= -1


def calcular_estadisticas():
    # Devuelve un diccionario con los resultados finales del juego.
    jugadores = estado["jugadores"]

    max_puntaje = max(j["puntos"] for j in jugadores)

    salas_por_jugador = {
        j["nombre"]: sum(1 for p in j["puntajes_sala"] if p > 0)
        for j in jugadores
    }

    max_salas = max(salas_por_jugador.values())

    ganadores_puntaje  = [j["nombre"] for j in jugadores if j["puntos"] == max_puntaje]
    ganadores_salas    = [n for n, s in salas_por_jugador.items() if s == max_salas]
    no_pasaron_primera = [j["nombre"] for j in jugadores if j["puntajes_sala"][0] == 0]

    return {
        "max_puntaje":        max_puntaje,
        "max_salas":          max_salas,
        "ganadores_puntaje":  ganadores_puntaje,
        "ganadores_salas":    ganadores_salas,
        "no_pasaron_primera": no_pasaron_primera,
    }