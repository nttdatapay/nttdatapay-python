# NTT DATA Payment Services India Payment Integration (Python)

A simple integration of the **NTT DATA Payment Services India Gateway** using pure Python.

---

## Setup

### 1. Install Dependencies

```bash
pip install pycryptodome requests
```

---

### 2. Configuration

Update `config.py` with your UAT or production credentials.

Security Notice:
Sensitive credentials such as API keys, encryption keys, and salts must never be hardcoded or exposed in source code repositories. It is strongly recommended to use secure storage mechanisms such as environment variables or a secrets management system.

Ensure that access to these credentials is restricted and follows your organization’s security policies.

For detailed security guidelines, refer to the official documentation:
https://in.nttdatapay.com/docs/integration-guide/Integration-Kits/best-practices

---

### 3. Run the Application

```bash
python server.py
```

Open in your browser:

```
http://127.0.0.1:8000
```

You may use the default port or change it to any available port if required.

---

## Flow

* Click **Start Payment**
* The server generates a transaction token via the NDPSI AUTH API
* The checkout opens as a popup
* The payment response is handled at `/response`

---

## Notes

* Always validate the signature for all responses
* Use HTTPS in production environments
* Ensure production URLs are configured before going live.s

---

## Project Structure

```
server.py      # Server and routing logic
payment.py     # Payment initiation
response.py    # Response handling
AESCipher.py   # Encryption and decryption logic
config.py      # Configuration settings
```
