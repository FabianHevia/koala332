# Created by Fabián Hevia
# Only works the cursor effect for now

import pyautogui
import ctypes
import time
import random
from tkinter import Tk, Label
from PIL import Image, ImageTk
import threading
import requests
from io import BytesIO
import keyboard

# Rotate the screen
# Only works in wds11 and have a few things to upgrade
def rotate_screen(angle):
    user32 = ctypes.windll.user32
    DMDO_DEFAULT = 0
    DMDO_90 = 1
    DMDO_180 = 2
    DMDO_270 = 3
    screen_settings = user32.GetDC(0)
    width = user32.GetDeviceCaps(screen_settings, 118)  # HORZRES
    height = user32.GetDeviceCaps(screen_settings, 117)  # VERTRES
    if angle == 90:
        orientation = DMDO_90
    elif angle == 180:
        orientation = DMDO_180
    elif angle == 270:
        orientation = DMDO_270
    else:
        orientation = DMDO_DEFAULT

    user32.ChangeDisplaySettingsW(None, orientation)
    time.sleep(2)  # Mantener la pantalla girada por 2 segundos
    user32.ChangeDisplaySettingsW(None, DMDO_DEFAULT) 

def change_cursor_size():
    for _ in range(5):
        size = random.randint(10, 50)  # Tamaño aleatorio entre 10 y 50
        pyautogui.FAILSAFE = False
        pyautogui.moveTo(random.randint(0, 1920), random.randint(0, 1080), duration=0.2)
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        time.sleep(0.5)

def show_koala_image():
    root = Tk()
    root.title("Koala")
    root.attributes("-topmost", True)  # Mantener la ventana siempre encima
    try:
        image_url = "https://www.google.com/imgres?q=koala&imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2F4%2F49%2FKoala_climbing_tree.jpg&imgrefurl=https%3A%2F%2Fes.wikipedia.org%2Fwiki%2FPhascolarctos_cinereus&docid=0bLilpXlNx-Q3M&tbnid=ztyw4cGDPImCNM&vet=12ahUKEwiJuaDuqdiMAxVQIrkGHX8hBBIQM3oECBUQAA..i&w=1132&h=1113&hcb=2&ved=2ahUKEwiJuaDuqdiMAxVQIrkGHX8hBBIQM3oECBUQAA"
        response = requests.get(image_url)
        image_data = Image.open(BytesIO(response.content))
        image_data = image_data.resize((300, 300), Image.ANTIALIAS) 
        koala_image = ImageTk.PhotoImage(image_data)
        label = Label(root, image=koala_image)
        label.image = koala_image 
        label.pack()

        root.mainloop()
    except Exception as e:
        print(f"Error al cargar la imagen del koala: {e}")

# Función para ejecutar efectos aleatorios cada 10 segundos
def random_effects(stop_event):
    effects = [
        lambda: rotate_screen(180),
        change_cursor_size,
        lambda: pyautogui.moveTo(random.randint(0, 1920), random.randint(0, 1080), duration=0.5),
    ]

    while not stop_event.is_set():
        effect = random.choice(effects)  # Seleccionar un efecto aleatorio
        effect()  # Ejecutar el efecto
        time.sleep(10)  # Esperar 10 segundos antes del próximo efecto

#  Primary function of the program
# The fully functions of the koala works here and the fuctions who dont works too
def main():
    print("Bienvenido al Koala!")
    time.sleep(2)

    # Evento para detener los hilos
    stop_event = threading.Event()

    # Mostrar la imagen de koala en un hilo separado
    koala_thread = threading.Thread(target=show_koala_image)
    koala_thread.daemon = True
    koala_thread.start()

    # Ejecutar efectos aleatorios en un hilo separado
    effects_thread = threading.Thread(target=random_effects, args=(stop_event,))
    effects_thread.daemon = True
    effects_thread.start()

    print("¡El Koala está activo! Presiona 'Esc' para detenerlo.")

    # Esperar hasta que se presione la tecla 'Esc'
    while True:
        if keyboard.is_pressed('esc'):  # Detectar si se presiona la tecla Esc
            print("Deteniendo el Koala...")
            stop_event.set()  # Detener los efectos aleatorios
            break

if __name__ == "__main__":
    main()