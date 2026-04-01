import flet as ft
from viewmodels.rutinas_viewmodel import RutinasViewModel

def CrearRutinaView(page: ft.Page, id_usuario, nombre_usuario, volver_callback):
    vm = RutinasViewModel()
    ejercicios_db = vm.obtener_ejercicios()
    seleccionados = {} 

    lista_ajustes = ft.Column(spacing=10)
    
    # Campo de búsqueda para filtrar la lista (opcional pero recomendado)
    def filtrar_ejercicios(e):
        termino = e.control.value.lower()
        for control in lista_seleccion.controls:
            # El control es el Container, su content es el ListTile
            nombre_ej = control.content.title.value.lower()
            control.visible = termino in nombre_ej
        lista_seleccion.update()

    def al_pulsar_ejercicio(e, ej):
        id_ej = ej['id_ejercicio']
        if id_ej in seleccionados:
            del seleccionados[id_ej]
            e.control.bgcolor = None
        else:
            seleccionados[id_ej] = {
                'id': id_ej, 'nombre': ej['nombre'],
                'series': 4, 'reps': 10, 'descanso': 60
            }
            e.control.bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.BLUE)
        
        e.control.update()
        dibujar_ajustes()

    def dibujar_ajustes():
        lista_ajustes.controls.clear()
        for id_ej, d in seleccionados.items():
            lista_ajustes.controls.append(
                ft.Container(
                    padding=10, bgcolor="#2A2A2A", border_radius=10,
                    content=ft.Column([
                        ft.Text(d['nombre'], weight="bold", color="white"),
                        ft.Row([
                            ft.TextField(label="Series", value="4", width=70, text_size=12,
                                       on_change=lambda e, i=id_ej: seleccionados[i].update({'series': e.control.value})),
                            ft.TextField(label="Reps", value="10", width=70, text_size=12,
                                       on_change=lambda e, i=id_ej: seleccionados[i].update({'reps': e.control.value})),
                            ft.TextField(label="Descanso", value="60", width=80, text_size=12,
                                       on_change=lambda e, i=id_ej: seleccionados[i].update({'descanso': e.control.value})),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ])
                )
            )
        page.update()

    def guardar_rutina(e):
        if vm.guardar_rutina_completa(id_usuario, txt_nombre.value, drp_nivel.value, list(seleccionados.values())):
            volver_callback()

    # UI principal
    txt_nombre = ft.TextField(label="Nombre de rutina", border_color="blue")
    drp_nivel = ft.Dropdown(label="Nivel", value="Intermedio", options=[
        ft.dropdown.Option("Principiante"), ft.dropdown.Option("Intermedio"), ft.dropdown.Option("Avanzado")
    ])
    busqueda = ft.TextField(label="Buscar ejercicio...", prefix_icon=ft.Icons.SEARCH, on_change=filtrar_ejercicios)
    
    lista_seleccion = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=250)
    for ej in ejercicios_db:
        lista_seleccion.controls.append(
            ft.Container(
                content=ft.ListTile(
                    title=ft.Text(ej['nombre'], size=14),
                    subtitle=ft.Text(f"{ej['nombre_grupo']} - {ej['dificultad']}", size=12)
                ),
                on_click=lambda e, item=ej: al_pulsar_ejercicio(e, item),
                border_radius=10
            )
        )

    return ft.Column([
        ft.Row([
            ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: volver_callback()),
            ft.Text("NUEVA RUTINA", size=20, weight="bold")
        ]),
        txt_nombre,
        drp_nivel,
        ft.Divider(),
        busqueda,
        lista_seleccion,
        ft.Text("Configuración de ejercicios:", weight="bold"),
        lista_ajustes,
        ft.ElevatedButton("GUARDAR RUTINA", icon=ft.Icons.SAVE, on_click=guardar_rutina, width=400)
    ], scroll=ft.ScrollMode.AUTO)