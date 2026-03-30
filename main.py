import flet as ft
from viewmodels.login_viewmodel import LoginViewModel

def main(page: ft.Page):
    page.title = "GYM PRO - Desktop"
    page.window.width = 400
    page.window.height = 700
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    # Intentamos cargar el ViewModel
    try:
        vm = LoginViewModel()
    except Exception as e:
        page.add(ft.Text(f"Error cargando datos: {e}", color="red"))
        page.update()
        return

    def view_dashboard(nombre_usuario):
        page.controls.clear()
        
        def crear_tarjeta(texto, icono_code, color_icon):
            return ft.Container(
                content=ft.Column([
                    ft.Icon(icono_code, size=35, color=color_icon),
                    ft.Text(texto, weight="bold", size=12)
                ], horizontal_alignment="center", alignment="center"),
                padding=10,
                bgcolor="#252525", 
                border_radius=15,
                width=140,
                height=120,
                on_click=lambda _: print(f"Click en {texto}"),
                ink=True
            )

        page.add(
            ft.Text(f"¡Hola, {nombre_usuario}!", size=28, weight="bold"),
            ft.Text("¿Qué vamos a entrenar?", size=16, color="blue"),
            ft.Divider(height=20, color="transparent"),
            ft.Column([
                ft.Row([
                    crear_tarjeta("MIS RUTINAS", ft.Icons.FITNESS_CENTER_ROUNDED, "blue"),
                    crear_tarjeta("PROGRESO", ft.Icons.SHOW_CHART_ROUNDED, "green"),
                ], alignment="center"),
                ft.Row([
                    crear_tarjeta("DIETAS", ft.Icons.RESTAURANT_ROUNDED, "orange"),
                    crear_tarjeta("PERFIL", ft.Icons.PERSON_ROUNDED, "white"),
                ], alignment="center"),
            ], spacing=15),
            ft.Divider(height=20, color="transparent"),
            ft.ElevatedButton("CERRAR SESIÓN", on_click=lambda _: view_login(), color="red")
        )
        page.update()

    def view_registro(e=None):
        page.controls.clear()
        nombre = ft.TextField(label="Nombre", prefix_icon=ft.Icons.PERSON_ROUNDED)
        email = ft.TextField(label="Email", prefix_icon=ft.Icons.EMAIL_ROUNDED)
        clave = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK_ROUNDED)
        msg = ft.Text()

        def btn_reg_click(e):
            res = vm.registrar(nombre.value, email.value, clave.value)
            if res == "OK":
                msg.value = "¡Registrado! Ya puedes loguearte."
                msg.color = "green"
            else:
                msg.value = res
                msg.color = "red"
            page.update()

        page.add(
            ft.Text("CREAR CUENTA", size=25, weight="bold"),
            nombre, email, clave, msg,
            ft.FilledButton("REGISTRAR", on_click=btn_reg_click, width=300),
            ft.TextButton("Volver", on_click=lambda _: view_login())
        )
        page.update()

    def view_login(e=None):
        page.controls.clear()
        email_f = ft.TextField(label="Email", width=300, prefix_icon=ft.Icons.PERSON)
        clave_f = ft.TextField(label="Contraseña", password=True, width=300, prefix_icon=ft.Icons.LOCK)
        error = ft.Text(color="red")

        def btn_login_click(e):
            res = vm.autenticar(email_f.value, clave_f.value)
            if res["exito"]:
                view_dashboard(res["nombre"])
            else:
                error.value = res["mensaje"]
                page.update()

        page.add(
            ft.Icon(ft.Icons.FITNESS_CENTER_ROUNDED, size=60, color="blue"),
            ft.Text("GYM PRO LOGIN", size=25, weight="bold"),
            email_f, clave_f, error,
            ft.FilledButton("ENTRAR", on_click=btn_login_click, width=300),
            ft.Row([
                ft.TextButton("Olvidé mi clave"),
                ft.TextButton("Regístrate", on_click=lambda _: view_registro())
            ], alignment="center")
        )
        page.update()

    view_login()

if __name__ == "__main__":
    # Cambiamos ft.app por ft.run para quitar el aviso de Deprecation
    ft.run(main)