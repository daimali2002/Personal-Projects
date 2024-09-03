import smtplib
from email.mime.text import MIMEText

def send_otp(reciever, otp):







    subject = "Your Password Reset OTP. Do Not Share With Anyone"

    body = f"""
Dear User,

We have received a request to reset your password. Your One-Time Password (OTP) for resetting your password is:

{otp}

Please use this OTP to complete the password reset process. This OTP is valid for the next 15 minutes.

If you did not request a password reset, please ignore this email or contact our support team for assistance.

Best regards,
Payfast
    """

    sender = "senderpayfast@gmail.com"
    recipients = [reciever]
    password = "scym eydf brcj xoyp"
    def send_email(subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
    send_email(subject, body, sender, recipients, password)

def send_order_details(receiver, order_details):
    subject = "Your Order Details from Payfast"

    body = f"""
Dear Customer,

Your order has been placed successfully! Here are the details of your order:

Order Details:
Product Title - Quantity
"""
    for product in order_details.get('Products'):
        body += f"{product['title']} - {product['quantity']}\n"

    body += f"""

Total Price: ${order_details.get('total_price')}
Total Discount: ${order_details['total_discount']}

Shipping Address:
{order_details.get('Address')}

Phone:
{order_details.get('Phone')}

Thank you for shopping with us!

Best regards,
Payfast
    """

    sender = "senderpayfast@gmail.com"
    recipients = [receiver]
    password = "scym eydf brcj xoyp"

    def send_email(subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())

    send_email(subject, body, sender, recipients, password)
