from pytube import YouTube

print('MP4 Audio Downloader \n')

rate = int(input('Cuantas canciones vas a descargar (max 20) >>> '))

if rate > 20 or rate < 0:
    print('Out of range')
else:
    for i in range(rate):
        URLs = input('URL de YouTube >>> ')
        
        # Crea una instancia del objeto YouTube
        video = YouTube(URLs)
        
        # Selecciona la mejor calidad de audio disponible
        audio_stream = video.streams.filter(only_audio=True, file_extension='mp4').first()

        song = input('Nombre de la cacion >>> ')
        
        # Descarga el audio en formato mp4
        audio_stream.download(output_path='MisCanciones', filename=song)

        # Renombra el archivo descargado a formato mp4
        import os
        os.rename('MisCanciones/'+song, 'MisCanciones/'+song+'.mp4')

        print('Descarga completada!')
