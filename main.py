import flet as ft
from viewmodels.login_viewmodel import LoginViewModel
from vistas.perfil_view import PerfilView
from vistas.resultado_view import ResultadoView

def main(page: ft.Page):
    page.title = "GYM PRO"
    page.theme_mode = ft.ThemeMode.DARK
    
    # Configuramos la ventana para que parezca un móvil al abrirse
    page.window_width = 400
    page.window_height = 800
    
    # Alineación central absoluta
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20

    try:
        vm = LoginViewModel()
    except Exception as e:
        page.add(ft.Text(f"Error: {e}", color="red"))
        return

    # --- WRAPPER PARA EFECTO MÓVIL ---
    def mobile_container(content):
        return ft.Container(
            content=content,
            width=350, # Esto evita que se estire en escritorio
            alignment=ft.Alignment.CENTER,
        )

    # --- NAVEGACIÓN ---

    def navegar_a_resultado(nombre, kcal):
        page.controls.clear()
        page.add(mobile_container(ResultadoView(page, nombre, kcal, view_dashboard)))
        page.update()

    def navegar_a_perfil(nombre):
        page.controls.clear()
        page.add(mobile_container(PerfilView(page, nombre, navegar_a_resultado, view_dashboard)))
        page.update()

    # --- VISTA: RECUPERAR CONTRASEÑA ---
    def view_recuperar(e=None):
        page.controls.clear()
        
        # 1. Campos de texto (algunos ocultos al inicio)
        email_f = ft.TextField(label="Email", width=300, border_radius=10, prefix_icon=ft.Icons.EMAIL)
        codigo_f = ft.TextField(label="Introduce el código de 6 dígitos", width=300, border_radius=10, visible=False)
        pass_f = ft.TextField(label="Nueva Contraseña", password=True, width=300, border_radius=10, visible=False)
        msg_status = ft.Text("", size=12)
        
        # Variables de control
        codigo_esperado = [None]
        email_usuario = [None]

        # 2. Botón Principal (Inicia como ENVIAR)
        btn_principal = ft.FilledButton(
            content="ENVIAR CÓDIGO", # IMPORTANTE: Usar 'label', no 'text'
            width=300, 
            height=50
        )

        def manejar_flujo(e):
            # PASO 1: Enviar Código
            if btn_principal.content == "ENVIAR CÓDIGO":
                res = vm.recuperar_password(email_f.value)
                if res["exito"]:
                    codigo_esperado[0] = res["token"]
                    email_usuario[0] = email_f.value
                    email_f.visible = False
                    codigo_f.visible = True
                    btn_principal.content = "COMPROBAR CÓDIGO" # Cambiamos el texto del botón
                    msg_status.value = "Código enviado a tu Gmail"
                    msg_status.color = "blue"
                else:
                    msg_status.value = "Email no encontrado"
                    msg_status.color = "red"
            
            # PASO 2: Comprobar Código
            elif btn_principal.content == "COMPROBAR CÓDIGO":
                if codigo_f.value == codigo_esperado[0]:
                    codigo_f.visible = False
                    pass_f.visible = True
                    btn_principal.content = "ACTUALIZAR CONTRASEÑA" # Siguiente estado
                    msg_status.value = "Código correcto."
                    msg_status.color = "green"
                else:
                    msg_status.value = "Código incorrecto"
                    msg_status.color = "red"
            
            # PASO 3: Actualizar y finalizar
            elif btn_principal.content == "ACTUALIZAR CONTRASEÑA":
                res_db = vm.cambiar_password(email_usuario[0], pass_f.value)
                if res_db == "OK":
                    pass_f.disabled = True
                    btn_principal.content = "VOLVER AL LOGIN" # Estado final
                    btn_principal.bgcolor = "green"
                    msg_status.value = "Contraseña cambiada con éxito"
                    msg_status.color = "green"
                else:
                    msg_status.value = res_db
                    msg_status.color = "red"
            
            # PASO 4: Salida
            elif btn_principal.content == "VOLVER AL LOGIN":
                view_login()

            page.update()

        btn_principal.on_click = manejar_flujo

        # 3. Construcción visual (mantenemos tu diseño de las capturas)
        page.add(
            mobile_container(
                ft.Column([
                    ft.Icon(ft.Icons.LOCK_RESET, size=80, color="blue"),
                    ft.Text("RECUPERACIÓN", size=28, weight="bold"),
                    email_f,
                    codigo_f,
                    pass_f,
                    msg_status,
                    btn_principal,
                    ft.TextButton("Cancelar", on_click=lambda _: view_login())
                ], horizontal_alignment="center")
            )
        )
        page.update()

    # --- VISTA: REGISTRO ---
    def view_registro(e=None):
        page.controls.clear()
        nom = ft.TextField(label="Nombre", width=300, border_radius=10)
        ema = ft.TextField(label="Email", width=300, border_radius=10)
        cla = ft.TextField(label="Contraseña", password=True, width=300, border_radius=10)
        
        def registrar_click(e):
            res = vm.registrar(nom.value, ema.value, cla.value)
            if res == "OK":
                page.snack_bar = ft.SnackBar(ft.Text("¡Registro con éxito!"), bgcolor="green")
                page.snack_bar.open = True
                view_login()
            page.update()

        page.add(
            mobile_container(
                ft.Column([
                    ft.Icon(ft.Icons.PERSON_ADD, size=80, color="blue"),
                    ft.Text("REGISTRO", size=28, weight="bold"),
                    nom, ema, cla,
                    ft.FilledButton("CREAR CUENTA", on_click=registrar_click, width=300),
                    ft.TextButton("Ya tengo cuenta", on_click=lambda _: view_login())
                ], horizontal_alignment="center")
            )
        )
        page.update()

    # --- VISTA: DASHBOARD ---
    def view_dashboard(nombre_usuario):
        page.controls.clear()
        
        def crear_tarjeta(texto, icono, color, click_func):
            return ft.Container(
                content=ft.Column([
                    ft.Icon(icono, size=35, color=color),
                    ft.Text(texto, weight="bold", size=12)
                ], horizontal_alignment="center", alignment="center"),
                padding=10, bgcolor="#252525", border_radius=15,
                width=140, height=120, on_click=click_func
            )

        page.add(
            mobile_container(
                ft.Column([
                    ft.Text(f"Hola, {nombre_usuario}", size=28, weight="bold"),
                    ft.Divider(height=20, color="transparent"),
                    ft.Row([
                        crear_tarjeta("RUTINAS", ft.Icons.FITNESS_CENTER, "blue", None),
                        crear_tarjeta("PROGRESO", ft.Icons.SHOW_CHART, "green", None),
                    ], alignment="center"),
                    ft.Row([
                        crear_tarjeta("DIETAS", ft.Icons.RESTAURANT, "orange", None),
                        crear_tarjeta("PERFIL", ft.Icons.PERSON, "white", lambda _: navegar_a_perfil(nombre_usuario)),
                    ], alignment="center"),
                    ft.Divider(height=20, color="transparent"),
                    ft.TextButton("CERRAR SESIÓN", on_click=lambda _: view_login(), icon=ft.Icons.LOGOUT, icon_color="red")
                ], horizontal_alignment="center")
            )
        )
        page.update()

    # --- VISTA: LOGIN ---
    def view_login(e=None):
        page.controls.clear()
        email_f = ft.TextField(label="Email", width=300, border_radius=10)
        clave_f = ft.TextField(label="Contraseña", password=True, width=300, border_radius=10)
        error_msg = ft.Text("", color="red", weight="bold") # TEXTO DE ERROR PEDIDO

        def login_click(e):
            res = vm.autenticar(email_f.value, clave_f.value)
            if res["exito"]:
                view_dashboard(res["nombre"])
            else:
                error_msg.value = "Credenciales incorrectas" # MENSAJE EN ROJO
                page.update()

        page.add(
            mobile_container(
                ft.Column([
                    ft.Icon(ft.Icons.FITNESS_CENTER, size=80, color="blue"),
                    ft.Text("GYM PRO", size=32, weight="bold"),
                    email_f, clave_f,
                    error_msg,
                    ft.TextButton("¿Has olvidado tu contraseña?", on_click=view_recuperar),
                    ft.FilledButton("ENTRAR", on_click=login_click, width=300, height=50),
                    ft.Row([ft.Text("¿Eres nuevo?"), ft.TextButton("Regístrate", on_click=view_registro)], alignment="center")
                ], horizontal_alignment="center")
            )
        )
        page.update()

    view_login()

if __name__ == "__main__":
    ft.app(target=main)