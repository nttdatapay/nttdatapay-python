import hashlib
import hmac
import urllib.parse, json, re
from AESCipher import AESCipher
from config import *

def handle_response(self):
    try:
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(post_data.decode())

        encData = data.get("encData", [""])[0]

        cipher =  cipher = AESCipher(
            REQUEST_ENC_KEY,
            REQUEST_SALT,
            RESPONSE_DEC_KEY,
            RESPONSE_SALT
        )
        decrypted = cipher.decrypt(encData)

        # to remove and clean unwanted spaces and special characters from response
        clean = decrypted.replace("\x00","").replace("\x01","").replace("\x0c","").strip() 
        clean_json = re.search(r'\{.*\}', clean, re.DOTALL).group()

        decoded = json.loads(clean_json)

        # print(json.dumps(decoded, indent=2))

        status = decoded['payInstrument']['responseDetails']['statusCode']

        received_signature = decoded['payInstrument']['payDetails'].get('signature')

        generated_signature = generate_signature(decoded, RESPONSE_HASH_KEY)

        is_valid = generated_signature == received_signature

        print("Received signature:", received_signature)
        print("Signature VALID:", is_valid)

        # Show message based on status
        if not is_valid:
          # CRITICAL: never trust this response
          title = "Invalid Signature, Response rejected"
        else:
            if status == "OTS0000":
                title = "Successful"
            elif status == "OTS0551":
                title = "Pending"
            else:
                title = "Failed"

        html = f"""
        <html>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <body>
            <h2>Payment Result: {title}</h2>
            <p>Status: {status}</p>
            <pre>{json.dumps(decoded, indent=2)}</pre>
        </body>
        </html>
        """

        self.respond(html)

    except Exception as e:
        self.respond(f"<h2>Error in Response:</h2><pre>{str(e)}</pre>")

def generate_signature(decoded, res_hash_key):
    try:
        data = decoded['payInstrument']

        merchId = str(data['merchDetails']['merchId'])
        atomTxnId = str(data['payDetails']['atomTxnId'])
        merchTxnId = str(data['merchDetails']['merchTxnId'])

        # match JS .toFixed(2)
        amount = "{:.2f}".format(float(data['payDetails']['totalAmount']))

        statusCode = str(data['responseDetails']['statusCode'])
        subChannel = str(data['payModeSpecificData']['subChannel'][0])
        bankTxnId = str(data['payModeSpecificData']['bankDetails']['bankTxnId'])

        # EXACT SAME ORDER AS JS
        signature_string = (
            merchId +
            atomTxnId +
            merchTxnId +
            amount +
            statusCode +
            subChannel +
            bankTxnId
        )

        print("SIGNATURE STRING:", signature_string)

        # HMAC SHA512
        generated_signature = hmac.new(
            res_hash_key.encode(),
            signature_string.encode(),
            hashlib.sha512
        ).hexdigest()

        print("GENERATED SIGNATURE:", generated_signature)

        return generated_signature

    except Exception as e:
        print("Signature Error:", str(e))
        return None