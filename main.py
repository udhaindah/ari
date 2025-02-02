import requests
import random
from colorama import Fore, Style, init

init()

def load_proxies():
    """Memuat proxy dari file 'proxy.txt' dengan format: username:password@host:port"""
    proxies = []
    try:
        with open("proxy.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    proxies.append(line)
    except FileNotFoundError:
        print(Fore.RED + "File proxy.txt tidak ditemukan!" + Style.RESET_ALL)
    return proxies

def get_random_proxy(proxies):
    """Mengembalikan proxy secara acak dari daftar"""
    if not proxies:
        return None
    return random.choice(proxies)

def get_proxy_dict(proxy):
    """Mengembalikan proxy dict dengan autentikasi"""
    if proxy:
        return {
            "http": f"http://{proxy}",
            "https": f"https://{proxy}"
        }
    return None

def get_random_user_agent():
    """Mengembalikan User-Agent Android secara acak"""
    user_agents = [
        "Mozilla/5.0 (Linux; Android 10; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.119 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
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
    return random.choice(user_agents)

def login_with_proxy(email, password, proxy):
    url = "https://arichain.io/api/account/signin_mobile"
    payload = {
        "blockchain": "testnet",
        "email": email,
        "pw": password,
        "lang": "id",
        "device": "app",
        "is_mobile": "Y"
    }
    headers = {"User-Agent": get_random_user_agent()}
    proxy_dict = get_proxy_dict(proxy)
    
    try:
        response = requests.post(url, data=payload, headers=headers, proxies=proxy_dict, timeout=30)
        response.raise_for_status()
        result = response.json()
        print(Fore.GREEN + f"Login sukses untuk {email}!" + Style.RESET_ALL)
        return result
    except requests.RequestException as e:
        print(Fore.RED + f"Login gagal: {e}" + Style.RESET_ALL)
        return None

def main():
    proxies = load_proxies()
    
    with open("data.txt", "r") as file:
        for line in file:
            email, password = line.strip().split(":")
            proxy = get_random_proxy(proxies)
            print(Fore.CYAN + f"Menggunakan proxy: {proxy}" + Style.RESET_ALL)
            result = login_with_proxy(email, password, proxy)
            
            if result and "result" in result:
                address = result["result"].get("address", "N/A")
                with open("hasil.txt", "a") as out_file:
                    out_file.write(f"{email}:{address}\n")

if __name__ == "__main__":
    main()
