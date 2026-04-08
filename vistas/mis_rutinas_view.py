import flet as ft
from viewmodels.rutinas_viewmodel import RutinasViewModel

def MisRutinasView(page: ft.Page, id_usuario, nombre_usuario, volver_callback, editar_rutina_callback):
    vm = RutinasViewModel()
    
    lista_rutinas = ft.ListView(
        spacing=10,
        expand=True,
        auto_scroll=False
    )

    def cargar_rutinas():
        lista_rutinas.controls.clear()
        rutinas = vm.listar_mis_rutinas(id_usuario)
        
        if not rutinas:
            lista_rutinas.controls.append(
                ft.Container(
                    content=ft.Text("Aún no tienes rutinas. ¡Crea la primera!", color="grey", italic=True),
                    padding=20, 
                    alignment=ft.Alignment.CENTER
                )
            )
        else:
            for r in rutinas:
                nivel_txt = r.get('nivel') or r.get('dificultad') or "Intermedio"
                id_r = r.get('id_rutina') or r.get('id')
                nombre_r = r['nombre']
                
                lista_rutinas.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text(nombre_r, weight="bold", size=16),
                                ft.Text(f"Nivel: {nivel_txt}", size=12, color="blue"),
                            ], expand=True),
                            
                            ft.IconButton(
                                icon=ft.Icons.EDIT_NOTE_ROUNDED,
                                on_click=lambda _, ir=id_r, nr=nombre_r: editar_rutina_callback(ir, nr)
                            ),
                            
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                icon_color="red",
                                on_click=lambda e, r_id=id_r: confirmar_borrado(r_id)
                            ),
                        ]),
                        padding=15, bgcolor="#1E1E1E", border_radius=12,
                        border=ft.Border.all(1, "#333333")
                    )
                )
        page.update()

    def confirmar_borrado(id_rutina):
        def cerrar_dialogo(e):
            dlg.open = False
            page.update()

        def borrar_si(e):
            if vm.eliminar_rutina(id_rutina):
                dlg.open = False
                page.snack_bar = ft.SnackBar(ft.Text("Rutina eliminada ✅"), bgcolor="green")
                page.snack_bar.open = True
                cargar_rutinas()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Error al borrar ❌"), bgcolor="red")
                page.snack_bar.open = True
            page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("¿Borrar rutina?"),
            content=ft.Text("Esta acción eliminará la rutina y sus ejercicios."),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),
                ft.TextButton("Eliminar", on_click=borrar_si, icon=ft.Icons.DELETE, icon_color="red"),
            ]
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    cargar_rutinas()

    return ft.Container(
        padding=15,
        expand=True, 
        content=ft.Column([
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: volver_callback(id_usuario, nombre_usuario)),
                ft.Text("MIS RUTINAS", size=22, weight="bold")
            ]),
            
            ft.Divider(height=10, color="transparent"),
            
            ft.Container(
                content=lista_rutinas,
                expand=True,
                height=300
            ),
            
        ], spacing=10, expand=True)
    )