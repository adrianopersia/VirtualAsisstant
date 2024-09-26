import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import pywhatkit
import yfinance as yf
import pyjokes

# Opciones de voz / idioma
id1 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0"
id2 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
id3 = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0"

# Función para que el asistente pueda ser escuchado
def hablar(mensaje):
    # Encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("voice", id3)  # Cambiar la voz al español
    engine.say(mensaje)
    engine.runAndWait()

# Saludo inicial basado en la hora
def saludo_inicial():
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = "Buenas noches"
    elif 6 <= hora.hour < 13:
        momento = "Buen día"
    else:
        momento = "Buenas tardes"
    
    # Saludo al usuario
    hablar(f"{momento}, en qué te puedo ayudar hoy?")

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

# Función principal
def asistente_noticias():
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
        elif "reproducir noticias" in comando:
            hablar("¿Qué tema de noticias deseas reproducir en YouTube?")
            tema = transformar_audio_texto()
            reproducir_noticias_youtube(tema)
        elif "precio de la acción" in comando:
            hablar("¿De qué empresa deseas saber el precio de la acción?")
            empresa = transformar_audio_texto()
            consultar_precio_accion(empresa)
        elif "contar un chiste" in comando or "cuéntame un chiste" in comando:
            contar_chiste()
        elif "jajaja" in comando or "risa" in comando:
            hablar("Me alegra que te haya gustado.")
        elif "adiós" in comando:
            hablar("Hasta luego, nos vemos pronto.")
            activo = False
        else:
            hablar("Lo siento, no te entendí.")
            
# Iniciar el asistente
asistente_noticias()
