#by Soul999
import telebot
from telebot import types
import random

# Define los ID de los administradores, reemplaza con los ID de tus administradores
administradores = [796054522, 7727189]

bot = telebot.TeleBot("6715500431:AAHZ1FHsYXZGilBgYaz_axdNK_5UJKMUv88")

estadisticas = {}

# Restringe el uso de comandos solo a administradores
def es_administrador(user_id):
    return user_id in administradores

def generar_estadisticas():
    fuerza = destreza = voluntad = 0
    
    # Genera estadísticas evitando 1 o 6 en cada tirada
    while True:
        fuerza = random.randint(2, 5)
        destreza = random.randint(2, 5)
        voluntad = random.randint(2, 5)
        if fuerza != 6 and destreza != 6 and voluntad != 6:
            break

    # Suma las estadísticas para obtener los Puntos de Vida (PV)
    puntos_vida = fuerza + destreza + voluntad

    # Determina el tipo de aventurero según la estadística más alta
    tipo_aventurero = ""
    if fuerza == max(fuerza, destreza, voluntad):
        tipo_aventurero = "Guerrero"
    elif destreza == max(fuerza, destreza, voluntad):
        tipo_aventurero = "Ladrón"
    else:
        tipo_aventurero = "Mago"

    return {"Clase": tipo_aventurero, "PV": puntos_vida, "FUE": fuerza, "DES": destreza, "VOL": voluntad}

def disminuir_estadistica(nombre_usuario, estadistica, cantidad):
    if nombre_usuario in estadisticas:
        if estadistica in estadisticas[nombre_usuario] and cantidad > 0:
            estadisticas[nombre_usuario][estadistica] -= cantidad
            return True
    return False

@bot.message_handler(commands=['start', 'help'])
def iniciar(mensaje):
    bot.send_message(mensaje.chat.id, 'Bienvenido al bot de estadísticas de personajes.')

@bot.message_handler(commands=['generar'])
def generar(mensaje):
    nombre_usuario = mensaje.from_user.username
    estadisticas_usuario = generar_estadisticas()
    estadisticas[nombre_usuario] = estadisticas_usuario

    # Formatear las estadísticas horizontalmente
    mensaje_respuesta = (
        f'Clase: {estadisticas_usuario["Clase"]}\n'
        f'PV: {estadisticas_usuario["PV"]}\n'
        f'FUE: {estadisticas_usuario["FUE"]}\n'
        f'DES: {estadisticas_usuario["DES"]}\n'
        f'VOL: {estadisticas_usuario["VOL"]}'
    )

    bot.send_message(mensaje.chat.id, mensaje_respuesta)

@bot.message_handler(commands=['obtener'])
def obtener(mensaje):
    nombre_usuario = mensaje.from_user.username
    estadisticas_usuario = estadisticas.get(nombre_usuario)
    if estadisticas_usuario is None:
        bot.send_message(mensaje.chat.id, 'No hay estadísticas generadas para este usuario.')
    else:
        # Formatear las estadísticas horizontalmente
        mensaje_respuesta = (
            f'Clase: {estadisticas_usuario["Clase"]}\n'
            f'PV: {estadisticas_usuario["PV"]}\n'
            f'FUE: {estadisticas_usuario["FUE"]}\n'
            f'DES: {estadisticas_usuario["DES"]}\n'
            f'VOL: {estadisticas_usuario["VOL"]}'
        )

        bot.send_message(mensaje.chat.id, mensaje_respuesta)

@bot.message_handler(commands=['tirar_dado'])
def tirar_dado_command(mensaje):
    tirar_dado(mensaje)

def tirar_dado(mensaje):
    resultado = random.randint(1, 6)
    bot.send_message(mensaje.chat.id, 'El resultado de la tirada es: ' + str(resultado))

@bot.message_handler(commands=['disminuir'])
def disminuir_estadistica_command(mensaje):
    # Ejemplo de uso: /disminuir usuario FUE 1
    partes = mensaje.text.split(' ')
    if len(partes) == 4:
        nombre_usuario = partes[1]
        estadistica = partes[2].upper()
        cantidad = int(partes[3])
        if es_administrador(mensaje.from_user.id):
            if disminuir_estadistica(nombre_usuario, estadistica, cantidad):
                bot.send_message(mensaje.chat.id, f'{estadistica} disminuida en {cantidad} para {nombre_usuario}.')
            else:
                bot.send_message(mensaje.chat.id, 'Error al disminuir la estadística. Asegúrate de especificar una estadística válida y una cantidad mayor que 0.')
        else:
            bot.send_message(mensaje.chat.id, 'No tienes permisos para usar este comando.')
    else:
        bot.send_message(mensaje.chat.id, 'Formato incorrecto. Uso: /disminuir usuario estadistica cantidad')

bot.polling()
