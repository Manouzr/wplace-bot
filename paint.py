import tls_client
import capsolver
import threading
from queue import Queue

capsolver.api_key = 'CAP-KEY'

TOKENS_FILE = "tokens.txt"   
PROXIES_FILE = "proxies.txt" # user:pass@ip:port
SITE_KEY = "0x4AAAAAABpqJe8FO0N84q0F"
SITE_URL = "https://wplace.live"
PIXEL_URL = "https://backend.wplace.live/s0/pixel/1054/750"
ME_URL = "https://backend.wplace.live/me"
COLOR = 1 # index couleur à utiliser 

# Deux coins du carré coords -1000 sur x
TOP_LEFT = (299, 614)
BOTTOM_RIGHT = (348, 622)

# === FUNCTIONS ===
def solve_turnstile():
    solution = capsolver.solve({
        "type": "AntiTurnstileTaskProxyLess",
        "websiteKey": SITE_KEY,
        "websiteURL": SITE_URL,
    })
    return solution['token']

def get_square_coords(tl, br):
    coords_list = []
    min_x, max_x = sorted([tl[0], br[0]])
    min_y, max_y = sorted([tl[1], br[1]])
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            coords_list.append((x, y))
    return coords_list

def paint_pixels(jwt_token, proxy, queue):
    session = tls_client.Session(client_identifier="chrome_112", random_tls_extension_order=True)

    # Proxy setup
    if proxy:
        session.proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "text/plain;charset=UTF-8",
        "cookie": f"j={jwt_token}",
        "origin": "https://wplace.live",
        "priority": "u=1, i",
        "referer": "https://wplace.live/",
        "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }

    me_data = session.get(ME_URL, headers=headers).text
    print(me_data)
    available = int(me_data["charges"]["count"])

    if available <= 0:
        print(f"[{me_data.get('name','Unknown')}] Pas de pixels disponibles")
        return

    coords_list = []
    colors_list = []

    # Prend autant de coords que de pixels dispos
    for _ in range(available):
        if queue.empty():
            break
        x, y = queue.get()
        coords_list.extend([x, y])
        colors_list.append(COLOR)

    if not coords_list:
        return

    token = solve_turnstile()

    payload = {
        "colors": colors_list,
        "coords": coords_list,
        "t": token
    }

    r = session.post(PIXEL_URL, headers=headers, json=payload)
    print(f"[{me_data.get('name','Unknown')}] Envoie {len(colors_list)} pixels → {r.status_code} {r.text}")

def worker(queue, jwt, proxy):
    try:
        paint_pixels(jwt, proxy, queue)
    except Exception as e:
        print(f"[{jwt[:10]}...] Erreur: {e}")

# === MAIN ===
with open(TOKENS_FILE, "r") as f:
    jwt_tokens = [line.strip() for line in f if line.strip()]

with open(PROXIES_FILE, "r") as f:
    proxies = [line.strip() for line in f if line.strip()]

coords_queue = Queue()
for coord in get_square_coords(TOP_LEFT, BOTTOM_RIGHT):
    coords_queue.put(coord)

threads = []
for i, jwt in enumerate(jwt_tokens):
    proxy = proxies[i % len(proxies)] if proxies else None
    t = threading.Thread(target=worker, args=(coords_queue, jwt, proxy))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("✅ Carré terminé avec envoi multi-pixels par compte")
