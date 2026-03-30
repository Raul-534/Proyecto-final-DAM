import flet as ft
from viewmodels.login_viewmodel import LoginViewModel
from vistas.perfil_view import PerfilView
from vistas.resultado_view import ResultadoView

def main(page: ft.Page):
    page.title = "GYM PRO - Desktop"
    page.window.width = 400
    page.window.height = 700
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 40

    # Inicialización del ViewModel
    try:
        vm = LoginViewModel()
    except Exception as e:
        page.add(ft.Text(f"Error de conexión: {e}", color="red"))
        page.update()
        return

    # --- FUNCIONES DE NAVEGACIÓN ---

    def navegar_a_resultado(nombre, kcal):
        page.controls.clear()
        # Pasamos view_dashboard como el callback para el botón "Volver"
        page.add(ResultadoView(page, nombre, kcal, view_dashboard))
        page.update()

    def navegar_a_perfil(nombre):
        page.controls.clear()
        # Le pasamos: page, nombre, función de cálculo, y función para volver (dashboard)
        page.add(PerfilView(page, nombre, navegar_a_resultado, view_dashboard))
        page.update()

    def view_dashboard(nombre_usuario):
        page.controls.clear()
        
        def crear_tarjeta(texto, icono, color, click_func):
            return ft.Container(
                content=ft.Column([
                    ft.Icon(icono, size=35, color=color),
                    ft.Text(texto, weight="bold", size=12)
                ], horizontal_alignment="center", alignment="center"),
                padding=10, bgcolor="#252525", border_radius=15,
                width=140, height=120, on_click=click_func, ink=True
            )

        page.add(
            ft.Text(f"¡Hola, {nombre_usuario}!", size=28, weight="bold"),
            ft.Text("¿Qué vamos a hacer hoy?", size=16, color="blue"),
            ft.Divider(height=20, color="transparent"),
            ft.Column([
                ft.Row([
                    crear_tarjeta("RUTINAS", ft.Icons.FITNESS_CENTER, "blue", None),
                    crear_tarjeta("PROGRESO", ft.Icons.SHOW_CHART, "green", None),
                ], alignment="center"),
                ft.Row([
                    crear_tarjeta("DIETAS", ft.Icons.RESTAURANT, "orange", None),
                    crear_tarjeta("PERFIL", ft.Icons.PERSON, "white", lambda _: navegar_a_perfil(nombre_usuario)),
                ], alignment="center"),
            ], spacing=15),
            ft.Divider(height=40, color="transparent"),
            ft.TextButton("CERRAR SESIÓN", on_click=lambda _: view_login(), icon=ft.Icons.LOGOUT, icon_color="red")
        )
        page.update()

    # --- VISTA: LOGIN (CORREGIDA) ---
    def view_login(e=None):
        page.controls.clear()
        
        email_f = ft.TextField(
            label="Email", 
            width=300, 
            prefix_icon=ft.Icons.EMAIL_ROUNDED,
            border_radius=10
        )
        clave_f = ft.TextField(
            label="Contraseña", 
            password=True, 
            can_reveal_password=True, 
            width=300, 
            prefix_icon=ft.Icons.LOCK_ROUNDED,
            border_radius=10
        )
        error_txt = ft.Text(color="red", size=12)

        def btn_login_click(e):
            # Aquí usamos tu LoginViewModel real
            res = vm.autenticar(email_f.value, clave_f.value)
            if res["exito"]:
                view_dashboard(res["nombre"])
            else:
                error_txt.value = res["mensaje"]
                page.update()

        # Diseño del Login
        page.add(
            ft.Column([
                ft.Icon(ft.Icons.FITNESS_CENTER_ROUNDED, size=80, color="blue"),
                ft.Text("GYM PRO", size=32, weight="bold"),
                ft.Text("Tu entrenador personal en casa", color="grey"),
                ft.Divider(height=20, color="transparent"),
                email_f,
                clave_f,
                error_txt,
                ft.Divider(height=10, color="transparent"),
                ft.FilledButton(
                    "ENTRAR", 
                    on_click=btn_login_click, 
                    width=300, 
                    height=50,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                ),
                ft.Row([
                    ft.Text("¿Eres nuevo?"),
                    ft.TextButton("Regístrate aquí", on_click=lambda _: print("Ir a registro"))
                ], alignment="center")
            ], horizontal_alignment="center", spacing=10)
        )
        page.update()

    view_login()

if __name__ == "__main__":
    ft.run(main)