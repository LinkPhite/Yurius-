import os
import time
import threading
import warnings
import glob

# Silenciamos todos los avisos de Pygame y Flet
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
warnings.filterwarnings("ignore")

import pygame
import flet as ft

pygame.mixer.init()

CARPETA_MUSICA = "Musica"

def main(page: ft.Page):
    page.title = "Yurius"
    
    if hasattr(page, "window"):
        page.window.width = 400
        page.window.height = 700
    else:
        page.window_width = 400
        page.window_height = 700

    page.theme_mode = "dark"
    page.bgcolor = "#0f1115"
    page.padding = 20

    state = {
        "lista_actual": [],
        "indice_actual": 0,
        "duracion_total": 0
    }

    # --- ELEMENTOS DE LA INTERFAZ ---
    texto_titulo = ft.Text("", size=22, weight="bold")
    texto_artista = ft.Text("", size=14, color="grey")
    img_portada = ft.Container(width=250, height=250, bgcolor="#1b1f27", border_radius=15)
    
    # Barra de progreso y tiempos
    slider = ft.Slider(min=0, max=100, value=0, active_color="blue")
    tiempo_actual = ft.Text("00:00", size=12, color="grey")
    tiempo_total = ft.Text("00:00", size=12, color="grey")

    def formatear_tiempo(segundos):
        mins = int(segundos // 60)
        segs = int(segundos % 60)
        return f"{mins:02d}:{segs:02d}"

    # HILO DE TIEMPO (CORREGIDO PARA QUE NO SE CONGELE)
    def actualizar_progreso():
        while True:
            try:
                if pygame.mixer.music.get_busy():
                    pos_actual = pygame.mixer.music.get_pos() / 1000 
                    if pos_actual >= 0 and state["duracion_total"] > 0:
                        slider.value = (pos_actual / state["duracion_total"]) * 100
                        tiempo_actual.value = formatear_tiempo(pos_actual)
                        # Actualizamos solo estos dos componentes directo, sin pedirle permiso a la página entera
                        slider.update()
                        tiempo_actual.update()
            except:
                pass
            time.sleep(1) # Espera 1 segundo y vuelve a actualizar

    threading.Thread(target=actualizar_progreso, daemon=True).start()

    def reproducir_cancion():
        ruta = state["lista_actual"][state["indice_actual"]]
        nombre_archivo = os.path.basename(ruta)
        
        pygame.mixer.music.load(ruta)
        sonido = pygame.mixer.Sound(ruta)
        state["duracion_total"] = sonido.get_length()
        
        pygame.mixer.music.play()
        
        texto_titulo.value = nombre_archivo.rsplit('.', 1)[0]
        tiempo_total.value = formatear_tiempo(state["duracion_total"])
        
        carpeta = os.path.dirname(ruta)
        portada = None
        for ext in ("*.jpg", "*.png", "*.jpeg"):
            archivos = glob.glob(os.path.join(carpeta, ext))
            if archivos:
                portada = archivos[0]
                break
        
        if portada:
            img_portada.content = ft.Image(src=os.path.abspath(portada), fit="cover", border_radius=15)
        else:
            img_portada.content = ft.Text("🎵", size=80)
            img_portada.alignment = ft.alignment.center
            
        page.update()

    def siguiente(e):
        if state["indice_actual"] < len(state["lista_actual"]) - 1:
            state["indice_actual"] += 1
            reproducir_cancion()

    def anterior(e):
        if state["indice_actual"] > 0:
            state["indice_actual"] -= 1
            reproducir_cancion()

    def retroceder(e):
        if len(page.views) > 1:
            page.views.pop()
            page.update()

    # Función para crear botones 100% visibles y a prueba de errores
    def crear_boton(texto, funcion, color_fondo="#1b1f27"):
        return ft.Container(
            content=ft.Text(texto, weight="bold", color="white"),
            bgcolor=color_fondo,
            padding=15,
            border_radius=8,
            ink=True,
            on_click=funcion
        )

    # --- VISTA DEL REPRODUCTOR ---
    def ir_al_reproductor(lista, indice):
        state["lista_actual"] = lista
        state["indice_actual"] = indice
        reproducir_cancion()
        
        view_player = ft.View(
            route="/player",
            bgcolor="#0f1115",
            controls=[
                ft.Container(content=ft.Text("⬅ VOLVER", color="grey", size=14, weight="bold"), on_click=retroceder, padding=10, ink=True),
                ft.Container(height=10),
                ft.Row([img_portada], alignment="center"),
                ft.Container(height=20),
                texto_titulo,
                texto_artista,
                ft.Container(height=10),
                
                # Barra de tiempo
                ft.Column([
                    slider,
                    ft.Row([tiempo_actual, tiempo_total], alignment="spaceBetween")
                ]),
                
                ft.Container(height=20),
                
                # CONTROLES (Ahora son botones de colores grandes con texto claro)
                ft.Row([
                    crear_boton("<< ANT", anterior),
                    crear_boton("► PLAY", lambda _: pygame.mixer.music.unpause(), "green"),
                    crear_boton("|| PAUSA", lambda _: pygame.mixer.music.pause(), "red"),
                    crear_boton("SIG >>", siguiente),
                ], alignment="center", wrap=True)
            ]
        )
        page.views.append(view_player)
        page.update()

    # --- NAVEGACIÓN DE CARPETAS ---
    def listar_archivos(ruta):
        elementos = os.listdir(ruta)
        carpetas = []
        canciones = []
        
        for item in elementos:
            full_path = os.path.join(ruta, item)
            if os.path.isdir(full_path):
                carpetas.append(item)
            elif item.lower().endswith((".mp3", ".flac", ".wav")):
                canciones.append(full_path)
        
        ui_elementos = [ft.Text(f"📁 Carpetas", size=16, color="blue")]
        for c in carpetas:
            ui_elementos.append(
                ft.Container(
                    content=ft.Text(f"  📂 {c}"),
                    on_click=lambda e, path=os.path.join(ruta, c): abrir_menu(path),
                    padding=10, bgcolor="#1b1f27", border_radius=10, ink=True
                )
            )
            
        ui_elementos.append(ft.Container(height=10))
        ui_elementos.append(ft.Text(f"🎵 Canciones", size=16, color="green"))
        for i, cancion in enumerate(canciones):
            nombre = os.path.basename(cancion)
            ui_elementos.append(
                ft.Container(
                    content=ft.Text(f"  🎶 {nombre}"),
                    on_click=lambda e, l=canciones, idx=i: ir_al_reproductor(l, idx),
                    padding=10, bgcolor="#1b1f27", border_radius=10, ink=True
                )
            )

        return ui_elementos

    def abrir_menu(ruta):
        nombre_carpeta = os.path.basename(ruta) if ruta != CARPETA_MUSICA else "Biblioteca"
        view = ft.View(
            route=f"/{ruta}",
            bgcolor="#0f1115",
            controls=[
                ft.Row([
                    ft.Container(content=ft.Text("⬅", size=20, weight="bold"), on_click=retroceder, ink=True) if ruta != CARPETA_MUSICA else ft.Container(),
                    ft.Text(nombre_carpeta, size=24, weight="bold")
                ]),
                ft.Divider(color="grey"),
                ft.Column(listar_archivos(ruta), scroll="auto", expand=True)
            ]
        )
        page.views.append(view)
        page.update()

    if not os.path.exists(CARPETA_MUSICA): os.makedirs(CARPETA_MUSICA)
    abrir_menu(CARPETA_MUSICA)

ft.app(target=main)