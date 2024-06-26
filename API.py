import http.server
import socketserver
import requests
import json
import os

PORT = 800
HTML_FILE = "index.html"

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(HTML_FILE, 'rb') as file:
                self.copyfile(file, self.wfile)
        elif self.path.startswith('/api/'):
            if len(self.path.split('/')) > 3:
                currency1 = self.path.split('/')[2].upper()
                currency2 = self.path.split('/')[3].upper()
                # Ensure the value is not None
                amount = max(1, 0 if self.path.split('/')[4] is None else int(self.path.split('/')[4]))
                url = f"https://v6.exchangerate-api.com/v6/b6319db2f2136872420d9e8e/pair/{currency1}/{currency2}/{amount}"
                response = requests.get(url)
                data = response.json()
                print(response.text)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode('utf-8'))
                
            else:
                currency = self.path.split('/api/')[1].upper()
                url = f"https://v6.exchangerate-api.com/v6/b6319db2f2136872420d9e8e/latest/{currency}"
                response = requests.get(url)
                data = response.json()
                print(response.text)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

# Change the working directory to the directory containing the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create an object of the above class
handler_object = MyHttpRequestHandler

# Create a TCP/IP server
with socketserver.TCPServer(("", PORT), handler_object) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
