import flet as ft
from viewmodels.dietas_viewmodel import DietasViewModel
from viewmodels.perfil_viewmodel import PerfilViewModel
from modelos.Dieta import Dieta

def DietasView(page, nombre_usuario, email_usuario, volver_callback, navegar_perfil_callback, vm_dietas=None):
    if vm_dietas is None:
        vm_dietas = DietasViewModel()
    
    vm_perfil = PerfilViewModel()
    datos_perfil = [None]

    # --- UI MACROS ---
    txt_calorias = ft.Text("0", size=40, weight="bold", color="blue")
    txt_prot = ft.Text("0/0g", size=12, color="grey")
    txt_carb = ft.Text("0/0g", size=12, color="grey")
    txt_gras = ft.Text("0/0g", size=12, color="grey")
    msg_status = ft.Text("", size=14, weight="bold", visible=False)
    
    btn_ir_perfil = ft.TextButton(
        "Configurar mi Perfil ahora",
        icon=ft.Icons.SETTINGS,
        on_click=lambda _: navegar_perfil_callback(),
        visible=False
    )
    
    nombre_dieta_f = ft.TextField(label="Nombre de la dieta", width=300, border_radius=10)
    lista_dietas_container = ft.Column(scroll="auto", spacing=10, width=330)

    # --- LÓGICA DE CÁLCULO ---
    def calcular_y_mostrar(objetivo, actividad_manual=None):
        if not datos_perfil[0]: return
        p = datos_perfil[0]
        
        tmb = (10 * float(p['peso'])) + (6.25 * float(p['altura'])) - (5 * int(p['edad'])) + (5 if p['genero'] == "hombre" else -161)
        factor_actividad = float(actividad_manual) if actividad_manual else float(p['actividad'])
        tdee = tmb * factor_actividad

        if "Bajar" in objetivo: cals = tdee - 500
        elif "Subir" in objetivo: cals = tdee + 500
        else: cals = tdee

        prot_g = float(p['peso']) * 2.2
        gras_g = float(p['peso']) * 1.0
        carb_g = max(0, (cals - (prot_g * 4) - (gras_g * 9)) / 4)
        
        txt_calorias.value = f"{int(cals)}"
        txt_prot.value = f"0/{int(prot_g)}g"
        txt_carb.value = f"0/{int(carb_g)}g"
        txt_gras.value = f"0/{int(gras_g)}g"
        
        try: page.update()
        except: pass

    def cambio_parametros(e):
        calcular_y_mostrar(dd_objetivo.value, dd_actividad.value)

    def seleccionar_dieta(dieta_obj):
        nombre_dieta_f.value = dieta_obj.nombre
        dd_objetivo.value = dieta_obj.objetivo
        txt_calorias.value = str(dieta_obj.kcal)
        txt_prot.value = f"0/{dieta_obj.proteina}g"
        txt_carb.value = f"0/{dieta_obj.carbos}g"
        txt_gras.value = f"0/{dieta_obj.grasas}g"
        msg_status.value = f"Cargada: {dieta_obj.nombre}"
        msg_status.visible = True
        page.update()

    def borrar_dieta_click(dieta_id):
        if vm_dietas.eliminar_dieta(dieta_id):
            msg_status.value = "🗑️ Dieta eliminada"
            msg_status.color = "red"
            msg_status.visible = True
            recargar_lista()
            page.update()

    def recargar_lista():
        dietas_rows = vm_dietas.listar_dietas(email_usuario)
        lista_dietas_container.controls.clear()
        
        if not dietas_rows:
            lista_dietas_container.controls.append(ft.Text("No hay dietas guardadas.", color="grey"))
        else:
            for row in dietas_rows:
                d = Dieta.from_db(row)
                lista_dietas_container.controls.append(
                    ft.Container(
                        content=ft.Row([
                            # Icono y textos (Click para seleccionar)
                            ft.GestureDetector(
                                mouse_cursor=ft.MouseCursor.CLICK,
                                on_tap=lambda _, obj=d: seleccionar_dieta(obj),
                                content=ft.Row([
                                    ft.Icon(ft.Icons.RESTAURANT_MENU, color="blue"),
                                    ft.Column([
                                        ft.Text(d.nombre, weight="bold", size=14),
                                        ft.Text(f"{d.kcal} kcal - {d.objetivo}", size=11, color="grey"),
                                    ], spacing=0, width=180), # Ancho fijo para no empujar el botón
                                ], tight=True)
                            ),
                            # Botón de borrar (A la derecha)
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_color="red",
                                icon_size=20,
                                tooltip="Eliminar dieta",
                                on_click=lambda _, id_dieta=d.id: borrar_dieta_click(id_dieta)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=10, 
                        bgcolor="#1A1A1A", 
                        border_radius=10,
                    )
                )
        try:
            lista_dietas_container.update()
        except:
            pass

    # Dropdowns
    dd_objetivo = ft.Dropdown(
        label="Objetivo", width=300, border_radius=10, value="Mantener Peso",
        options=[ft.dropdown.Option("Bajar Peso (Definición)"), ft.dropdown.Option("Mantener Peso"), ft.dropdown.Option("Subir Peso (Volumen)")],
        on_select=cambio_parametros
    )

    dd_actividad = ft.Dropdown(
        label="Estilo de vida / Actividad", width=300, border_radius=10,
        options=[ft.dropdown.Option(key="1.2", text="Sedentario"), ft.dropdown.Option(key="1.55", text="Moderado"), ft.dropdown.Option(key="1.9", text="Atleta")],
        on_select=cambio_parametros
    )

    def eliminar_dieta(self, dieta_id):
        try:
            cursor = self.db.cursor()
            sql = "DELETE FROM dietas WHERE id = %s"
            cursor.execute(sql, (dieta_id,))
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar dieta: {e}")
            return False

    def guardar_dieta_click(e):
        if not nombre_dieta_f.value:
            msg_status.value = "❌ Nombre obligatorio"; msg_status.visible = True; page.update(); return
        
        vm_dietas.guardar_nueva_dieta(
            email_usuario, nombre_dieta_f.value, dd_objetivo.value, 
            int(txt_calorias.value), 
            int(txt_prot.value.split('/')[-1].replace('g', '')),
            int(txt_carb.value.split('/')[-1].replace('g', '')),
            int(txt_gras.value.split('/')[-1].replace('g', ''))
        )
        msg_status.value = "✅ Dieta guardada"; nombre_dieta_f.value = ""; recargar_lista(); page.update()

    layout = ft.Column([
        ft.Row([ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: volver_callback()), ft.Text("NUTRICIÓN Y MACROS", size=22, weight="bold")]),
        nombre_dieta_f, dd_objetivo, dd_actividad,
        ft.Container(content=ft.Column([ft.Text("CALORÍAS DIARIAS ESTIMADAS", color="grey", size=12), txt_calorias, ft.ProgressBar(value=0.4, color="blue", width=250)], horizontal_alignment="center"), padding=20, bgcolor="#1A1A1A", border_radius=20, alignment=ft.Alignment.CENTER),
        ft.Row([ft.Column([ft.Text("PROT", size=11), txt_prot], horizontal_alignment="center"), ft.Column([ft.Text("CARB", size=11), txt_carb], horizontal_alignment="center"), ft.Column([ft.Text("GRAS", size=11), txt_gras], horizontal_alignment="center")], alignment=ft.MainAxisAlignment.SPACE_AROUND),
        msg_status, btn_ir_perfil,
        ft.FilledButton("GUARDAR CONFIGURACIÓN", icon=ft.Icons.SAVE, width=300, on_click=guardar_dieta_click),
        ft.Text("MIS DIETAS GUARDADAS", size=16, weight="bold", color="blue"),
        lista_dietas_container,
    ], scroll="auto", spacing=15, horizontal_alignment="center")

    # --- CARGA INICIAL ---
    try:
        res = vm_perfil.obtener_datos(nombre_usuario) 
        if res:
            datos_perfil[0] = res
            dd_actividad.value = str(res['actividad'])
            calcular_y_mostrar(dd_objetivo.value)
        else:
            txt_calorias.value = "---"; msg_status.value = "⚠️ Perfil no configurado"; msg_status.visible = True; btn_ir_perfil.visible = True
    except: pass

    recargar_lista() # Ahora no romperá gracias al try/except interno
    return layout