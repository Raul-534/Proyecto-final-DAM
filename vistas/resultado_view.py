import flet as ft

def ResultadoView(page: ft.Page, id_usuario, nombre_usuario, kcal, al_volver):
    txt_pro = ft.Text("", size=20, weight="bold", color=ft.Colors.ORANGE_400)
    txt_car = ft.Text("", size=20, weight="bold", color=ft.Colors.BLUE_400)
    txt_gra = ft.Text("", size=20, weight="bold", color=ft.Colors.PINK_400)
    
    detalles_container = ft.Container(
        content=ft.Column([
            ft.Text("Tu reparto de macros sugerido:", size=16, weight="bold"),
            ft.Row([
                ft.Column([ft.Text("Proteína"), txt_pro], horizontal_alignment="center"),
                ft.Column([ft.Text("Carbohidratos"), txt_car], horizontal_alignment="center"),
                ft.Column([ft.Text("Grasas"), txt_gra], horizontal_alignment="center"),
            ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, width=300),
        ], horizontal_alignment="center"),
        bgcolor="#1A1A1A",
        padding=20,
        border_radius=15,
        visible=False
    )

    def cambiar_objetivo(e):
        obj = e.control.value
        ratios = {
            "perder": [0.40, 0.30, 0.30],
            "mantener": [0.30, 0.40, 0.30],
            "ganar": [0.25, 0.55, 0.20]
        }
        
        p_pct, c_pct, g_pct = ratios[obj]
        
        g_pro = (kcal * p_pct) / 4
        g_car = (kcal * c_pct) / 4
        g_gra = (kcal * g_pct) / 9
        
        txt_pro.value = f"{int(g_pro)}g"
        txt_car.value = f"{int(g_car)}g"
        txt_gra.value = f"{int(g_gra)}g"
        
        detalles_container.visible = True
        page.update()

    select_obj = ft.Dropdown(
        label="¿Cuál es tu objetivo?",
        width=280,
        on_select=cambiar_objetivo,
        options=[
            ft.dropdown.Option(key="perder", text="Perder Grasa (Definición)"),
            ft.dropdown.Option(key="mantener", text="Mantener Peso"),
            ft.dropdown.Option(key="ganar", text="Ganar Músculo (Volumen)"),
        ]
    )

    return ft.Container(
        content=ft.Column([
            ft.Text("RESULTADOS", size=28, weight="bold"),
            
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
            
            detalles_container,
            
            ft.Divider(height=20, color="transparent"),
            ft.FilledButton("VOLVER AL MENÚ", width=280, on_click=lambda _: al_volver(id_usuario, nombre_usuario)),
        ], horizontal_alignment="center", alignment="center"),
        expand=True,
        alignment=ft.Alignment.CENTER
    )
    
import flet as ft

def DietasView(page, email_usuario, volver_callback):
    peso_usuario = 80 
    
    txt_calorias = ft.Text("2000", size=40, weight="bold", color="blue")
    prog_bar = ft.ProgressBar(value=0.5, color="blue", bgcolor="grey900")
    
    txt_prot = ft.Text("0/160g", size=10, color="grey")
    txt_carb = ft.Text("0/250g", size=10, color="grey")
    txt_gras = ft.Text("0/70g", size=10, color="grey")

    def actualizar_objetivo(e):
        objetivo = dd_objetivo.value
        
        if objetivo == "Bajar Peso":
            cals = 1800
            prot = peso_usuario * 2.2
            gras = peso_usuario * 0.8
        elif objetivo == "Subir Peso":
            cals = 2800
            prot = peso_usuario * 1.8
            gras = peso_usuario * 1.0
        else:
            cals = 2300
            prot = peso_usuario * 2.0
            gras = peso_usuario * 0.9
            
        carbs = (cals - (prot * 4) - (gras * 9)) / 4

        txt_calorias.value = str(cals)
        txt_prot.value = f"0/{int(prot)}g"
        txt_carb.value = f"0/{int(carbs)}g"
        txt_gras.value = f"0/{int(gras)}g"
        
        page.update()

    dd_objetivo = ft.Dropdown(
        label="Mi Objetivo",
        width=300,
        options=[
            ft.dropdown.Option("Bajar Peso"),
            ft.dropdown.Option("Mantener Peso"),
            ft.dropdown.Option("Subir Peso"),
        ],
        on_change=actualizar_objetivo,
        border_radius=10,
        value="Mantener Peso"
    )

    def crear_anillo(label, ref_text, color):
        return ft.Column([
            ft.Container(
                content=ft.ProgressRing(value=0.4, stroke_width=5, color=color),
                width=60, height=60, alignment=ft.Alignment.CENTER
            ),
            ft.Text(label, size=12, weight="bold"),
            ref_text
        ], horizontal_alignment="center")

    layout = ft.Column([
        ft.Row([
            ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: volver_callback()),
            ft.Text("DIETAS Y MACROS", size=24, weight="bold"),
        ]),
        
        ft.Text("Configura tu plan diario:", color="grey"),
        dd_objetivo,
        
        ft.Container(
            content=ft.Column([
                ft.Text("Calorías Objetivo", color="grey"),
                txt_calorias,
                prog_bar,
            ], horizontal_alignment="center"),
            padding=20, bgcolor="#1A1A1A", border_radius=20
        ),

        ft.Row([
            crear_anillo("PROT", txt_prot, "orange"),
            crear_anillo("CARB", txt_carb, "green"),
            crear_anillo("GRAS", txt_gras, "pink"),
        ], alignment="space_around"),
        
        ft.FilledButton("GUARDAR CONFIGURACIÓN", icon=ft.Icons.SAVE, width=300),
        
    ], scroll="auto", spacing=20, horizontal_alignment="center")

    return layout