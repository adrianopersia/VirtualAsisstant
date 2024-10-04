import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import pywhatkit
import yfinance as yf
import pyjokes
import json
import requests
import os

# Opciones de voz / idioma
id1 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0"
id2 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
id3 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0"

# Archivo de recordatorios
RECORDATORIOS_FILE = "recordatorios.json"
NEWS_API_KEY = "83559c6f31524fb09b2877eff5c77293"
PREFERENCIAS_FILE = "preferencias_usuario.json"


def hablar(mensaje):
    # Encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("voice", id3)  # Cambiar la voz al español
    engine.say(mensaje)
    engine.runAndWait()

def saludo_inicial():
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = "Buenas noches"
    elif 6 <= hora.hour < 13:
        momento = "Buen día"
    else:
        momento = "Buenas tardes"
    
    preferencias = cargar_preferencias()
    nombre = preferencias.get('nombre', 'Usuario')
    
    # Saludo al usuario
    hablar(f"{momento}{nombre}, en qué te puedo ayudar hoy?")

# Informar la hora actual
def pedir_hora():
    hora = datetime.datetime.now()
    hora_formateada = f"En este momento son las {hora.hour} horas con {hora.minute} minutos."
    hablar(hora_formateada)

# Informar el día actual
def pedir_dia():
    dia = datetime.datetime.now()
    dias_semana = {
        0: "Lunes", 1: "Martes", 2: "Miércoles", 
        3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"
    }
    dia_semana = dias_semana[dia.weekday()]
    hablar(f"Hoy es {dia_semana} {dia.day} de {dia.strftime('%B')} de {dia.year}.")

# Función para abrir aplicaciones locales en Windows
def abrir_aplicacion(app):
    aplicaciones = {
        "calculadora": "calc.exe",
        "bloc de notas": "notepad.exe",
        "explorador de archivos": "explorer.exe",
        "cmd": "cmd.exe",
        "Spotify": "spotify.exe"
    }

    if app in aplicaciones:
        os.system(aplicaciones[app])
        hablar(f"Abriendo {app}.")
    else:
        hablar(f"No tengo información sobre la aplicación {app}.")

# Función para cargar las preferencias del usuario
def cargar_preferencias():
    try:
        with open(PREFERENCIAS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Función para guardar las preferencias del usuario
def guardar_preferencias(preferencias):
    with open(PREFERENCIAS_FILE, 'w') as file:
        json.dump(preferencias, file)

# Función para establecer el nombre del usuario
def establecer_nombre(nombre):
    preferencias = cargar_preferencias()
    preferencias['nombre'] = nombre
    guardar_preferencias(preferencias)
    hablar(f"Hola, {nombre}. A partir de ahora te llamaré así.")

# Función para obtener el nombre del usuario
def obtener_nombre():
    preferencias = cargar_preferencias()
    return preferencias.get('nombre', 'Usuario')

# Función para buscar en Wikipedia
def buscar_wikipedia(pedido):
    wikipedia.set_lang("es")
    resultado = wikipedia.summary(pedido, sentences=2)
    hablar("Esto es lo que encontré en Wikipedia.")
    hablar(resultado)

# Función para reproducir noticias en YouTube
def reproducir_noticias_youtube(pedido):
    hablar(f"Reproduciendo noticias sobre {pedido} en YouTube.")
    pywhatkit.playonyt(f"noticias sobre {pedido}")

# Función para consultar precio de acciones
def consultar_precio_accion(empresa):
    cartera = {
        "apple": "AAPL",
        "amazon": "AMZN",
        "google": "GOOGL",
        "tesla": "TSLA"
    }
    
    accion = cartera.get(empresa.lower())
    
    if accion:
        ticker = yf.Ticker(accion)
        info = ticker.info
        
        # Verificar varios posibles campos de precios
        posibles_precios = ['regularMarketPrice', 'ask', 'bid', 'previousClose']
        precio = None
        
        for campo in posibles_precios:
            if campo in info:
                precio = info[campo]
                break
        
        if precio:
            hablar(f"El precio actual de la acción de {empresa} es {precio} dólares.")
        else:
            hablar(f"No pude obtener el precio de la acción de {empresa} en este momento.")
    else:
        hablar(f"No tengo información sobre la empresa {empresa}.")

# Función para contar chistes
def contar_chiste():
    chiste = pyjokes.get_joke("es")  # Obtener un chiste en español
    hablar(chiste)

# Función central para recibir comandos de voz
def transformar_audio_texto():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        print("Escuchando...")
        audio = r.listen(source)
        try:
            comando = r.recognize_google(audio, language="es-ES")
            print(f"Dijiste: {comando}")
            return comando.lower()
        except sr.UnknownValueError:
            hablar("No entendí lo que dijiste, podrías repetirlo?")
            return "No entendido"
        except sr.RequestError:
            hablar("Hubo un problema con el servicio.")
            return "Error"


# Función para cargar recordatorios
def cargar_recordatorios():
    try:
        with open(RECORDATORIOS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Función para guardar recordatorios
def guardar_recordatorios(recordatorios):
    with open(RECORDATORIOS_FILE, 'w') as file:
        json.dump(recordatorios, file)

# Función para agregar un recordatorio
def agregar_recordatorio(tarea, hora):
    recordatorios = cargar_recordatorios()
    recordatorios.append({"tarea": tarea, "hora": hora})
    guardar_recordatorios(recordatorios)
    hablar(f"He agregado un recordatorio para {tarea} a las {hora}.")

# Función para listar recordatorios
def listar_recordatorios():
    recordatorios = cargar_recordatorios()
    if recordatorios:
        hablar("Estos son tus recordatorios:")
        for recordatorio in recordatorios:
            hablar(f"Tarea: {recordatorio['tarea']} a las {recordatorio['hora']}")
    else:
        hablar("No tienes recordatorios pendientes.")

# Función para eliminar un recordatorio
def eliminar_recordatorio(tarea):
    recordatorios = cargar_recordatorios()
    recordatorios = [r for r in recordatorios if r["tarea"] != tarea]
    guardar_recordatorios(recordatorios)
    hablar(f"He eliminado el recordatorio para {tarea}.")

# Función para obtener las últimas noticias
def obtener_noticias(tema):
    url = f"https://newsapi.org/v2/everything?q={tema}&apiKey={NEWS_API_KEY}&language=es"
    response = requests.get(url)
    if response.status_code == 200:
        noticias = response.json().get('articles', [])
        if noticias:
            hablar(f"Estas son algunas noticias sobre {tema}:")
            for i, noticia in enumerate(noticias[:3], start=1):  # Mostrar las primeras 3 noticias
                hablar(f"Noticia {i}: {noticia['title']}")
        else:
            hablar(f"No encontré noticias sobre {tema}.")
    else:
        hablar("No pude obtener las noticias en este momento.")


TMDB_API_KEY = "2d3eec019fc7600b98881216539c4c68"

# Función para buscar película, serie o podcast usando la API de TMDB
def buscar_pelicula_serie(titulo):
    url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={titulo}&language=es-ES"
    response = requests.get(url)
    if response.status_code == 200:
        resultados = response.json()['results']
        if resultados:
            resultado = resultados[0]  # Tomamos el primer resultado
            nombre = resultado.get('title') or resultado.get('name')
            descripcion = resultado.get('overview')
            hablar(f"Encontré {nombre}. {descripcion}")
            return nombre, descripcion
        else:
            hablar("No encontré resultados.")
    else:
        hablar("Hubo un problema al conectarse con el servicio.")

# Inicializar archivo JSON para favoritos
def inicializar_datos():
    if not os.path.exists('datos_entretenimiento.json'):
        with open('datos_entretenimiento.json', 'w') as f:
            json.dump({"favoritos": [], "vistas": []}, f)

# Función para guardar un título como favorito en JSON
def guardar_favorito(titulo):
    with open('datos_entretenimiento.json', 'r') as f:
        datos = json.load(f)
    
    if titulo not in datos["favoritos"]:
        datos["favoritos"].append(titulo)
    
    with open('datos_entretenimiento.json', 'w') as f:
        json.dump(datos, f)

def eliminar_favorito(titulo):
    archivo_favoritos = 'datos_entretenimiento.json'
    
    if not os.path.exists(archivo_favoritos):
        hablar("No tienes ningún favorito guardado.")
        return

    with open(archivo_favoritos, 'r') as f:
        datos = json.load(f)
    
    favoritos = datos.get("favoritos", [])

    favoritos_normalizados = [favorito.lower() for favorito in favoritos]
    titulo_normalizado = titulo.lower()

    print(favoritos)
    print(titulo)
    
    if titulo_normalizado in favoritos_normalizados:
        indice = favoritos_normalizados.index(titulo_normalizado)
        favorito_a_eliminar = favoritos[indice]

        favoritos.remove(favorito_a_eliminar)  
        datos["favoritos"] = favoritos

        with open(archivo_favoritos, 'w') as f:
            json.dump(datos, f, indent=4)
        
        hablar(f"El título '{favorito_a_eliminar}' ha sido eliminado de tus favoritos.")
    else:
        hablar(f"El título '{titulo}' no se encuentra en tu lista de favoritos.")

# Función para listar los favoritos guardados
def listar_favoritos():
    with open('datos_entretenimiento.json', 'r') as f:
        datos = json.load(f)
    favoritos = datos["favoritos"]
    if favoritos:
        hablar("Tus favoritos son: " + ", ".join(favoritos))
    else:
        hablar("No tienes favoritos guardados.")

def obtener_calificaciones(titulo):
    url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={titulo}&language=es-ES"
    response = requests.get(url)
    if response.status_code == 200:
        resultados = response.json()['results']
        if resultados:
            resultado = resultados[0]  # Tomamos el primer resultado
            nombre = resultado.get('title') or resultado.get('name')
            calificacion = resultado.get('vote_average', 'No disponible')
            print(calificacion)
            hablar(f"{nombre} tiene una calificación de {calificacion} sobre 10 en TMDB.")
        else:
            hablar("No encontré resultados para ese título.")
    else:
        hablar("Hubo un problema al conectarse con el servicio.")

def obtener_recomendaciones(tipo_contenido):
    # Verificar si hay favoritos guardados
    if not os.path.exists('datos_entretenimiento.json'):
        hablar("No tienes favoritos guardados para hacer recomendaciones.")
        return
    
    with open('datos_entretenimiento.json', 'r') as f:
        datos = json.load(f)

    favoritos = datos.get("favoritos", [])
    if not favoritos:
        hablar("No tienes favoritos guardados para hacer recomendaciones.")
        return
    
    # Obtener el primer favorito que coincida con el tipo de contenido
    favorito = None
    for item in favoritos:
        # Búsqueda en TMDB para determinar si es serie o película
        url_busqueda = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={item}&language=es-ES"
        response_busqueda = requests.get(url_busqueda)

        if response_busqueda.status_code == 200:
            resultados = response_busqueda.json().get('results', [])
            if resultados:
                tipo_favorito = resultados[0]['media_type']  # Puede ser 'movie' o 'tv'
                
                if (tipo_contenido == 'pelicula' and tipo_favorito == 'movie') or \
                  (tipo_contenido == 'serie' and tipo_favorito == 'tv'):
                    favorito = resultados[0]
                    break  # Salimos del bucle al encontrar una coincidencia

    if not favorito:
        hablar(f"No encontré ningún favorito del tipo {tipo_contenido} para hacer recomendaciones.")
        return

    # Obtener recomendaciones basadas en el favorito encontrado
    id_favorito = favorito['id']
    tipo_favorito = favorito['media_type']
    
    url_recomendaciones = f"https://api.themoviedb.org/3/{tipo_favorito}/{id_favorito}/recommendations?api_key={TMDB_API_KEY}&language=es-ES"
    response_recomendaciones = requests.get(url_recomendaciones)

    if response_recomendaciones.status_code == 200:
        recomendaciones = response_recomendaciones.json().get('results', [])
        if recomendaciones:
            nombre_recomendado = recomendaciones[0]['title'] if tipo_favorito == 'movie' else recomendaciones[0]['name']
            hablar(f"Te recomiendo {nombre_recomendado}.")
        else:
            hablar("No encontré recomendaciones basadas en tus favoritos.")
    else:
        hablar("Hubo un problema al obtener las recomendaciones.")



# Función principal del asistente de entretenimiento
def asistente_entretenimiento():
    inicializar_datos()
    hablar("Bienvenido al asistente de entretenimiento. ¿Qué deseas hacer?")
    
    while True:
        comando = transformar_audio_texto()
        if comando:
            if "buscar película" in comando or "buscar serie" in comando:
                hablar("¿Qué título quieres buscar?")
                titulo = transformar_audio_texto()
                if titulo:
                    nombre, _ = buscar_pelicula_serie(titulo)
                    if nombre:
                        hablar(f"¿Quieres guardar {nombre} como favorito?")
                        respuesta = transformar_audio_texto()
                        if respuesta and "sí" in respuesta:
                            guardar_favorito(nombre)
                            hablar(f"{nombre} guardado en favoritos.")
            elif "dime la calificación de una serie" in comando:
                hablar("¿De que serie quieres saber la calificación?")
                titulo = transformar_audio_texto()
                obtener_calificaciones(titulo)
            elif "dime la calificación de una película" in comando:
                hablar("¿De que película quieres saber la calificación?")
                titulo = transformar_audio_texto()
                obtener_calificaciones(titulo)    
            elif "qué serie me recomiendas ver hoy" in comando:       
                obtener_recomendaciones("serie")
            elif "qué película me recomiendas ver hoy" in comando:       
                obtener_recomendaciones("pelicula")    
            elif "quiero eliminar un favorito" in comando or "eliminar un favorito" in comando:
                hablar("¿Qué título quieres eliminar de tus favoritos?") 
                titulo = transformar_audio_texto()
                eliminar_favorito(titulo)
            elif "quiero agregar un favorito" in comando or "guardar un favorito" in comando:
                hablar("¿Qué titulo quieres añadir a favoritos?")
                titulo = transformar_audio_texto()
                guardar_favorito(titulo)
                hablar(f"{titulo} guardado en favoritos.")                                 
            elif "cuáles son mis favoritos" in comando or "listar favoritos" in comando:
                listar_favoritos()
            elif "salir" in comando:
                hablar("Cerrando asistente de entretenimiento")
                break
            else:
                hablar("No entendí ese comando.")


# Función principal
def asistente_virtual():
    saludo_inicial()
    activo = True
    while activo:
        comando = transformar_audio_texto()
        
        if "qué hora es" in comando:
            pedir_hora()
        elif "qué día es hoy" in comando:
            pedir_dia()
        elif "buscar en wikipedia" in comando:
            hablar("¿Qué tema deseas buscar en Wikipedia?")
            tema = transformar_audio_texto()
            buscar_wikipedia(tema)
        elif "reproducir noticias en youtube" in comando:
            hablar("¿Qué tema de noticias deseas reproducir en YouTube?")
            tema = transformar_audio_texto()
            reproducir_noticias_youtube(tema)
        elif "quiero saber el precio de una acción" in comando:
            hablar("¿De qué empresa deseas saber el precio de la acción?")
            empresa = transformar_audio_texto()
            consultar_precio_accion(empresa)
        elif "agregar recordatorio" in comando:
            hablar("¿Qué tarea quieres agregar?")
            tarea = transformar_audio_texto()
            hablar("¿A qué hora quieres que te lo recuerde? (por ejemplo, 15:30)")
            hora = transformar_audio_texto()
            agregar_recordatorio(tarea, hora)
        elif "listar mis recordatorios" in comando or "ver mis recordatorios" in comando:
            listar_recordatorios()
        elif "eliminar recordatorio" in comando:
            hablar("¿Qué recordatorio quieres eliminar?")
            tarea = transformar_audio_texto()
            eliminar_recordatorio(tarea)
        elif "noticias" in comando:
            hablar("¿Sobre qué tema deseas saber las noticias?")
            tema = transformar_audio_texto()
            obtener_noticias(tema)
        elif "mi nombre es" in comando:
            nombre = comando.replace("mi nombre es", "").strip()
            establecer_nombre(nombre)
        elif "abre la" in comando or "abre el" in comando or "abre" in comando:
            # Identificar la aplicación a abrir
            app = comando.replace("abre la", "").replace("abre el", "").replace("abre","").strip()
            abrir_aplicacion(app)
        elif "contar un chiste" in comando or "cuéntame un chiste" in comando:
            contar_chiste()
        elif "jajaja" in comando or "risa" in comando:
            hablar("Me alegra que te haya gustado.")
        elif "adiós" in comando:
            hablar("Hasta luego, nos vemos pronto.")
            activo = False
        elif "abrir asistente de entretenimiento" in comando:
            asistente_entretenimiento()    
        else:
            hablar("Lo siento, no te entendí.")
            
# Iniciar el asistente
asistente_virtual()

