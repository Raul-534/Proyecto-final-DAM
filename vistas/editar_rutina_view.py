import flet as ft
from viewmodels.rutinas_viewmodel import RutinasViewModel

def EditarRutinaView(page: ft.Page, id_usuario, nombre_usuario, id_rutina, volver_callback):
    vm = RutinasViewModel()
    ejercicios_db = vm.obtener_ejercicios()
    detalles_actuales = vm.obtener_detalles_rutina(id_rutina)
    
    # Pre-cargar seleccionados
    seleccionados = {}
    for d in detalles_actuales:
        seleccionados[d['id_ejercicio']] = {
            'id': d['id_ejercicio'], 'nombre': d['nombre'],
            'series': d['series'], 'reps': d['repeticiones'], 'descanso': d['descanso']
        }

    lista_ajustes = ft.Column(spacing=10)
    
    def dibujar_ajustes():
        lista_ajustes.controls.clear()
        for id_ej, d in seleccionados.items():
            lista_ajustes.controls.append(
                ft.Container(
                    padding=10, bgcolor="#2A2A2A", border_radius=10,
                    content=ft.Column([
                        ft.Text(d['nombre'], weight="bold"),
                        ft.Row([
                            ft.TextField(label="Ser", value=str(d['series']), width=60, 
                                       on_change=lambda e, i=id_ej: seleccionados[i].update({'series': e.control.value})),
                            ft.TextField(label="Rep", value=str(d['reps']), width=60,
                                       on_change=lambda e, i=id_ej: seleccionados[i].update({'reps': e.control.value})),
                            ft.TextField(label="Desc", value=str(d['descanso']), width=70,
                                       on_change=lambda e, i=id_ej: seleccionados[i].update({'descanso': e.control.value})),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ])
                )
            )
        page.update()

    def al_clic_ejercicio(e, ej):
        id_ej = ej['id_ejercicio']
        if id_ej in seleccionados:
            del seleccionados[id_ej]
            e.control.bgcolor = None
        else:
            seleccionados[id_ej] = {'id': id_ej, 'nombre': ej['nombre'], 'series': 4, 'reps': 10, 'descanso': 60}
            e.control.bgcolor = ft.Colors.with_opacity(0.2, ft.Colors.BLUE)
        e.control.update()
        dibujar_ajustes()

    # --- UI ---
    txt_nombre = ft.TextField(label="Nombre", value="", border_color="blue") # Rellenar después
    drp_nivel = ft.Dropdown(label="Nivel", value="Intermedio", options=[
        ft.dropdown.Option("Principiante"), ft.dropdown.Option("Intermedio"), ft.dropdown.Option("Avanzado")
    ])

    lista_seleccion = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=200)
    for ej in ejercicios_db:
        # Si el ejercicio ya estaba en la rutina, lo pintamos de azul
        es_activo = ej['id_ejercicio'] in seleccionados
        lista_seleccion.controls.append(
            ft.Container(
                content=ft.ListTile(title=ft.Text(ej['nombre'], size=14)),
                on_click=lambda e, item=ej: al_clic_ejercicio(e, item),
                bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLUE) if es_activo else None,
                border_radius=10
            )
        )

    def guardar_cambios(e):
        if vm.actualizar_rutina_completa(id_rutina, txt_nombre.value, drp_nivel.value, list(seleccionados.values())):
            volver_callback()

    # Inicializar panel de ajustes
    dibujar_ajustes()

    return ft.Column([
        ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: volver_callback()), ft.Text("EDITAR RUTINA", size=20, weight="bold")]),
        txt_nombre,
        drp_nivel,
        ft.Text("Selecciona/Desmarca ejercicios:"),
        lista_seleccion,
        ft.Divider(),
        lista_ajustes,
        ft.ElevatedButton("ACTUALIZAR RUTINA", icon=ft.Icons.UPDATE, on_click=guardar_cambios, width=400)
    ], scroll=ft.ScrollMode.AUTO)