from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import random
import string
import time
import re
from colorama import Fore, init
import requests
import os
import subprocess
import atexit
import ctypes
from selenium.webdriver.chrome.service import Service
from pystyle import Anime, Colors, Colorate, Center, System, Write

purple_static = ['150;0;255'] * 24
intro_text = r'''
                      _ _ _ _
  __ _ _ _ _ _ ___ | |___| | _ _ ___ ___ _ _ _ _ __ _ _ __ ___ __| |_ ___ __| |_____ _ _
 / _` | || | ' \(_-<_| / _ \ | | || (_-</ -_) '_| ' \/ _` | ' \/ -_) / _| ' \/ -_) _| / / -_) '_|
 \__, |\_,_|_||_/__(_)_\___/_| \_,_/__/\___|_| |_||_\__,_|_|_|_\___| \__|_||_\___\__|_\_\___|_|
 |___/
                    Made By Kiyozu - https://discord.gg/MdDQwzEstF
                                               > Press Enter
'''

def show_header():
    System.Clear()
    print(Colorate.Vertical(purple_static, intro_text.split('> Press Enter')[0]))

init(autoreset=True)

# Global driver reference for cleanup
_active_driver = None

def _cleanup_chrome():
    global _active_driver
    try:
        if _active_driver:
            _active_driver.quit()
            _active_driver = None
    except:
        pass
    if os.name == 'nt':
        try:
            subprocess.run(['taskkill', '/F', '/IM', 'chromedriver.exe', '/T'], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass

atexit.register(_cleanup_chrome)

def random_letters(n, filter_premium=False):
    all_chars = string.ascii_lowercase + string.digits + "._-"
    base_chars = string.ascii_lowercase + string.digits
    if filter_premium:
        if n == 1:
            return random.choice(base_chars)
        first = random.choice(base_chars)
        middle = ''.join(random.choice(all_chars) for _ in range(n - 2))
        last = random.choice(base_chars)
        return first + middle + last
    else:
        return ''.join(random.choice(all_chars) for _ in range(n))

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    ]
    return random.choice(user_agents)

def check_user_status(letter_count, interval, customlist=None, filter_premium=False, save_to_file=True, webhook_url=None):
    base_url = "guns.lol/"
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument(f'user-agent={get_random_user_agent()}')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    try:
        service = Service(log_path=os.devnull)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        global _active_driver
        _active_driver = driver
        driver.set_page_load_timeout(15)
    except Exception as e:
        print(f"{Fore.RED}Erreur Chrome: {e}{Fore.RESET}")
        return

    try:
        request_count = 0
        usernames_to_check = customlist if customlist else None
        index = 0

        while True:
            if usernames_to_check is not None:
                if index >= len(usernames_to_check):
                    print(f"{Fore.CYAN}Vérification terminée.{Fore.RESET}")
                    break
                current_suffix = usernames_to_check[index]
                index += 1
                if filter_premium and (current_suffix[0] in "._-" or current_suffix[-1] in "._-"):
                    print(f"URL: {Fore.MAGENTA}{base_url}{current_suffix} - {Fore.YELLOW}Premium Alias (ignoré){Fore.RESET}")
                    continue
            else:
                current_suffix = random_letters(letter_count, filter_premium)

            url = base_url + current_suffix
            request_count += 1

            try:
                driver.get(f"https://{url}")
                time.sleep(1.2)

                is_unclaimed = False
                h1_elements = driver.find_elements(By.TAG_NAME, "h1")
                for h1 in h1_elements:
                    if "username not found" in h1.text.lower() or "bulunamad" in h1.text.lower():
                        is_unclaimed = True
                        break

                if is_unclaimed:
                    status = f"{Fore.GREEN}unclaimed"
                    print(f"URL: {Fore.MAGENTA}{base_url}{current_suffix} {Fore.WHITE}- Status: {status}{Fore.RESET}")

                    if save_to_file:
                        with open("unclaimed.txt", "a", encoding="utf-8") as f:
                            f.write(f"{current_suffix}\n")

                    if webhook_url:
                        embed = {
                            "title": f"Available: {current_suffix}[](https://guns.lol/{current_suffix})",
                            "description": "https://discord.gg/MdDQwzEstF ON TOP ! Made By Kiyozu !",
                            "color": 0x9B59B6
                        }
                        try:
                            requests.post(webhook_url, json={"embeds": [embed]})
                        except:
                            pass
                else:
                    print(f"URL: {Fore.MAGENTA}{base_url}{current_suffix} {Fore.WHITE}- Status: {Fore.RED}claimed{Fore.RESET}")

            except Exception:
                print(f"URL: {Fore.MAGENTA}{base_url}{current_suffix} - {Fore.YELLOW}error/timeout{Fore.RESET}")

            time.sleep(interval + random.uniform(0.3, 0.8))

    finally:
        try:
            driver.quit()
        except:
            pass
        _active_driver = None

# ====================== MAIN ======================
try:
    Anime.Fade(Center.Center(intro_text), purple_static, Colorate.Vertical, interval=0.035, enter=True)

    letter_count = int(input(f"{Fore.CYAN}Combien de lettres par username ? (ex: 4-6) : {Fore.RESET}"))
    interval = float(input(f"{Fore.CYAN}Délai entre les checks (0 recommandé) : {Fore.RESET}"))

    use_custom = input(f"{Fore.CYAN}Utiliser customlist.txt ? (Y/N) : {Fore.RESET}").lower() == 'y'
    customlist = None
    if use_custom:
        try:
            with open("customlist.txt", "r", encoding="utf-8") as f:
                customlist = [line.strip() for line in f if line.strip() and not line.strip().startswith("//")]
            print(f"{Fore.GREEN}{len(customlist)} usernames chargés.{Fore.RESET}")
        except:
            print(f"{Fore.RED}customlist.txt non trouvé.{Fore.RESET}")
            use_custom = False

    filter_premium = input(f"{Fore.CYAN}Filtrer les Premium (._-) ? (Y/N) : {Fore.RESET}").lower() == 'y'
    save_to_file = input(f"{Fore.CYAN}Sauvegarder les unclaimed dans unclaimed.txt ? (Y/N) : {Fore.RESET}").lower() == 'y'

    use_webhook = input(f"{Fore.CYAN}Envoyer les unclaimed sur Discord Webhook ? (Y/N) : {Fore.RESET}").lower() == 'y'
    webhook_url = None
    if use_webhook:
        webhook_url = input(f"{Fore.CYAN}Colle ton Webhook Discord : {Fore.RESET}").strip()

    print(f"\n{Fore.MAGENTA}Démarrage du checker...{Fore.RESET}\n")
    check_user_status(letter_count, interval, customlist, filter_premium, save_to_file, webhook_url)

except KeyboardInterrupt:
    print(f"\n{Fore.YELLOW}Arrêt par l'utilisateur.{Fore.RESET}")
except Exception as e:
    print(f"{Fore.RED}Erreur: {e}{Fore.RESET}")
finally:
    if os.name == 'nt':
        print(f"\n{Fore.CYAN}Appuie sur une touche pour quitter...{Fore.RESET}")
        os.system("pause >nul")
