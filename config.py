import pygame

# ─── Ventana ─────────────────────────
ANCHO, ALTO = 800, 600
FPS         = 60
TITULO      = "Final Programacion I"

# ─── Reglas del juego ────────────────────
MAX_INTENTOS   = 2        
TIEMPO_LIMITE  = 20       
MAX_JUGADORES  = 10

# ─── Timer ─────────────
EVENTO_TIMER    = pygame.USEREVENT + 1
INTERVALO_TIMER = 1000    # milisegundos

# ─── Colores ──────────────────────
NEGRO        = (0,   0,   0)
BLANCO       = (255, 255, 255)
ROSACLARO    = (242, 214, 207)
VERDE        = (88,  214, 141)
ROJO         = (231, 76,  60)
VERDEPIZARRON = (35, 86,  45)

# ─── Fuentes ────────────────────────
FUENTE_PATH = "tiza.ttf"
FUENTE_SIZE = 28

# ─── Imagenes ──────────────────
IMG_FONDO    = "pizarron.jpg"
IMG_MENU     = "afuera.jpg"
IMG_END      = "recreo.jpg"
IMG_PROFE    = "profe.png"
IMG_PROFE_B  = "profebien.png"
IMG_PROFE_M  = "profemal.png"

# ─── Sonidos ─────────────────────────────
SND_CORRECTO   = "correcto.wav"
SND_INCORRECTO = "incorrecto.wav"
VOL_INCORRECTO = 0.5
