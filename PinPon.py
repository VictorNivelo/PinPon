import pygame
import random

pygame.init()

ANCHO, ALTO = 800, 600
ANCHO_PALETA, ALTO_PALETA = 15, 90
TAMANO_PELOTA = 15
FPS = 60
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 120, 255)
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ping Pong")
reloj = pygame.time.Clock()

controles = {
    "Jugador 1 Arriba": pygame.K_w,
    "Jugador 1 Abajo": pygame.K_s,
    "Jugador 2 Arriba": pygame.K_UP,
    "Jugador 2 Abajo": pygame.K_DOWN,
    "Pausa": pygame.K_ESCAPE,
}


class Paleta:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ANCHO_PALETA, ALTO_PALETA)
        self.velocidad = 5

    def mover(self, arriba=True):
        if arriba:
            self.rect.y -= self.velocidad
        else:
            self.rect.y += self.velocidad
        self.rect.clamp_ip(pantalla.get_rect())

    def dibujar(self):
        pygame.draw.rect(pantalla, AZUL, self.rect, border_radius=10)


class Pelota:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TAMANO_PELOTA, TAMANO_PELOTA)
        self.dx = random.choice([-5, 5])
        self.dy = random.randint(-4, 4)

    def mover(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.top <= 0 or self.rect.bottom >= ALTO:
            self.dy = -self.dy

    def dibujar(self):
        pygame.draw.circle(pantalla, BLANCO, self.rect.center, TAMANO_PELOTA // 2)


def menu_principal():
    fuente = pygame.font.Font(None, 74)
    fuente_pequeña = pygame.font.Font(None, 36)
    seleccion = 0
    opciones = ["Jugar", "Controles", "Salir"]
    while True:
        pantalla.fill(NEGRO)
        texto_titulo = fuente.render("Ping Pong", True, BLANCO)
        pantalla.blit(
            texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTO // 4)
        )
        for i, opcion in enumerate(opciones):
            color = BLANCO if i == seleccion else (150, 150, 150)
            texto_opcion = fuente_pequeña.render(opcion, True, color)
            pantalla.blit(
                texto_opcion,
                (ANCHO // 2 - texto_opcion.get_width() // 2, ALTO // 2 + i * 50),
            )
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                if evento.key == pygame.K_RETURN:
                    if seleccion == 0:
                        return
                    elif seleccion == 1:
                        personalizar_controles()
                    elif seleccion == 2:
                        pygame.quit()
                        return
        pygame.display.flip()
        reloj.tick(FPS)


def personalizar_controles():
    fuente = pygame.font.Font(None, 36)
    fuente_Titulo = pygame.font.Font(None, 46)
    fuente_instrucciones = pygame.font.Font(None, 26)
    controles_orden = [
        "Jugador 1 Arriba",
        "Jugador 1 Abajo",
        "Jugador 2 Arriba",
        "Jugador 2 Abajo",
        "Pausa",
    ]
    seleccion = 0
    esperando_tecla = False
    gris_claro = (200, 200, 200)
    while True:
        pantalla.fill(NEGRO)
        texto_titulo = fuente_Titulo.render("Personalizar Controles", True, BLANCO)
        pantalla.blit(
            texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTO // 6)
        )
        for i, control in enumerate(controles_orden):
            color = AZUL if i == seleccion else BLANCO
            texto = f"{control}: {pygame.key.name(controles[control])}"
            if esperando_tecla and i == seleccion:
                texto = f"{control}: Presiona una tecla..."
            texto_renderizado = fuente.render(texto, True, color)
            pantalla.blit(
                texto_renderizado,
                (ANCHO // 2 - texto_renderizado.get_width() // 2, ALTO // 3 + i * 50),
            )
        texto_instruccion = fuente_instrucciones.render(
            "Presiona ENTER para personalizar", True, gris_claro
        )
        pantalla.blit(
            texto_instruccion,
            (ANCHO // 2 - texto_instruccion.get_width() // 2, ALTO - 100),
        )
        texto_volver = fuente_instrucciones.render(
            "Presiona ESC para volver", True, gris_claro
        )
        pantalla.blit(
            texto_volver, (ANCHO // 2 - texto_volver.get_width() // 2, ALTO - 60)
        )
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if esperando_tecla:
                    controles[controles_orden[seleccion]] = evento.key
                    esperando_tecla = False
                else:
                    if evento.key == pygame.K_UP:
                        seleccion = (seleccion - 1) % len(controles_orden)
                    elif evento.key == pygame.K_DOWN:
                        seleccion = (seleccion + 1) % len(controles_orden)
                    elif evento.key == pygame.K_RETURN:
                        esperando_tecla = True
                    elif evento.key == pygame.K_ESCAPE:
                        return
        pygame.display.flip()


def menu_pausa():
    fuente = pygame.font.Font(None, 74)
    fuente_pequeña = pygame.font.Font(None, 36)
    seleccion = 0
    opciones = ["Reanudar", "Reiniciar", "Salir al menu principal"]
    while True:
        pantalla.fill(NEGRO)
        texto_titulo = fuente.render("Pausa", True, BLANCO)
        pantalla.blit(
            texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTO // 4)
        )
        for i, opcion in enumerate(opciones):
            color = BLANCO if i == seleccion else (150, 150, 150)
            texto_opcion = fuente_pequeña.render(opcion, True, color)
            pantalla.blit(
                texto_opcion,
                (ANCHO // 2 - texto_opcion.get_width() // 2, ALTO // 2 + i * 50),
            )
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return "salir"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                if evento.key == pygame.K_RETURN:
                    if seleccion == 0:
                        return "reanudar"
                    elif seleccion == 1:
                        return "reiniciar"
                    elif seleccion == 2:
                        return "menu_principal"
        pygame.display.flip()
        reloj.tick(FPS)


def jugar():
    jugador1 = Paleta(20, ALTO // 2 - ALTO_PALETA // 2)
    jugador2 = Paleta(ANCHO - 20 - ANCHO_PALETA, ALTO // 2 - ALTO_PALETA // 2)
    pelota = Pelota(ANCHO // 2 - TAMANO_PELOTA // 2, ALTO // 2 - TAMANO_PELOTA // 2)
    puntuacion1, puntuacion2 = 0, 0
    meta = 5
    fuente = pygame.font.Font(None, 74)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
        teclas = pygame.key.get_pressed()
        if teclas[controles["Jugador 1 Arriba"]]:
            jugador1.mover(arriba=True)
        if teclas[controles["Jugador 1 Abajo"]]:
            jugador1.mover(arriba=False)
        if teclas[controles["Jugador 2 Arriba"]]:
            jugador2.mover(arriba=True)
        if teclas[controles["Jugador 2 Abajo"]]:
            jugador2.mover(arriba=False)
        pelota.mover()
        if pelota.rect.colliderect(jugador1.rect) or pelota.rect.colliderect(
            jugador2.rect
        ):
            pelota.dx = -pelota.dx
            pelota.dy = random.randint(-4, 4)
        if pelota.rect.left <= 0:
            puntuacion2 += 1
            pelota = Pelota(
                ANCHO // 2 - TAMANO_PELOTA // 2, ALTO // 2 - TAMANO_PELOTA // 2
            )
        if pelota.rect.right >= ANCHO:
            puntuacion1 += 1
            pelota = Pelota(
                ANCHO // 2 - TAMANO_PELOTA // 2, ALTO // 2 - TAMANO_PELOTA // 2
            )
        if teclas[controles["Pausa"]]:
            opcion = menu_pausa()
            if opcion == "menu_principal":
                return "menu_principal"
            elif opcion == "salir":
                return "salir"
            elif opcion == "reiniciar":
                return "reiniciar"
        pantalla.fill(NEGRO)
        jugador1.dibujar()
        jugador2.dibujar()
        pelota.dibujar()
        texto_puntuacion = fuente.render(
            f"{puntuacion1}  -  {puntuacion2}", True, BLANCO
        )
        pantalla.blit(
            texto_puntuacion, (ANCHO // 2 - texto_puntuacion.get_width() // 2, 20)
        )
        pygame.display.flip()
        reloj.tick(FPS)
        if puntuacion1 == meta or puntuacion2 == meta:
            pantalla.fill(NEGRO)
            texto_meta = fuente.render("Fin del Juego", True, BLANCO)
            pantalla.blit(
                texto_meta, (ANCHO // 2 - texto_meta.get_width() // 2, ALTO // 2 - 30)
            )
            pygame.display.flip()
            pygame.time.delay(2000)
            return "menu_principal"


def main():
    while True:
        menu_principal()
        while True:
            resultado = jugar()
            if resultado == "menu_principal":
                break
            elif resultado == "salir":
                pygame.quit()
                return


if __name__ == "__main__":
    main()
    pygame.quit()
