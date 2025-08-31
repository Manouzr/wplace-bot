import tls_client

TOKENS_FILE = "tokens.txt"  
PROXIES_FILE = "proxies.txt"  # user:pass@ip:port
ME_URL = "https://backend.wplace.live/me"
PURCHASE_URL = "https://backend.wplace.live/purchase"

def check_and_purchase(jwt_token, proxy=None):
    session = tls_client.Session(client_identifier="chrome_112", random_tls_extension_order=True)

    if proxy:
        session.proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "cookie": f"j={jwt_token}",
        "origin": "https://wplace.live",
        "referer": "https://wplace.live/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }

    try:
        me_data = session.get(ME_URL, headers=headers).json()
    except Exception as e:
        print(f"[{jwt_token[:10]}...] Erreur /me: {e}")
        return

    droplets = me_data.get("droplets", 0)
    name = me_data.get("name", "Unknown")

    if droplets >= 500:
        amount = droplets // 500
        payload = {"product": {"id": 70, "amount": amount}}
        try:
            r = session.post(PURCHASE_URL, headers=headers, json=payload)
            print(f"[{name}] Achat {amount}x (500 droplets) → {r.status_code} {r.text}")
        except Exception as e:
            print(f"[{name}] Erreur achat: {e}")
    else:
        print(f"[{name}] Pas assez de droplets ({droplets}/500)")

def main():
    with open(TOKENS_FILE, "r") as f:
        jwt_tokens = [line.strip() for line in f if line.strip()]

    proxies = []
    try:
        with open(PROXIES_FILE, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        proxies = [None] * len(jwt_tokens)

    for i, jwt in enumerate(jwt_tokens):
        proxy = proxies[i % len(proxies)] if proxies else None
        check_and_purchase(jwt, proxy)

if __name__ == "__main__":
    main()
