import smtplib
from email.message import EmailMessage

class EmailService: 
    def __init__(self):
        self.emisor = "r7965151@gmail.com" 
        self.password = "tmyl ossx qkep sotb"

    def enviar_bienvenida(self, receptor_email, nombre_usuario):
        msg = EmailMessage()
        msg['Subject'] = "¡Bienvenido a GYM PRO! 💪"
        msg['From'] = self.emisor
        msg['To'] = receptor_email
        msg.set_content(f"Hola {nombre_usuario}, ¡Bienvenido!")
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.emisor, self.password)
                smtp.send_message(msg)
            return True
        except:
            return False