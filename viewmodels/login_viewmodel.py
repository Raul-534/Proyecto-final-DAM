import random # Importación limpia para evitar el AttributeError
from repositorios.usuario_repository import UsuarioRepository
from repositorios.email_service import EmailService

class LoginViewModel:
    def __init__(self):
        self.repo = UsuarioRepository()
        self.email_service = EmailService()

    def registrar(self, nombre, email, password):
        if not nombre or not email or not password:
            return "Campos obligatorios vacíos"
        if self.repo.registrar_usuario(nombre, email, password):
            self.email_service.enviar_bienvenida(email, nombre)
            return "OK"
        return "Error al registrar"

    def autenticar(self, email, password):
        user = self.repo.login(email, password)
        if user:
            # Extraemos el id_usuario y el nombre que devuelve el repositorio
            return {
                "exito": True, 
                "id_usuario": user['id_usuario'], # Clave vital para la navegación
                "nombre": user['nombre']
            }
        return {"exito": False, "mensaje": "Credenciales incorrectas"}

    def recuperar_password(self, email):
        if not email:
            return {"exito": False, "mensaje": "Introduce un email válido"}
        
        # Generamos código de 6 dígitos
        codigo = str(random.randint(100000, 999999))
        
        # Intentamos enviar el correo
        enviado = self.email_service.enviar_correo_recuperacion(email, codigo)
        
        if enviado:
            return {"exito": True, "token": codigo}
        return {"exito": False, "mensaje": "Error de conexión con el servidor de correo"}
    
    def cambiar_password(self, email, nueva_password):
        if len(nueva_password) < 4:
            return "La contraseña es muy corta"
        
        if self.repo.actualizar_password(email, nueva_password):
            return "OK"
        return "No se pudo actualizar la contraseña"