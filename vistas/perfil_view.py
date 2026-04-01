import flet as ft
from viewmodels.perfil_viewmodel import PerfilViewModel

def PerfilView(page: ft.Page, id_usuario, nombre_usuario, al_calcular, al_volver):
    vm = PerfilViewModel()
    # Seguimos obteniendo datos por nombre si tu VM así lo requiere, 
    # aunque lo ideal a futuro sería usar el id_usuario también aquí.
    data = vm.obtener_datos(nombre_usuario)

    # Inputs
    ed_in = ft.TextField(label="Edad", width=85, border_radius=10, value=str(data['edad']) if data else "")
    pe_in = ft.TextField(label="Peso", width=85, border_radius=10, value=str(data['peso']) if data else "")
    al_in = ft.TextField(label="Altura", width=85, border_radius=10, value=str(data['altura']) if data else "")
    
    gen_radio = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="hombre", label="M"),
            ft.Radio(value="mujer", label="F"),
        ], alignment="center"),
        value=data['genero'] if data else "hombre"
    )

    act_drop = ft.Dropdown(
        label="Actividad Física", width=280, border_radius=10,
        value=str(data['actividad']) if data else "1.55",
        options=[
            ft.dropdown.Option(key="1.2", text="Sedentario"),
            ft.dropdown.Option(key="1.55", text="Moderado"),
            ft.dropdown.Option(key="1.9", text="Atleta"),
        ]
    )

    def validar_y_guardar(e):
        # --- VALIDACIÓN DE CAMPOS VACÍOS ---
        if not ed_in.value or not pe_in.value or not al_in.value:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("No dejes campos vacíos"),
                bgcolor=ft.Colors.ORANGE_700
            )
            page.snack_bar.open = True
            page.update()
            return

        try:
            p = float(pe_in.value.replace(",", "."))
            a = float(al_in.value.replace(",", "."))
            ev = int(ed_in.value)
            
            # Cálculo de TMB
            tmb = (10 * p) + (6.25 * a) - (5 * ev) + (5 if gen_radio.value == "hombre" else -161)
            kcal = tmb * float(act_drop.value)

            # Guardado en BD (Usamos nombre_usuario como pide tu VM actual)
            if vm.guardar_datos(nombre_usuario, {
                "peso": p, "altura": a, "edad": ev, "genero": gen_radio.value,
                "objetivo": "Mantener", "actividad": act_drop.value
            }):
                # --- REDIRECCIÓN CON ID Y NOMBRE ---
                # Importante: Enviamos el ID para que ResultadoView sepa a quién pertenece
                al_calcular(id_usuario, nombre_usuario, int(kcal))
                
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Introduce números válidos"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    return ft.Container(
        content=ft.Column([
            ft.Text("MI PERFIL FÍSICO", size=24, weight="bold"),
            ft.Text(f"Configuración para {nombre_usuario}", size=12, color="blue"),
            ft.Divider(height=20, color="transparent"),
            
            ft.Text("GÉNERO", size=12, weight="bold"),
            gen_radio,
            
            ft.Row([ed_in, pe_in, al_in], alignment="center", spacing=10),
            
            ft.Divider(height=10, color="transparent"),
            ft.Text("ACTIVIDAD", size=12, weight="bold"),
            act_drop,
             
            ft.Divider(height=30, color="transparent"), 
            ft.FilledButton("GUARDAR Y VER RESULTADO", width=280, height=55, on_click=validar_y_guardar),
            
            # --- BOTÓN CANCELAR CORREGIDO ---
            # Ahora envía id_usuario y nombre_usuario para que view_dashboard no de error
            ft.TextButton("CANCELAR", on_click=lambda _: al_volver(id_usuario, nombre_usuario))
            
        ], horizontal_alignment="center", alignment="center"),
        expand=True,
        alignment=ft.Alignment.CENTER
    )