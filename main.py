import flet as ft
from viewmodels.login_viewmodel import LoginViewModel
from vistas.dietas_view import DietasView
from vistas.perfil_view import PerfilView
from vistas.resultado_view import ResultadoView
from vistas.crear_rutina_view import CrearRutinaView
from vistas.menu_rutinas_view import MenuRutinasView
from vistas.editar_rutina_view import EditarRutinaView
from vistas.mis_rutinas_view import MisRutinasView

def main(page: ft.Page):
    page.title = "GYM PRO"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 800
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20

    try:
        vm = LoginViewModel()
    except Exception as e:
        page.add(ft.Text(f"Error: {e}", color="red"))
        return

    def mobile_container(content):
        return ft.Container(content=content, width=350, alignment=ft.Alignment.CENTER)

    # --- NAVEGACIÓN ---
    def navegar_a_dietas(id_u, email, nom_u):
        page.controls.clear()
        page.add(mobile_container(DietasView(
            page, nom_u, email, 
            volver_callback=lambda: view_dashboard(id_u, nom_u), 
            navegar_perfil_callback=lambda: navegar_a_perfil(id_u, nom_u)
        )))
        page.update()

    def navegar_a_rutinas(id_u, nom_u):
        page.controls.clear()
        page.add(mobile_container(MenuRutinasView(
            page, id_u, nom_u,
            volver_callback=lambda: view_dashboard(id_u, nom_u),
            ir_a_crear=lambda: navegar_a_crear_rutina(id_u, nom_u),
            ir_a_mis_rutinas=lambda: navegar_a_mis_rutinas(id_u, nom_u)
        )))
        page.update()

    def navegar_a_crear_rutina(id_u, nom_u):
        page.controls.clear()
        page.add(mobile_container(CrearRutinaView(
            page, id_u, nom_u,
            volver_callback=lambda id_x, nom_x: navegar_a_rutinas(id_x, nom_x)
        )))
        page.update()

    def navegar_a_mis_rutinas(id_u, nom_u):
        page.controls.clear()
        page.add(mobile_container(MisRutinasView(
            page, id_u, nom_u,
            volver_callback=lambda id_x, nom_x: navegar_a_rutinas(id_x, nom_x),
            editar_rutina_callback=lambda id_r, nom_r: navegar_a_editar_rutina(id_u, nom_u, id_r, nom_r)
        )))
        page.update()

    def navegar_a_editar_rutina(id_u, nom_u, id_r, nom_r):
        page.controls.clear()
        page.add(mobile_container(EditarRutinaView(
            page, id_u, nom_u, id_r, 
            volver_callback=lambda id_x, nom_x: navegar_a_mis_rutinas(id_x, nom_x)
        )))
        page.update()

    def navegar_a_perfil(id_u, nom_u):
        page.controls.clear()
        page.add(mobile_container(PerfilView(page, id_u, nom_u, navegar_a_resultado, view_dashboard)))
        page.update()

    def navegar_a_resultado(id_usuario, nombre, kcal):
        page.controls.clear()
        page.add(mobile_container(ResultadoView(page, id_usuario, nombre, kcal, view_dashboard)))
        page.update()

    def view_dashboard(id_usuario, nombre_usuario):
        page.controls.clear()
        email_actual = getattr(vm, 'email_actual', "usuario@test.com")

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
                        crear_tarjeta("RUTINAS", ft.Icons.FITNESS_CENTER, "blue", 
                                      lambda _: navegar_a_rutinas(id_usuario, nombre_usuario)),
                        crear_tarjeta("PROGRESO", ft.Icons.SHOW_CHART, "green", 
                                      lambda _: print(f"Seguimiento para ID: {id_usuario}")),
                    ], alignment="center"),
                    ft.Row([
                        crear_tarjeta("DIETAS", ft.Icons.RESTAURANT, "orange", 
                                      lambda _: navegar_a_dietas(id_usuario, email_actual, nombre_usuario)),
                        crear_tarjeta("PERFIL", ft.Icons.PERSON, "white", 
                                      lambda _: navegar_a_perfil(id_usuario, nombre_usuario)),
                    ], alignment="center"),
                    ft.Divider(height=20, color="transparent"),
                    ft.TextButton("CERRAR SESIÓN", on_click=lambda _: view_login(), icon=ft.Icons.LOGOUT, icon_color="red")
                ], horizontal_alignment="center")
            )
        )
        page.update()

    # --- LOGIN ---
    def view_login(e=None):
        page.controls.clear()
        ema = ft.TextField(label="Email", width=300, border_radius=10)
        cla = ft.TextField(label="Contraseña", password=True, width=300, border_radius=10)
        
        def log(e):
            res = vm.autenticar(ema.value, cla.value)
            if res["exito"]:
                vm.email_actual = ema.value
                view_dashboard(res["id_usuario"], res["nombre"])
            else: 
                page.snack_bar = ft.SnackBar(ft.Text("Credenciales incorrectas"))
                page.snack_bar.open = True
                page.update()

        page.add(mobile_container(ft.Column([
            ft.Icon(ft.Icons.FITNESS_CENTER, size=80, color="blue"),
            ft.Text("GYM PRO", size=32, weight="bold"),
            ema, cla,
            ft.FilledButton(content=ft.Text("ENTRAR"), on_click=log, width=300, height=50),
            ft.TextButton("¿Has olvidado tu contraseña?", on_click=lambda _: view_recuperar()),
            ft.Row([ft.Text("¿Eres nuevo?"), ft.TextButton("Regístrate", on_click=lambda _: view_registro())], alignment="center")
        ], horizontal_alignment="center")))
        page.update()

    # --- RECUPERAR CONTRASEÑA ---
    def view_recuperar(e=None):
        page.controls.clear()
        email_f = ft.TextField(label="Email", width=300, border_radius=10)
        codigo_f = ft.TextField(label="Código de 6 dígitos", width=300, border_radius=10, visible=False)
        pass_f = ft.TextField(label="Nueva Contraseña", password=True, width=300, border_radius=10, visible=False)
        msg_status = ft.Text("", size=12)
        
        token_servidor = [None]
        email_memoria = [None]

        btn_accion = ft.FilledButton(content=ft.Text("ENVIAR CÓDIGO"), width=300, height=50)

        def manejar_pasos(e):
            if btn_accion.content.value == "ENVIAR CÓDIGO":
                res = vm.recuperar_password(email_f.value)
                if res["exito"]:
                    token_servidor[0] = str(res["token"])
                    email_memoria[0] = email_f.value
                    email_f.visible = False
                    codigo_f.visible = True
                    btn_accion.content.value = "COMPROBAR CÓDIGO"
                    msg_status.value = "Código enviado a tu correo"
                    msg_status.color = "blue"
                else:
                    msg_status.value = "Email no registrado"
                    msg_status.color = "red"
            
            elif btn_accion.content.value == "COMPROBAR CÓDIGO":
                if codigo_f.value == token_servidor[0]:
                    codigo_f.visible = False
                    pass_f.visible = True
                    btn_accion.content.value = "CAMBIAR CONTRASEÑA"
                    msg_status.value = "Código verificado."
                    msg_status.color = "green"
                else:
                    msg_status.value = "Código incorrecto"
                    msg_status.color = "red"
            
            elif btn_accion.content.value == "CAMBIAR CONTRASEÑA":
                if vm.cambiar_password(email_memoria[0], pass_f.value) == "OK":
                    page.snack_bar = ft.SnackBar(ft.Text("Contraseña actualizada ✅"), bgcolor="green")
                    page.snack_bar.open = True
                    view_login()
                else:
                    msg_status.value = "Error al actualizar"
                    msg_status.color = "red"
            page.update()

        btn_accion.on_click = manejar_pasos
        page.add(mobile_container(ft.Column([
            ft.Icon(ft.Icons.LOCK_RESET, size=80, color="blue"),
            ft.Text("RECUPERACIÓN", size=28, weight="bold"),
            email_f, codigo_f, pass_f, msg_status,
            btn_accion,
            ft.TextButton("Cancelar", on_click=lambda _: view_login())
        ], horizontal_alignment="center")))
        page.update()

    # --- REGISTRO ---
    def view_registro(e=None):
        page.controls.clear()
        n = ft.TextField(label="Nombre", width=300, border_radius=10)
        em = ft.TextField(label="Email", width=300, border_radius=10)
        cl = ft.TextField(label="Contraseña", password=True, width=300, border_radius=10)
        def reg(e):
            if vm.registrar(n.value, em.value, cl.value) == "OK": view_login()
        page.add(mobile_container(ft.Column([
            ft.Icon(ft.Icons.PERSON_ADD, size=80, color="blue"),
            ft.Text("REGISTRO", size=28, weight="bold"),
            n, em, cl,
            ft.FilledButton(content=ft.Text("CREAR CUENTA"), on_click=reg, width=300, height=50),
            ft.TextButton("Volver", on_click=lambda _: view_login())
        ], horizontal_alignment="center")))
        page.update()

    view_login()

if __name__ == "__main__":
    ft.app(target=main)