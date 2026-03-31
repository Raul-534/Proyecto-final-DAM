import flet as ft

def ResultadoView(page: ft.Page, nombre_usuario, kcal, al_volver):
    # --- CONTENEDORES PARA LOS MACROS (Empiezan ocultos) ---
    txt_pro = ft.Text("", size=20, weight="bold", color=ft.Colors.ORANGE_400)
    txt_car = ft.Text("", size=20, weight="bold", color=ft.Colors.BLUE_400)
    txt_gra = ft.Text("", size=20, weight="bold", color=ft.Colors.PINK_400)
    
    detalles_container = ft.Container(
        content=ft.Column([
            ft.Text("Tu reparto de macros sugerido:", size=16, weight="bold"),
            ft.Row([
                ft.Column([ft.Text("Proteína"), txt_pro], horizontal_alignment="center"),
                ft.Column([ft.Text("Carbos"), txt_car], horizontal_alignment="center"),
                ft.Column([ft.Text("Grasas"), txt_gra], horizontal_alignment="center"),
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, width=300),
        ], horizontal_alignment="center"),
        bgcolor="#1A1A1A",
        padding=20,
        border_radius=15,
        visible=False  # ESTO ES EL "DIV OCULTO"
    )

    def cambiar_objetivo(e):
        obj = e.control.value
        # Ratios: [Prot %, Carb %, Gras %]
        ratios = {
            "perder": [0.40, 0.30, 0.30],
            "mantener": [0.30, 0.40, 0.30],
            "ganar": [0.25, 0.55, 0.20]
        }
        
        p_pct, c_pct, g_pct = ratios[obj]
        
        # Cálculo de gramos (Prot=4cal, Carb=4cal, Gras=9cal)
        g_pro = (kcal * p_pct) / 4
        g_car = (kcal * c_pct) / 4
        g_gra = (kcal * g_pct) / 9
        
        # Actualizamos textos y hacemos visible el contenedor
        txt_pro.value = f"{int(g_pro)}g"
        txt_car.value = f"{int(g_car)}g"
        txt_gra.value = f"{int(g_gra)}g"
        
        detalles_container.visible = True
        page.update()

    # Selector de objetivo
    select_obj = ft.Dropdown(
        label="¿Cuál es tu objetivo?",
        width=280,
        on_change=cambiar_objetivo,
        options=[
            ft.dropdown.Option(key="perder", text="Perder Grasa (Definición)"),
            ft.dropdown.Option(key="mantener", text="Mantener Peso"),
            ft.dropdown.Option(key="ganar", text="Ganar Músculo (Volumen)"),
        ]
    )

    return ft.Container(
        content=ft.Column([
            ft.Text("RESULTADOS", size=28, weight="bold"),
            
            # Bloque principal de calorías
            ft.Container(
                content=ft.Column([
                    ft.Text("Calorías diarias necesarias", size=14),
                    ft.Text(f"{kcal} Kcal", size=40, weight="bold", color=ft.Colors.GREEN_400),
                ], horizontal_alignment="center"),
                padding=20
            ),
            
            ft.Divider(height=10, color="transparent"),
            select_obj,
            ft.Divider(height=10, color="transparent"),
            
            # El "DIV" que aparece y desaparece
            detalles_container,
            
            ft.Divider(height=20, color="transparent"),
            ft.FilledButton("VOLVER AL MENÚ", width=280, on_click=lambda _: al_volver(nombre_usuario)),
        ], horizontal_alignment="center", alignment="center"),
        expand=True,
        alignment=ft.alignment.CENTER
    )