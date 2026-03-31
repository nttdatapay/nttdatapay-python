import json, uuid, re, requests
from time import gmtime, strftime
from AESCipher import AESCipher
from config import *

def initiate_payment(self):
    try:
        amount = '100.00'
        merchTxnId = uuid.uuid4().hex[:12]
        merchId = '317159'
        password = 'Test@123'
        product = 'NSE'
        custEmail = 'testemailid@xyz.com'
        custMobile = '8888888888'
        returnUrl = 'http://127.0.0.1:8000/response'
        txnDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        # optional udf parameters, available till udf10
        udf1 = "udf1 value"
        udf2 = "udf2 value"
        udf3 = "udf3 value"
        udf4 = "udf4 value"
        udf5 = "udf5 value"

        jsondata = {
            "payInstrument": {
                "headDetails": {"version": "OTSv1.1","api": "AUTH","platform": "FLASH"},
                "merchDetails": {
                    "merchId": merchId,
                    "password": password,
                    "merchTxnId": merchTxnId,
                    "merchTxnDate": txnDate
                },
                "payDetails": {"amount": amount,"product": product,"txnCurrency": "INR"},
                "custDetails": {"custEmail": custEmail,"custMobile": custMobile},
                "extras": {"udf1": udf1, "udf2": udf2, "udf3": udf3, "udf4": udf4, "udf5": udf5}
            }
        }

        cipher = AESCipher(
            REQUEST_ENC_KEY,
            REQUEST_SALT,
            RESPONSE_DEC_KEY,
            RESPONSE_SALT
        )

        encrypted = cipher.encrypt(bytes(json.dumps(jsondata), encoding="utf-8"))

        url = AUTH_UPI_URL
        payload = f"encData={encrypted}&merchId={merchId}"
        headers = {'content-type': "application/x-www-form-urlencoded"}

        res = requests.post(url, data=payload, headers=headers)

        arr = res.text.split('&')
        token_enc = arr[1].split('=')[1]

        decrypted = cipher.decrypt(token_enc)

        clean = decrypted.replace("\x00","").replace("\x01","").replace("\x0c","").strip()
        clean_json = re.search(r'\{.*\}', clean, re.DOTALL).group()

        data = json.loads(clean_json)
        atomTokenId = data['atomTokenId']

        response = {
            "atomTokenId": atomTokenId,
            "merchId": merchId,
            "custEmail": custEmail,
            "custMobile": custMobile,
            "returnUrl": returnUrl
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    except Exception as e:
            self.respond(f"<h2>Error:</h2><pre>{str(e)}</pre>")