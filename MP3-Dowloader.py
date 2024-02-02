#!/usr/bin/env python3
import customtkinter
import webbrowser
import _bootlocale
from pytube import YouTube
from PIL import Image
import os

contador = 1
row = 0

# Centramos la ventana al medio de la pantalla
def centrarVentana(app):
    
    app.update_idletasks()
    ancho = 1000
    alto = 600
    x_ubicacion = (app.winfo_screenwidth() - ancho) // 2
    y_ubicacion = (app.winfo_screenheight() - alto) // 2
    app.geometry(f'{ancho}x{alto}+{x_ubicacion}+{y_ubicacion}')
    app.resizable(width=False, height=False)
    app.title('Free Music Downloader')

# Personalizamos los botones, etiquetas, ...etc
def customWidgets(app):
    
    # Etiquetas
    bienvenida = customtkinter.CTkLabel(app, text='Bienvenid@s', font=('transparent', 20))
    bienvenida.place(relx=0.488, rely=0.05, anchor=customtkinter.CENTER)

    funcionamiento = customtkinter.CTkLabel(app, text='Solo hay que escribir la URL de Youtube debajo y darle a descargar, ¡Así de sencillo!', font=('transparent', 14))
    funcionamiento.place(relx=0.488, rely=0.12, anchor=customtkinter.CENTER)

    donaciones = customtkinter.CTkLabel(app, text='Gratis y sin anuncios, se aceptan donaciones ¡GRACIAS!', font=('transparent', 14))
    donaciones.place(relx=0.25, rely=0.96, anchor=customtkinter.CENTER)

    # Boton
    descargar = customtkinter.CTkButton(app, text='DESCARGAR', command=on_Click)
    descargar.place(relx=0.488, rely=0.3, anchor=customtkinter.CENTER)

    donar = customtkinter.CTkButton(app, text='DONAR', command=donate)
    donar.place(relx=0.52, rely=0.96, anchor=customtkinter.CENTER)

def on_Click():

    global contador
    global row

    if entry.get():
        try:
            # Crea una instancia del objeto YouTube
            video = YouTube(entry.get())
            
            # Obtener el título del video
            video_title = video.title
            
            # Selecciona la mejor calidad de audio disponible
            audio_stream = video.streams.filter(only_audio=True, file_extension='mp4').first()
            
            # Descargar el audio
            audio_stream.download(output_path='MisCanciones')

            # Renombrar el archivo descargado con el título del video
            downloaded_file = audio_stream.default_filename
            new_file_path = os.path.join('MisCanciones', f'{video_title}.mp3')
            os.rename(os.path.join('MisCanciones', downloaded_file), new_file_path)

            text = f'Descarga completada! - {video_title}'

            descargado = customtkinter.CTkLabel(music, text=text, font=('transparent', 12))
            descargado.grid(row=row, column=0, padx=20)
            
            contador += 1
            row += 1
        except Exception as RegexMathError:
            pass

def donate():
    # Abrir la URL en el navegador web
    webbrowser.open('https://paypal.me/altf4sh?country.x=ES&locale.x=es_ES')

# Inicio de la aplicación
if __name__ == '__main__':

    app = customtkinter.CTk()
    centrarVentana(app)
    customWidgets(app)

    # Frame
    music = customtkinter.CTkScrollableFrame(app, width=700, height=300)
    music.place(relx=0.488, rely=0.65, anchor=customtkinter.CENTER)

    # Entrada de datos
    entry = customtkinter.CTkEntry(app, placeholder_text='URL Youtube', width=650)
    entry.place(relx=0.488, rely=0.2, anchor=customtkinter.CENTER)

    app.mainloop()