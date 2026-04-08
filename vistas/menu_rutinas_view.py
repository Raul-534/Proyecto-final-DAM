import flet as ft

def MenuRutinasView(page, id_usuario, nombre_usuario, volver_callback, ir_a_crear, ir_a_mis_rutinas):
    
    estilo_boton = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=15),
        padding=25,
    )

    return ft.Column([
        ft.Row([
            ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: volver_callback()),
            ft.Text("ENTRENAMIENTO", size=22, weight="bold")
        ]),
        
        ft.Divider(height=20, color="transparent"),
        
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.LIST_ALT_ROUNDED, size=40, color="blue"),
                ft.Text("MIS RUTINAS", size=18, weight="bold"),
                ft.Text("Ver, editar o eliminar tus planes", size=12, color="grey"),
            ], horizontal_alignment="center"),
            padding=30,
            bgcolor="#1E1E1E",
            border_radius=20,
            on_click=lambda _: ir_a_mis_rutinas(),
            ink=True,
            alignment=ft.Alignment.CENTER,
        ),
        
        ft.Divider(height=10, color="transparent"),
        
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE_ROUNDED, size=40, color="green"),
                ft.Text("CREAR RUTINA", size=18, weight="bold"),
                ft.Text("Diseña un nuevo entrenamiento", size=12, color="grey"),
            ], horizontal_alignment="center"),
            padding=30,
            bgcolor="#1E1E1E",
            border_radius=20,
            on_click=lambda _: ir_a_crear(),
            ink=True,
            alignment=ft.Alignment.CENTER,
        ),
        
        ft.Divider(height=40, color="transparent"),
        
        ft.Text(
            "Selecciona una opción para gestionar tus entrenamientos.",
            size=12, 
            color="grey", 
            text_align="center"
        )
    ], horizontal_alignment="center", spacing=10)