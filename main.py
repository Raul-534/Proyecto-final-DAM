import flet as ft
from viewmodels.login_viewmodel import LoginViewModel
import time

def main(page: ft.Page):
    page.title = "GYM PRO - Mobile"
    page.window.width = 400
    page.window.height = 750
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    vm = LoginViewModel()

    def view_dashboard(nombre_usuario):
        page.controls.clear()
        
        def crear_tarjeta(texto, icono, color_icon, click_func=None):
            return ft.Container(
                content=ft.Column([
                    ft.Icon(icono, size=35, color=color_icon),
                    ft.Text(texto, weight="bold", size=12)
                ], horizontal_alignment="center", alignment="center"),
                padding=10,
                bgcolor="#252525", 
                border_radius=15,
                width=140,
                height=120,
                on_click=click_func,
                ink=True
            )

        page.add(
            ft.Text(f"¡Hola, {nombre_usuario}!", size=28, weight="bold"),
            ft.Text("¿Qué vamos a entrenar?", size=16, color="blue"),
            ft.Divider(height=20, color="transparent"),
            ft.Column([
                ft.Row([
                    crear_tarjeta("MIS RUTINAS", "fitness_center", "blue"),
                    crear_tarjeta("PROGRESO", "show_chart", "green"),
                ], alignment="center"),
                ft.Row([
                    crear_tarjeta("DIETAS", "restaurant", "orange"),
                    crear_tarjeta("PERFIL", "person", "white", lambda _: view_perfil(nombre_usuario)),
                ], alignment="center"),
            ], spacing=15),
            ft.Divider(height=20, color="transparent"),
            ft.ElevatedButton("CERRAR SESIÓN", on_click=lambda _: view_login(), color="red")
        )
        page.update()

    def view_perfil(nombre_usuario):
        page.controls.clear()
        
        edad_i = ft.TextField(label="Edad", width=100, keyboard_type=ft.KeyboardType.NUMBER)
        peso_i = ft.TextField(label="Peso (kg)", width=120, keyboard_type=ft.KeyboardType.NUMBER)
        altura_i = ft.TextField(label="Altura (cm)", width=120, keyboard_type=ft.KeyboardType.NUMBER)

        genero_sel = ft.SegmentedButton(
            selected={"hombre"},
            allow_multiple_selection=False,
            segments=[
                ft.Segment(value="hombre", label=ft.Text("Hombre"), icon=ft.Icon("male")),
                ft.Segment(value="mujer", label=ft.Text("Mujer"), icon=ft.Icon("female")),
            ],
        )

        def on_chip_select(e, container):
            for chip in container.controls:
                chip.selected = False
            e.control.selected = True
            page.update()

        obj_row = ft.Row(alignment="center", wrap=True)
        obj_row.controls = [
            ft.ChoiceChip(label=ft.Text("Perder Grasa"), on_select=lambda e: on_chip_select(e, obj_row)),
            ft.ChoiceChip(label=ft.Text("Ganar Músculo"), selected=True, on_select=lambda e: on_chip_select(e, obj_row)),
            ft.ChoiceChip(label=ft.Text("Mantener"), on_select=lambda e: on_chip_select(e, obj_row)),
        ]

        act_row = ft.Row(alignment="center", wrap=True)
        act_row.controls = [
            ft.ChoiceChip(label=ft.Text("Sedentario"), on_select=lambda e: on_chip_select(e, act_row)),
            ft.ChoiceChip(label=ft.Text("Moderado"), selected=True, on_select=lambda e: on_chip_select(e, act_row)),
            ft.ChoiceChip(label=ft.Text("Atleta"), on_select=lambda e: on_chip_select(e, act_row)),
        ]

        # LÓGICA DE CALCULO HARRIS-BENEDICT
        def btn_calcular_click(e):
            try:
                p = float(peso_i.value)
                a = float(altura_i.value)
                ed = float(edad_i.value)
                gen = list(genero_sel.selected)[0]
                
                # TMB
                if gen == "hombre":
                    tmb = 88.36 + (13.4 * p) + (4.8 * a) - (5.7 * ed)
                else:
                    tmb = 447.59 + (9.2 * p) + (3.1 * a) - (4.3 * ed)
                
                # Actividad
                act_val = next(c.label.value for c in act_row.controls if c.selected)
                factores = {"Sedentario": 1.2, "Moderado": 1.55, "Atleta": 1.9}
                total = tmb * factores[act_val]
                
                page.open(ft.AlertDialog(title=ft.Text(f"Resultado: {total:.0f} kcal/día")))
            except:
                page.open(ft.SnackBar(ft.Text("Por favor, introduce números válidos")))

        page.add(
            ft.SafeArea(
                ft.Column([
                    ft.Row([
                        ft.IconButton("arrow_back", on_click=lambda _: view_dashboard(nombre_usuario)),
                        ft.Text("MI PERFIL", size=22, weight="bold"),
                    ], alignment="spaceBetween"),
                    ft.Text("Información Básica", color="blue", weight="bold"),
                    genero_sel,
                    ft.Row([edad_i, peso_i, altura_i], alignment="center", wrap=True),
                    ft.Divider(),
                    ft.Text("Objetivo", weight="bold"),
                    obj_row,
                    ft.Text("Actividad", weight="bold"),
                    act_row,
                    ft.Divider(height=20, color="transparent"),
                    ft.FilledButton("CALCULAR PLAN", icon="calculate", width=350, height=50, on_click=btn_calcular_click)
                ], scroll="auto", horizontal_alignment="center", spacing=15)
            )
        )
        page.update()

    def view_registro(e=None):
        page.controls.clear()
        
        nombre_i = ft.TextField(label="Nombre Completo", prefix_icon="person", border_radius=10)
        email_i = ft.TextField(label="Email", prefix_icon="email", border_radius=10)
        clave_i = ft.TextField(
            label="Contraseña", 
            password=True, 
            can_reveal_password=True, 
            prefix_icon="lock",
            border_radius=10
        )
        msg = ft.Text()

        def btn_reg_click(e):
            if not nombre_i.value or not email_i.value or not clave_i.value:
                msg.value = "Por favor, rellena todos los campos."
                msg.color = "orange"
                page.update()
                return
                
            res = vm.registrar(nombre_i.value, email_i.value, clave_i.value)
            if res == "OK":
                msg.value = "¡Usuario creado! Ya puedes entrar."
                msg.color = "green"
                import time
                page.update()
                time.sleep(1.5)
                view_login()
            else:
                msg.value = res
                msg.color = "red"
            page.update()

        page.add(
            ft.SafeArea(
                ft.Column([
                    ft.Icon("person_add", size=50, color="blue"),
                    ft.Text("NUEVA CUENTA", size=25, weight="bold"),
                    ft.Text("Únete a la comunidad GYM PRO", size=14, color="grey"),
                    
                    ft.Divider(height=10, color="transparent"),
                    
                    nombre_i, 
                    email_i, 
                    clave_i, 
                    msg,
                    
                    ft.Divider(height=10, color="transparent"),
                    
                    ft.FilledButton(
                        "CREAR CUENTA", 
                        on_click=btn_reg_click, 
                        width=300,
                        height=50
                    ),
                    
                    ft.TextButton("¿Ya tienes cuenta? Inicia sesión", on_click=lambda _: view_login())
                    
                ], horizontal_alignment="center", spacing=15)
            )
        )
        page.update()

    def view_login(e=None):
        page.controls.clear()
        email_f = ft.TextField(label="Email", width=300, prefix_icon="person")
        clave_f = ft.TextField(label="Contraseña", password=True, width=300, prefix_icon="lock")
        error = ft.Text(color="red")

        def btn_login_click(e):
            res = vm.autenticar(email_f.value, clave_f.value)
            if res["exito"]:
                view_dashboard(res["nombre"])
            else:
                error.value = res["mensaje"]
                page.update()

        page.add(
            ft.Icon("fitness_center", size=60, color="blue"),
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
    ft.app(target=main)