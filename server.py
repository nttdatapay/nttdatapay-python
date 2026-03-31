from http.server import BaseHTTPRequestHandler, HTTPServer
from payment import initiate_payment
from response import handle_response
from config import NDPSI_JS_CDN_LINK

PORT = 8000

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.respond(f"""
            <html>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <body>
                <h2>NTTDATA Payment Gateway Demo</h2>

                <button onclick="startPayment()">Start Payment</button>

                <!-- Injected from Python -->
                <script src="{NDPSI_JS_CDN_LINK}"></script>

                <script>

                // Event listener
                window.addEventListener('message', function(event) {{
                    const data = event.data;
                    console.log("Event:", data);

                    if (data === "cancelTransaction") {{
                        console.log("Payment cancelled by user");
                        alert("Payment cancelled");
                    }}

                    if (data === "sessionTimeout") {{
                        console.log("Session timeout");
                        alert("Session expired. Please try again.");
                    }}
                }});

                function startPayment() {{
                    fetch("/pay", {{ method: "POST" }})
                        .then(res => res.json())
                        .then(data => {{
                            new AtomPaynetz({{
                                atomTokenId: data.atomTokenId,
                                merchId: data.merchId,
                                custEmail: data.custEmail,
                                custMobile: data.custMobile,
                                returnUrl: data.returnUrl
                            }}, "uat");
                        }});
                }}
                </script>

            </body>
            </html>
            """)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/pay":
            initiate_payment(self)
        elif self.path == "/response":
            handle_response(self)
        else:
            self.send_error(404)

    def respond(self, html):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())


if __name__ == "__main__":
    print(f"Running on http://127.0.0.1:{PORT}")
    HTTPServer(("127.0.0.1", PORT), MyHandler).serve_forever()