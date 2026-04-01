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
        page.add(ft.Text(f"Error al iniciar ViewModel: {e}", color="red"))
        return

    def mobile_container(content):
        return ft.Container(content=content, width=350, alignment=ft.Alignment.CENTER)

    # --- NAVEGACIÓN ACTUALIZADA POR ID ---

    def navegar_a_resultado(id_usuario, nombre, kcal):
        page.controls.clear()
        # Pasamos ID para que pueda volver correctamente
        page.add(mobile_container(ResultadoView(page, id_usuario, nombre, kcal, view_dashboard)))
        page.update()

    def navegar_a_perfil(id_usuario, nombre):
        page.controls.clear()
        page.add(mobile_container(PerfilView(page, id_usuario, nombre, navegar_a_resultado, view_dashboard)))
        page.update()
        
    def navegar_a_dietas(id_usuario, email, nombre):
        page.controls.clear()
        page.add(mobile_container(DietasView(
            page, nombre, email, 
            volver_callback=lambda: view_dashboard(id_usuario, nombre), 
            navegar_perfil_callback=lambda: navegar_a_perfil(id_usuario, nombre)
        )))
        page.update()

    def navegar_a_rutinas(id_usuario, nombre_usuario):
        page.controls.clear()
        page.add(mobile_container(MenuRutinasView(
            page, id_usuario, nombre_usuario,
            volver_callback=lambda: view_dashboard(id_usuario, nombre_usuario),
            ir_a_crear=lambda: navegar_a_crear_rutina(id_usuario, nombre_usuario),
            ir_a_mis_rutinas=lambda: navegar_a_mis_rutinas(id_usuario, nombre_usuario)
        )))
        page.update()

    def navegar_a_mis_rutinas(id_usuario, nombre_usuario):
        page.controls.clear()
        page.add(mobile_container(MisRutinasView(
            page, id_usuario, nombre_usuario,
            volver_callback=lambda: navegar_a_rutinas(id_usuario, nombre_usuario),
            editar_rutina_callback=lambda id_r, nom_r: navegar_a_editar_rutina(id_usuario, nombre_usuario, id_r, nom_r)
        )))
        page.update()

    def navegar_a_crear_rutina(id_usuario, nombre_usuario):
        page.controls.clear()
        page.add(mobile_container(CrearRutinaView(
            page, id_usuario, nombre_usuario,
            volver_callback=lambda: navegar_a_rutinas(id_usuario, nombre_usuario)
        )))
        page.update()

    def navegar_a_editar_rutina(id_usuario, nombre_usuario, id_rutina, nombre_rutina):
        page.controls.clear()
        page.add(mobile_container(EditarRutinaView(
            page, id_usuario, nombre_usuario, id_rutina, 
            volver_callback=lambda: navegar_a_mis_rutinas(id_usuario, nombre_usuario)
        )))
        page.update()

    # --- VISTA: DASHBOARD (Ahora recibe ID y Nombre) ---
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

    # --- VISTA: LOGIN (Captura el ID) ---
    def view_login(e=None):
        page.controls.clear()
        email_f = ft.TextField(label="Email", width=300, border_radius=10)
        clave_f = ft.TextField(label="Contraseña", password=True, width=300, border_radius=10)
        error_msg = ft.Text("", color="red", weight="bold")

        def login_click(e):
            res = vm.autenticar(email_f.value, clave_f.value)
            if res["exito"]:
                vm.email_actual = email_f.value 
                # Pasamos res["id"] que viene de la base de datos
                view_dashboard(res["id_usuario"], res["nombre"])
            else:
                error_msg.value = "Credenciales incorrectas"
                page.update()

        page.add(
            mobile_container(
                ft.Column([
                    ft.Icon(ft.Icons.FITNESS_CENTER, size=80, color="blue"),
                    ft.Text("GYM PRO", size=32, weight="bold"),
                    email_f, clave_f, error_msg,
                    ft.FilledButton(content=ft.Text("ENTRAR"), on_click=login_click, width=300, height=50),
                    ft.Row([ft.Text("¿Eres nuevo?"), ft.TextButton("Regístrate", on_click=lambda _: view_registro())], alignment="center")
                ], horizontal_alignment="center")
            )
        )
        page.update()

# --- VISTA: RECUPERAR CONTRASEÑA ---

    def view_recuperar(e=None):

        page.controls.clear()

        

        email_f = ft.TextField(label="Email", width=300, border_radius=10, prefix_icon=ft.Icons.EMAIL)

        codigo_f = ft.TextField(label="Introduce el código de 6 dígitos", width=300, border_radius=10, visible=False)

        pass_f = ft.TextField(label="Nueva Contraseña", password=True, width=300, border_radius=10, visible=False)

        msg_status = ft.Text("", size=12)

        

        codigo_esperado = [None]

        email_usuario = [None]



        # CORRECCIÓN: Usar 'label' en lugar de 'content' para el texto simple

        btn_principal = ft.FilledButton(

            label="ENVIAR CÓDIGO", 

            width=300, 

            height=50

        )



        def manejar_flujo(e):

            # PASO 1: Enviar Código

            if btn_principal.label == "ENVIAR CÓDIGO":

                res = vm.recuperar_password(email_f.value)

                if res["exito"]:

                    codigo_esperado[0] = res["token"]

                    email_usuario[0] = email_f.value

                    email_f.visible = False

                    codigo_f.visible = True

                    btn_principal.label = "COMPROBAR CÓDIGO" 

                    msg_status.value = "Código enviado a tu Gmail"

                    msg_status.color = "blue"

                else:

                    msg_status.value = "Email no encontrado"

                    msg_status.color = "red"

            

            # PASO 2: Comprobar Código

            elif btn_principal.label == "COMPROBAR CÓDIGO":

                if codigo_f.value == codigo_esperado[0]:

                    codigo_f.visible = False

                    pass_f.visible = True

                    btn_principal.label = "ACTUALIZAR CONTRASEÑA"

                    msg_status.value = "Código correcto."

                    msg_status.color = "green"

                else:

                    msg_status.value = "Código incorrecto"

                    msg_status.color = "red"

            

            # PASO 3: Actualizar y finalizar

            elif btn_principal.label == "ACTUALIZAR CONTRASEÑA":

                res_db = vm.cambiar_password(email_usuario[0], pass_f.value)

                if res_db == "OK":

                    pass_f.disabled = True

                    btn_principal.label = "VOLVER AL LOGIN"

                    btn_principal.bgcolor = "green"

                    msg_status.value = "Contraseña cambiada con éxito"

                    msg_status.color = "green"

                else:

                    msg_status.value = res_db

                    msg_status.color = "red"

            

            # PASO 4: Salida

            elif btn_principal.label == "VOLVER AL LOGIN":

                view_login()



            page.update()



        btn_principal.on_click = manejar_flujo



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

                    ft.FilledButton(label="CREAR CUENTA", on_click=registrar_click, width=300),

                    ft.TextButton("Ya tengo cuenta", on_click=lambda _: view_login())

                ], horizontal_alignment="center")

            )

        )

        page.update()
    
    view_login()

if __name__ == "__main__":
    ft.run(main)