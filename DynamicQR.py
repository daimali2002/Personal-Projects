from flask import Flask, render_template_string
import qrcode
import base64
from io import BytesIO
import requests
import json
import uuid

app = Flask(__name__)
merchant_reference_id = str(uuid.uuid4())


#GETS TOKEN 
url = "https://apipxyuat.apps.net.pk:8443/api/raast/token"

payload = json.dumps({
  "merchant_id": "102",
  "secured_key": "zWHjBp2AlttNu1sK"
})
headers = {
  'X-Request-ID': '1cc09837-f2b7-40ab-84b2-222ed022af67',
  'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload)
token = response.json()['data']['token']



url = "https://apipxyuat.apps.net.pk:8443/api/raast/qrcode/generate/dynamic"

payload = json.dumps({
  "merchant_reference_id": merchant_reference_id,
  "expiry": 200,
  "customer_prompt": "EMAIL",
  "transaction_amount": 12345
})
headers = {
  'X-Request-ID': '6397b56f-c1ab-4fb4-87fa-38df03da8c5f',
  'Content-Type': 'application/json',
  'Authorization': "Bearer " + token
}

response = requests.request("POST", url, headers=headers, data=payload)


# Check if the request was successful
if response.status_code == 200:
    # Extract JSON content from the response
    qr_payload = response.json()['data']['qrpayload']


    # Encode payload as base64 URI
    qr_payload_b64 = base64.urlsafe_b64encode(qr_payload.encode()).decode()

    @app.route('/')
    def index():
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_payload_b64)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        # HTML template for displaying the QR code
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>QR Code Dynamic </title>
        </head>
        <body>
            <h1>QR Code Dynamic</h1>
            <img src="data:image/png;base64,{img_str}" alt="QR Code Dynamic">
        </body>
        </html>
        '''
        return render_template_string(html)

    if __name__ == '__main__':
        app.run(debug=True)
else:
    print(f"Failed to retrieve QR payload: {response.status_code} - {response.text}")
