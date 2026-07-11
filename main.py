import os
import subprocess
import time
import pygetwindow as gw
import pyautogui

from colorama import Fore
from config import happ_path, window_title

img_on_button = "on_button.jpg"

def get_window():
    windows = gw.getWindowsWithTitle(window_title)

    if windows:
        print(Fore.GREEN + f"Окно '{window_title}' активно.")
        print(Fore.RESET + f"Открываю окно '{window_title}'...")
        win = windows[0]
        try:
            win.restore()
            win.activate()
            time.sleep(0.3)
            print(Fore.GREEN + f"Окно '{window_title}' успешно открыто.")
            print(Fore.RESET + f"Включаю VPN...")
            time.sleep(0.3)
            start_vpn()
        except AttributeError as e:
            print(Fore.RED + f"Окно '{window_title}' не удалось открыть. Ошибка: {e}")
    else:
        print(f"Окно '{window_title}' не найдено. Запускаю клиент.")
        try:
            os.startfile(happ_path)
            time.sleep(0.3)
            start_vpn()
        except FileNotFoundError:
            print(Fore.RED + f'Не удалось найти клиент Happ: {happ_path}')

def start_vpn():
    try:
        button_center = pyautogui.locateCenterOnScreen(
            "on_button.jpg",
            confidence=0.7
        )
    except pyautogui.ImageNotFoundException:
        print(Fore.RED + "Кнопка включения VPN не найдена на экране.")
        return

    x, y = button_center
    try:
        pyautogui.click(x, y)
        print(Fore.GREEN + f"VPN был успешно запущен.")
    except Exception as e:
        print(Fore.RED + f"Произошла ошибка при включении VPN: {e}")

get_window()

input(Fore.RESET + 'Нажмите Enter для продолжения...')