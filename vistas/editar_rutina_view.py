import flet as ft
from viewmodels.rutinas_viewmodel import RutinasViewModel

def EditarRutinaView(page: ft.Page, id_usuario, nombre_usuario, id_rutina, volver_callback):
    vm = RutinasViewModel()
    
    ejercicios_seleccionados = {} 
    lista_ui = ft.ListView(spacing=10, expand=True)

    nombre_in = ft.TextField(label="Nombre de la Rutina", border_radius=10)
    nivel_drop = ft.Dropdown(
        label="Nivel",
        options=[
            ft.dropdown.Option("Principiante"),
            ft.dropdown.Option("Intermedio"),
            ft.dropdown.Option("Avanzado")
        ],
        border_radius=10
    )

    def refrescar_lista_pantalla():
        lista_ui.controls.clear()
        for id_e, info in ejercicios_seleccionados.items():
            lista_ui.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(info["nombre"], weight="bold"),
                            ft.Text(info["grupo"], size=11, color="blue"),
                        ], expand=True),
                        info["S_in"], 
                        info["R_in"],
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE, 
                            icon_color="red", 
                            tooltip="Quitar ejercicio",
                            on_click=lambda _, i=id_e: eliminar_de_seleccion(i)
                        )
                    ]),
                    bgcolor="#252525", padding=10, border_radius=10
                )
            )
        page.update()

    def eliminar_de_seleccion(id_e):
        if id_e in ejercicios_seleccionados:
            del ejercicios_seleccionados[id_e]
            refrescar_lista_pantalla()

    def abrir_catalogo(e):
        todos = vm.obtener_ejercicios()
        lista_catalogo = ft.ListView(expand=True, spacing=5)

        def toggle_ejercicio(ej, tile):
            id_e = ej.get('id_ejercicio') or ej.get('id')
            if id_e in ejercicios_seleccionados:
                del ejercicios_seleccionados[id_e]
                tile.trailing = ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE, color="grey")
            else:
                ejercicios_seleccionados[id_e] = {
                    "nombre": ej['nombre'],
                    "grupo": ej.get('nombre_grupo', 'General'),
                    "S_in": ft.TextField(value="3", width=65, label="S", dense=True),
                    "R_in": ft.TextField(value="12", width=65, label="R", dense=True),
                    "descanso": "60"
                }
                tile.trailing = ft.Icon(ft.Icons.CHECK_CIRCLE, color="green")
            page.update()

        for ej in todos:
            id_act = ej.get('id_ejercicio') or ej.get('id')
            ya_esta = id_act in ejercicios_seleccionados
            
            tile = ft.ListTile(
                title=ft.Text(ej['nombre']),
                trailing=ft.Icon(
                    ft.Icons.CHECK_CIRCLE if ya_esta else ft.Icons.ADD_CIRCLE_OUTLINE,
                    color="green" if ya_esta else "grey"
                )
            )
            tile.on_click = lambda _, item=ej, t=tile: toggle_ejercicio(item, t)
            lista_catalogo.controls.append(tile)

        bs = ft.BottomSheet(
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Catálogo de Ejercicios", size=18, weight="bold", expand=True),
                        ft.IconButton(ft.Icons.CLOSE, on_click=lambda _: cerrar_bs(bs))
                    ]),
                    ft.Container(content=lista_catalogo, height=400),
                    ft.FilledButton("ACEPTAR", width=400, on_click=lambda _: cerrar_bs(bs))
                ], tight=True),
                padding=20, bgcolor="#1A1A1A"
            ),
            open=True
        )
        page.overlay.append(bs)
        page.update()

    def cerrar_bs(bs):
        bs.open = False
        page.update()
        refrescar_lista_pantalla()

    def guardar_cambios_click(e):
        if not nombre_in.value or not ejercicios_seleccionados:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, pon un nombre y añade ejercicios"), bgcolor="orange")
            page.snack_bar.open = True
            page.update()
            return

        lista_final = []
        for id_e, info in ejercicios_seleccionados.items():
            lista_final.append({
                "id": id_e,
                "series": info["S_in"].value,
                "reps": info["R_in"].value,
                "descanso": info["descanso"]
            })

        if vm.actualizar_rutina_completa(id_rutina, nombre_in.value, nivel_drop.value, lista_final):
            page.snack_bar = ft.SnackBar(ft.Text("Rutina actualizada ✅"), bgcolor="green")
            page.snack_bar.open = True
            volver_callback(id_usuario, nombre_usuario)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Error al guardar en la base de datos"), bgcolor="red")
            page.snack_bar.open = True
        page.update()

    def cargar_datos_actuales():
        rutina_info = vm.obtener_rutina_por_id(id_rutina)
        if rutina_info:
            nombre_in.value = rutina_info['nombre']
            nivel_drop.value = rutina_info.get('nivel') or rutina_info.get('dificultad')

        actuales = vm.obtener_detalles_rutina(id_rutina)
        for ej in actuales:
            id_e = ej['id_ejercicio']
            ejercicios_seleccionados[id_e] = {
                "nombre": ej['nombre'],
                "grupo": "Actual",
                "S_in": ft.TextField(value=str(ej['series']), width=65, label="S", dense=True),
                "R_in": ft.TextField(value=str(ej['repeticiones']), width=65, label="R", dense=True),
                "descanso": str(ej['descanso'])
            }
        refrescar_lista_pantalla()

    cargar_datos_actuales()

    # Layout Principal
    return ft.Container(
        padding=ft.padding.only(left=15, right=15, bottom=30),
        expand=True, 
        content=ft.Column([
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: volver_callback(id_usuario, nombre_usuario)),
                ft.Text("EDITAR RUTINA", size=22, weight="bold"),
            ]),
            
            nombre_in,
            nivel_drop,
            ft.FilledTonalButton(
                "MODIFICAR EJERCICIOS", 
                icon=ft.Icons.LIST, 
                on_click=abrir_catalogo, 
                width=400
            ),
            
            ft.Divider(height=20),
            ft.Text("EJERCICIOS SELECCIONADOS:", size=12, color="grey", weight="bold"),
            
            ft.Container(
            content=lista_ui,
            expand=True,
            height=300
        ),
            
            ft.Column([
                ft.Divider(),
                ft.FilledButton(
                    "GUARDAR CAMBIOS", 
                    icon=ft.Icons.SAVE, 
                    width=400, 
                    height=50, 
                    on_click=guardar_cambios_click
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            
        ]) 
    )