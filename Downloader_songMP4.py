from pytube import YouTube
import os
print('MP3 Audio Downloader \n')

rate = int(input('Cuantas canciones vas a descargar (max 20) >>> '))

if rate > 20 or rate < 0:
    print('Out of range')
else:
    for i in range(rate):
        URLs = input('URL de YouTube >>> ')
        
        # Crea una instancia del objeto YouTube
        video = YouTube(URLs)
        
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

        print('Descarga completada!')
