# Yurius
# Yurius MP3 Player 🎵

Un reproductor de música de escritorio minimalista y moderno, construido en Python. Yurius cuenta con una interfaz de usuario inspirada en reproductores móviles, modo oscuro por defecto y exploración automática de carpetas locales.

## 🚀 Características Principales

* **Interfaz Fluida:** Navegación por vistas con animaciones fluidas, diseñada para sentirse como una app nativa.
* **Lectura Automática:** Escanea automáticamente tu biblioteca y organiza la música por Artista > Álbum > Canción.
* **Detección de Carátulas:** Busca y carga automáticamente imágenes (`.jpg`, `.png`, `.jpeg`) presentes en la carpeta del álbum para mostrarlas en el reproductor.
* **Soporte Multiformato:** Reproduce archivos de audio en formato `.mp3`, `.flac`, `.wav`, `.ogg` y `.m4a`.
* **Controles Completos:** Barra de progreso en tiempo real, Play/Pausa, y salto entre canciones (Siguiente/Anterior) dentro de la misma lista.

## 📦 Descarga e Instalación

No necesitas instalar Python para usar Yurius. 

1. Ve a la pestaña de [Releases](../../releases) de este repositorio.
2. Descarga la última versión del archivo `reproductor.exe`.
3. Coloca el `.exe` en la carpeta donde quieras tener tu música.

## 📁 ¿Cómo organizar tu música?

Para que Yurius lea correctamente tus canciones y menús, **es obligatorio** crear una carpeta llamada `Musica` exactamente en la misma ubicación donde está el archivo `reproductor.exe`.

La estructura recomendada dentro de la carpeta `Musica` es la siguiente:

```text
📁 Directorio del programa
│
├── ⚙️ reproductor.exe (Tu programa)
│
└── 📁 Musica/ (Carpeta principal)
    │
    └── 📁 Galneryus/ (Carpeta de Artista)
        │
        └── 📁 Attitude to Life/ (Carpeta de Álbum)
            ├── 🎵 01 - Cancion.flac
            ├── 🎵 02 - Cancion.flac
            └── 🖼️ caratula.jpg (La imagen se cargará automáticamente)

🛠️ Tecnologías Utilizadas
Python 3: Lenguaje principal.

Flet: Framework utilizado para la Interfaz de Usuario (UI) basada en Flutter, garantizando un diseño moderno y responsivo.

Pygame: Motor utilizado para la carga, decodificación y reproducción fluida de los archivos de audio en segundo plano.

👨‍💻 Autor
Desarrollado por LinkPhite.

