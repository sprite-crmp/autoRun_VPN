import subprocess
import json
import os
import time
import pygetwindow as gw
import pyautogui

from colorama import Fore

trying = 1
trying_locked = 1
window = None
win = None

with open("assets/config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

def is_windows_locked():
    process_name = 'LogonUI.exe'
    callall = 'TASKLIST'
    outputall = subprocess.check_output(callall)
    outputstringall = str(outputall)
    if process_name in outputstringall:
        return True
    else:
        return False

def get_window(start=True):
    global window, win

    windows = gw.getWindowsWithTitle(config["window_title"])

    if windows:
        print(Fore.GREEN + f"Окно '{config['window_title']}' активно.")
        print(Fore.RESET + f"Открываю окно '{config['window_title']}'...")

        win = windows[0]

        try:
            win.restore()
            win.activate()
            time.sleep(0.3)

            print(Fore.GREEN + f"Окно '{config['window_title']}' успешно открыто.")
            print(Fore.RESET + "Включаю VPN...")
            time.sleep(0.3)

            if start:
                start_vpn()

        except AttributeError as e:
            print(Fore.RED + f"Окно '{config['window_title']}' не удалось открыть. Ошибка: {e}")
            input(Fore.RESET + "Нажмите Enter для продолжения...")

    else:
        print(f"Окно '{config['window_title']}' не найдено. Запускаю клиент.")

        try:
            os.startfile(config["happ_path"])
            time.sleep(1)

            if start:
                start_vpn()

        except FileNotFoundError:
            print(Fore.RED + f"Не удалось найти клиент Happ: {config['happ_path']}")
            input(Fore.RESET + "Нажмите Enter для продолжения...")

def start_vpn():
    trying = 1

    while trying <= 5:
        get_window(start=False)

        try:
            button_center = pyautogui.locateCenterOnScreen(
                "assets/on_button.jpg",
                confidence=0.7
            )

            x, y = button_center
            pyautogui.click(x, y)

            print(Fore.GREEN + "VPN был успешно запущен.")
            win.minimize()
            return

        except pyautogui.ImageNotFoundException:
            print(
                Fore.RED +
                f"Кнопка включения VPN не найдена на экране. Попытка: ({trying}/5)")
            trying += 1
            time.sleep(3)

        except Exception as e:
            print(Fore.RED + f"Произошла ошибка при включении VPN: {e}")
            input(Fore.RESET + "Нажмите Enter для продолжения...")
            return

    input(Fore.RESET + "Нажмите Enter для продолжения...")

while is_windows_locked():
    print(Fore.RED + f"\rЭкран Windows заблокирован. Ожидаю разблокировки... Попытка: ({trying_locked})" + Fore.RESET,
          end="",
          flush=True)
    trying_locked = trying_locked + 1
    time.sleep(5)

if trying_locked != 1: print()
get_window()

#pyinstaller --onefile --icon icon.ico --name autoRun_VPN main.py