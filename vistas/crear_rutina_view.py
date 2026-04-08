import flet as ft
from viewmodels.rutinas_viewmodel import RutinasViewModel

def CrearRutinaView(page: ft.Page, id_usuario, nombre_usuario, volver_callback):
    vm = RutinasViewModel()
    
    ejercicios_en_rutina = {} 
    lista_seleccionados_ui = ft.ListView(
        spacing=10,
        expand=True
    )    
    nombre_in = ft.TextField(
        label="Nombre de la Rutina", 
        hint_text="Ej: Pierna / Empuje",
        border_radius=10, 
        expand=True,
        height=70, 
        text_size=14
    )
    
    nivel_drop = ft.Dropdown(
        label="Dificultad",
        value="Intermedio",
        width=160, 
        height=70,
        options=[
            ft.dropdown.Option("Principiante"),
            ft.dropdown.Option("Intermedio"),
            ft.dropdown.Option("Avanzado")
        ]
    )

    def salir(e=None):
        page.clean()
        volver_callback(id_usuario, nombre_usuario)

    def eliminar_ejercicio(id_ej):
        if id_ej in ejercicios_en_rutina:
            del ejercicios_en_rutina[id_ej]
            refrescar_pantalla()

    def refrescar_pantalla():
        lista_seleccionados_ui.controls.clear()
        for id_ej, info in ejercicios_en_rutina.items():
            lista_seleccionados_ui.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(info["nombre"], weight="bold", size=14),
                            ft.Text(info["grupo"], size=11, color="blue"),
                        ], expand=True, spacing=2),
                        info["S_input"], 
                        info["R_input"],
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE, 
                            icon_color="red", 
                            on_click=lambda _, i=id_ej: eliminar_ejercicio(i)
                        )
                    ], alignment="center"),
                    bgcolor="#252525", padding=10, border_radius=10
                )
            )
        page.update()

    def abrir_catalogo(e):
        items_bd = vm.obtener_ejercicios()
        lista_view = ft.ListView(expand=True, spacing=5)

        def toggle_ejercicio(ej, tile):
            id_e = ej.get('id_ejercicio') or ej.get('id')
            if id_e in ejercicios_en_rutina:
                del ejercicios_en_rutina[id_e]
                tile.trailing = ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE, color="grey")
            else:
                ejercicios_en_rutina[id_e] = {
                    "nombre": ej['nombre'],
                    "grupo": ej.get('nombre_grupo', 'General'),
                    "S_input": ft.TextField(
                        label="S", value="3", width=65, 
                        text_align="center", dense=True, 
                        keyboard_type=ft.KeyboardType.NUMBER
                    ),
                    "R_input": ft.TextField(
                        label="R", value="12", width=65, 
                        text_align="center", dense=True, 
                        keyboard_type=ft.KeyboardType.NUMBER
                    ),
                    "D_value": "60" 
                }
                tile.trailing = ft.Icon(ft.Icons.CHECK_CIRCLE, color="green")
            page.update()

        for ej in items_bd:
            id_act = ej.get('id_ejercicio') or ej.get('id')
            ya_esta = id_act in ejercicios_en_rutina
            tile = ft.ListTile(
                title=ft.Text(ej['nombre'], size=14, weight="w500"),
                subtitle=ft.Text(ej.get('nombre_grupo', ''), size=11),
                trailing=ft.Icon(
                    ft.Icons.CHECK_CIRCLE if ya_esta else ft.Icons.ADD_CIRCLE_OUTLINE,
                    color="green" if ya_esta else "grey"
                )
            )
            tile.on_click = lambda _, item=ej, t=tile: toggle_ejercicio(item, t)
            lista_view.controls.append(tile)

        def confirmar_seleccion(e):
            bs.open = False
            page.update()
            refrescar_pantalla()

        bs = ft.BottomSheet(
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Catálogo", size=18, weight="bold", expand=True),
                        ft.IconButton(ft.Icons.CLOSE, on_click=lambda _: confirmar_seleccion(None))
                    ]),
                    ft.Container(content=lista_view, height=380),
                    ft.FilledButton("AÑADIR SELECCIONADOS", icon=ft.Icons.DONE_ALL, on_click=confirmar_seleccion, width=400)
                ], tight=True),
                padding=20, bgcolor="#1A1A1A",
                border_radius=ft.BorderRadius(top_left=20, top_right=20, bottom_left=0, bottom_right=0)
            ),
            open=True
        )
        page.overlay.append(bs)
        page.update()

    def guardar_rutina(e):
        # 1. Validación de nombre y existencia de ejercicios
        if not nombre_in.value or not ejercicios_en_rutina:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Falta nombre de rutina o añadir ejercicios"), bgcolor="orange")
            page.snack_bar.open = True
            page.update()
            return
        
        # 2. Validación de que series y reps no estén vacíos
        for id_ej, info in ejercicios_en_rutina.items():
            if not info["S_input"].value or not info["R_input"].value:
                page.snack_bar = ft.SnackBar(ft.Text(f"⚠️ Revisa las series/reps de {info['nombre']}"), bgcolor="orange")
                page.snack_bar.open = True
                page.update()
                return

        datos_bd = [{"id": k, "series": v["S_input"].value, "reps": v["R_input"].value, "descanso": v["D_value"]} 
                    for k, v in ejercicios_en_rutina.items()]

        # 3. Guardado con mensaje de éxito
        if vm.guardar_rutina_completa(id_usuario, nombre_in.value, nivel_drop.value, datos_bd):
            page.snack_bar = ft.SnackBar(ft.Text("¡Rutina guardada con éxito! ✅"), bgcolor="green")
            page.snack_bar.open = True
            import time
            page.update()
            time.sleep(1)
            salir()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Error al guardar la rutina"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    return ft.Container(
        padding=15,
        content=ft.Column([
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK_IOS, on_click=salir, icon_size=18),
                ft.Text("NUEVA RUTINA", size=22, weight="bold"),
            ]),
            ft.Row([nombre_in, nivel_drop], spacing=10),
            ft.FilledTonalButton("ABRIR CATÁLOGO", icon=ft.Icons.SEARCH, on_click=abrir_catalogo, width=400, height=45),
            ft.Text("EJERCICIOS AÑADIDOS:", size=11, weight="bold", color="grey"),
            ft.Container(
                content=lista_seleccionados_ui,
                expand=True,
                height=300
            ),
            ft.FilledButton("GUARDAR TODO", icon=ft.Icons.SAVE, width=400, height=55, on_click=guardar_rutina)
        ], spacing=10, expand=True)
    )