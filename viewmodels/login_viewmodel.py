from repositorios.usuario_repository import UsuarioRepository
from repositorios.email_service import EmailService

class LoginViewModel:
    def __init__(self):
        self.repo = UsuarioRepository()
        self.email_service = EmailService()

    def registrar(self, nombre, email, password):
        if not nombre or not email or not password:
            return "Todos los campos son obligatorios"
        
        exito = self.repo.registrar_usuario(nombre, email, password)
        if exito:
            self.email_service.enviar_bienvenida(email, nombre)
            return "OK"
        return "Error al registrar (¿Email ya existe?)"

    def autenticar(self, email, password):
        user = self.repo.login(email, password)
        if user:
            return {"exito": True, "nombre": user['nombre']}
        return {"exito": False, "mensaje": "Credenciales incorrectas"}