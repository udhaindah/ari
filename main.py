import requests
import random
import time
import string
from colorama import Fore, Style, init
from datetime import datetime
from bs4 import BeautifulSoup

init()

ANDROID_USER_AGENTS = [
    'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-A346B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-A236B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; M2101K6G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; moto g(30)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; CPH2211) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; V2169) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'
]

def load_proxies():
    try:
        with open("proxies.txt", "r") as file:
            proxies = [line.strip() for line in file if line.strip()]
        print(f"{Fore.GREEN}\nLoaded {len(proxies)} proxies{Style.RESET_ALL}")
        return proxies
    except FileNotFoundError:
        print(f"{Fore.RED}\nFile proxies.txt not found{Style.RESET_ALL}")
        return []

def get_random_proxy(proxies):
    return random.choice(proxies) if proxies else None

def baca_akun():
    try:
        with open("data.txt", "r") as file:
            akun_list = []
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line or line.startswith('#'):  # Skip baris kosong atau komentar
                    continue
                
                if ':' not in line:
                    print(f"Peringatan: Format salah di baris {line_num} - '{line}'")
                    continue
                
                email, password = line.split(':', 1)
                akun_list.append({
                    'email': email.strip(),
                    'password': password.strip()
                })
            
            if not akun_list:
                raise ValueError("Tidak ada akun valid dalam file")
            
            return akun_list
    
    except FileNotFoundError:
        print("Error: File data.txt tidak ditemukan")
        exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

def proses_akun(akun):
    url = "https://arichain.io/api/account/signin_mobile"
    
    payload = {
        "blockchain": "testnet",
        "email": akun['email'],
        "pw": akun['password'],
        "lang": "id",
        "device": "app",
        "is_mobile": "Y"
    }
    
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=payload,
            timeout=10  # Timeout 10 detik
        )
        
        # Cek status response
        if response.status_code == 200:
            print(f"\nLogin berhasil untuk: {akun['email']}")
            print("Response:", response.text)
            return True
        else:
            print(f"\nLogin gagal untuk: {akun['email']}")
            print(f"Status Code: {response.status_code}")
            print("Error:", response.text)
            return False
    
    except Exception as e:
        print(f"\nError proses {akun['email']}: {str(e)}")
        return False

if __name__ == "__main__":
    semua_akun = baca_akun()
    total_akun = len(semua_akun)
    sukses = 0
    gagal = 0
    
    print(f"Memproses {total_akun} akun...\n")
    
    for idx, akun in enumerate(semua_akun, 1):
        print(f"Memproses akun {idx}/{total_akun} - {akun['email']}")
        if proses_akun(akun):
            sukses += 1
        else:
            gagal += 1
        
        # Jeda antar request untuk menghindari rate limiting
        if idx < total_akun:
            time.sleep(1)  # Delay 1 detik antara request
    
    print("\nHasil proses:")
    print(f"Total akun: {total_akun}")
    print(f"Berhasil: {sukses}")
    print(f"Gagal: {gagal}")

