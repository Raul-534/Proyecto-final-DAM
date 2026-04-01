import flet as ft
from viewmodels.rutinas_viewmodel import RutinasViewModel

def MisRutinasView(page: ft.Page, id_usuario, nombre_usuario, volver_callback, editar_rutina_callback):
    vm = RutinasViewModel()
    lista_rutinas = ft.Column(spacing=10, scroll=ft.ScrollMode.ALWAYS, expand=True)

    def cargar_rutinas():
        lista_rutinas.controls.clear()
        rutinas = vm.listar_mis_rutinas(id_usuario)
        
        if not rutinas:
            lista_rutinas.controls.append(
                ft.Container(
                    content=ft.Text("Aún no tienes rutinas. ¡Crea la primera!", color="grey", italic=True),
                    padding=20, alignment=ft.alignment.center
                )
            )
        else:
            for r in rutinas:
                lista_rutinas.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text(r['nombre'], weight="bold", size=16),
                                ft.Text(f"Nivel: {r['nivel']}", size=12, color="blue"),
                            ], expand=True),
                            # Botón Editar
                            ft.IconButton(
                                icon=ft.Icons.EDIT_NOTE_ROUNDED,
                                icon_color="white",
                                tooltip="Editar rutina",
                                on_click=lambda _, id_r=r['id_rutina'], nom_r=r['nombre']: editar_rutina_callback(id_r, nom_r)
                            ),
                            # Botón Borrar
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                icon_color="red",
                                tooltip="Eliminar",
                                on_click=lambda _, id_r=r['id_rutina']: confirmar_borrado(id_r)
                            ),
                        ]),
                        padding=15,
                        bgcolor="#1E1E1E",
                        border_radius=12,
                        border=ft.border.all(1, "#333333")
                    )
                )
        page.update()

    def confirmar_borrado(id_rutina):
        def borrar_si(e):
            if vm.eliminar_rutina(id_rutina):
                dlg.open = False
                cargar_rutinas()
                page.update()
        
        dlg = ft.AlertDialog(
            title=ft.Text("¿Borrar rutina?"),
            content=ft.Text("Se eliminarán todos los ejercicios asociados."),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: setattr(dlg, "open", False) or page.update()),
                ft.TextButton("Sí, eliminar", on_click=borrar_si, icon=ft.Icons.DELETE, icon_color="red"),
            ]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # Carga inicial de datos
    cargar_rutinas()

    return ft.Column([
        ft.Row([
            ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: volver_callback()),
            ft.Text("MIS RUTINAS", size=22, weight="bold")
        ]),
        ft.Divider(height=10, color="transparent"),
        lista_rutinas
    ], expand=True)