from tkinter import Tk, Label, Button, Entry, Frame, Scrollbar, Canvas, messagebox
import webbrowser
import os
import yt_dlp
import re

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

# Validar URL de YouTube
def validar_url(url):
    patron = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'
    return re.match(patron, url)

# Crear botones redondeados
def crear_boton_redondeado(canvas, x, y, width, height, text, command, bg, fg, hover_bg):
    # Crear las partes del botón
    rect_id = canvas.create_oval(x, y, x + height, y + height, fill=bg, outline="")
    right_oval_id = canvas.create_oval(x + width - height, y, x + width, y + height, fill=bg, outline="")
    rect_middle_id = canvas.create_rectangle(x + height // 2, y, x + width - height // 2, y + height, fill=bg, outline="")
    text_id = canvas.create_text(x + width // 2, y + height // 2, text=text, fill=fg, font=('Arial', 12))

    # Lista para agrupar elementos del botón
    button_ids = [rect_id, right_oval_id, rect_middle_id, text_id]

    # Función para manejar el hover
    def on_enter(event=None):
        for item in button_ids[:-1]:  # Cambiar solo las formas, no el texto
            canvas.itemconfig(item, fill=hover_bg)

    def on_leave(event=None):
        for item in button_ids[:-1]:
            canvas.itemconfig(item, fill=bg)

    # Vincular eventos de hover
    for item in button_ids:
        canvas.tag_bind(item, "<Enter>", on_enter)
        canvas.tag_bind(item, "<Leave>", on_leave)
        canvas.tag_bind(item, "<Button-1>", lambda e: command())

# Personalizamos los botones, etiquetas, ...etc
def customWidgets(app):
    # Colores
    app.configure(bg='#1e1e2f')
    label_color = '#f8f8f2'

    # Etiquetas
    bienvenida = Label(app, text='Bienvenidos', font=('Arial', 20), bg='#1e1e2f', fg=label_color)
    bienvenida.place(relx=0.488, rely=0.05, anchor='center')

    funcionamiento = Label(app, text='Solo hay que escribir la URL de Youtube debajo y darle a descargar, ¡Así de sencillo!', font=('Arial', 14), bg='#1e1e2f', fg=label_color)
    funcionamiento.place(relx=0.488, rely=0.12, anchor='center')

    donaciones = Label(app, text='Gratis y sin anuncios, se aceptan donaciones ¡GRACIAS!', font=('Arial', 14), bg='#1e1e2f', fg=label_color)
    donaciones.place(relx=0.25, rely=0.96, anchor='center')

    # Botones redondeados
    crear_boton_redondeado(canvas, 380, 160, 200, 40, "DESCARGAR", on_Click, "#6272a4", "#f8f8f2", "#44475a")
    crear_boton_redondeado(canvas, 500, 550, 120, 40, "DONAR", donate, "#6272a4", "#f8f8f2", "#44475a")

def on_Click():
    global contador
    global row

    url = entry.get()
    if not url:
        messagebox.showerror("Error", "Por favor, ingrese una URL.")
        return

    if not validar_url(url):
        messagebox.showerror("Error", "URL no válida. Por favor, ingrese una URL de YouTube válida.")
        return

    try:
        # Crear la carpeta si no existe
        if not os.path.exists('MisCanciones'):
            os.makedirs('MisCanciones')

        # Configuración de yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'MisCanciones/%(title)s.%(ext)s',
        }

        # Descargar el audio usando yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=True)

        title = result.get('title', 'Audio')
        text = f'{title} - Descarga completa'

        descargado = Label(content_frame, text=text, font=('Arial', 12), bg='#282a36', fg='#50fa7b')
        descargado.grid(row=row, column=0, padx=20, pady=5, sticky='w')

        contador += 1
        row += 1

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al descargar: {str(e)}")

def donate():
    # Abrir la URL en el navegador web
    webbrowser.open('https://paypal.me/altf4sh?country.x=ES&locale.x=es_ES')

def actualizar_scrollbar():
    """Actualizar la visibilidad del scrollbar en función del tamaño del contenido."""
    canvas.update_idletasks()
    bbox = canvas.bbox("all")  # Obtener los límites del contenido
    if bbox:
        content_height = bbox[3] - bbox[1]  # Altura del contenido
        visible_height = canvas.winfo_height()  # Altura visible del canvas
        if content_height > visible_height:
            scrollbar.place(relx=0.84, rely=0.65, anchor='center', height=300)  # Mostrar scrollbar
        else:
            scrollbar.place_forget()  # Ocultar scrollbar si no es necesario

# Inicio de la aplicación
if __name__ == '__main__':
    app = Tk()
    centrarVentana(app)
    
    # Canvas para botones redondeados
    canvas = Canvas(app, bg="#1e1e2f", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    
    
    customWidgets(app)

    # Frame con scrollbar para mostrar canciones descargadas
    canvas = Canvas(app, bg='#282a36', highlightthickness=0)
    scrollbar = Scrollbar(app, orient='vertical', bg='#44475a', troughcolor='#282a36', activebackground='#6272a4', command=canvas.yview)
    scrollable_frame = Frame(canvas, bg='#282a36')

    scrollable_frame.bind(
        "<Configure>",
        lambda e: [
            canvas.configure(scrollregion=canvas.bbox("all")),
            actualizar_scrollbar()  # Comprobar si el scrollbar es necesario
        ]
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.place(relx=0.488, rely=0.65, anchor='center', width=700, height=300)

    content_frame = scrollable_frame

    # Entrada de datos
    entry = Entry(app, width=80, bg='#44475a', fg='#f8f8f2', font=('Arial', 12), insertbackground='#f8f8f2', highlightbackground='#1e1e2f', highlightthickness=0, bd=0)
    entry.place(relx=0.488, rely=0.2, anchor='center')

    app.mainloop()
