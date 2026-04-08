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
        msg.set_content(f"Hola {nombre_usuario}, ¡Bienvenido a GYM PRO!")
        
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.emisor, self.password)
                smtp.send_message(msg)
            return True
        except Exception as e:
            print(f"Error bienvenida: {e}")
            return False
        
    def enviar_correo_recuperacion(self, email_destino, token):
        msg = EmailMessage()
        msg["Subject"] = "Código de Recuperación - GYM PRO"
        msg["From"] = self.emisor
        msg["To"] = email_destino
        msg.set_content(f"Tu código de seguridad para cambiar la contraseña es: {token}\n\nSi no has solicitado esto, ignora este correo.")

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.emisor, self.password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Error recuperación: {e}")
            return False