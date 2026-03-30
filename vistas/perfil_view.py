import flet as ft
from viewmodels.perfil_viewmodel import PerfilViewModel

def PerfilView(page: ft.Page, nombre_usuario, al_calcular, al_volver):
    # Instanciamos el ViewModel (Si es Singleton, devolverá la instancia única)
    vm = PerfilViewModel()
    
    # 1. Recuperar datos de la BD al cargar la vista
    datos_bd = vm.obtener_datos_perfil(nombre_usuario)

    # Campos de texto con valores por defecto si existen en la BD
    edad_i = ft.TextField(
        label="Edad", width=110, border_radius=10, 
        value=str(datos_bd['edad']) if datos_bd else "",
        keyboard_type=ft.KeyboardType.NUMBER
    )
    peso_i = ft.TextField(
        label="Peso (kg)", width=110, border_radius=10, 
        value=str(datos_bd['peso']) if datos_bd else "",
        keyboard_type=ft.KeyboardType.NUMBER
    )
    altura_i = ft.TextField(
        label="Altura (cm)", width=110, border_radius=10, 
        value=str(datos_bd['altura']) if datos_bd else "",
        keyboard_type=ft.KeyboardType.NUMBER, hint_text="Ej: 175"
    )

    genero_radio = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="hombre", label="Hombre"),
            ft.Radio(value="mujer", label="Mujer"),
        ], alignment="center"),
        value=datos_bd['genero'] if datos_bd else "hombre"
    )

    act_dropdown = ft.Dropdown(
        label="Nivel de Actividad",
        width=350,
        border_radius=10,
        value=str(datos_bd['actividad']) if datos_bd else "1.55",
        options=[
            ft.dropdown.Option(key="1.2", text="Sedentario (Poco ejercicio)"),
            ft.dropdown.Option(key="1.55", text="Moderado (3-5 días/sem)"),
            ft.dropdown.Option(key="1.9", text="Atleta (6-7 días/sem)"),
        ]
    )

    def btn_click(e):
        try:
            # Validaciones básicas
            alt_val = float(altura_i.value.replace(",", "."))
            p_val = float(peso_i.value.replace(",", "."))
            ed_val = int(edad_i.value)
            gen = genero_radio.value
            factor = float(act_dropdown.value)

            # Fórmula Harris-Benedict
            if gen == "hombre":
                tmb = 88.36 + (13.4 * p_val) + (4.8 * alt_val) - (5.7 * ed_val)
            else:
                tmb = 447.59 + (9.2 * p_val) + (3.1 * alt_val) - (4.3 * ed_val)
            
            kcal = tmb * factor

            # 2. GUARDAR EN BD antes de navegar
            datos_a_guardar = {
                "peso": p_val,
                "altura": alt_val,
                "edad": ed_val,
                "genero": gen,
                "objetivo": "Mantener", # Puedes hacerlo dinámico luego
                "actividad": factor
            }
            
            if vm.guardar_o_actualizar_perfil(nombre_usuario, datos_a_guardar):
                al_calcular(nombre_usuario, kcal)
            else:
                raise Exception("Error al conectar con la base de datos")

        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    # --- DISEÑO CENTRADO ---
    return ft.Container(
        content=ft.Column([
            # Cabecera (Siempre arriba)
            ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, 
                    on_click=lambda _: al_volver(nombre_usuario)
                ),
                ft.Text("CONFIGURACIÓN DE PERFIL", size=20, weight="bold"),
            ], alignment="start"),
            
            # Espaciador para empujar el contenido al centro
            ft.Column([
                ft.Text("Género", weight="bold", color="blue"),
                genero_radio,
                ft.Divider(height=10, color="transparent"),
                ft.Row([edad_i, peso_i, altura_i], alignment="center", spacing=10),
                ft.Divider(height=10, color="transparent"),
                ft.Text("Actividad Física", weight="bold", color="blue"),
                act_dropdown,
                ft.Divider(height=30, color="transparent"),
                ft.FilledButton(
                    "CALCULAR PLAN Y GUARDAR",
                    icon=ft.Icons.SAVE_AS_ROUNDED,
                    width=350,
                    height=55,
                    on_click=btn_click,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15))
                ),
            ], 
            alignment=ft.MainAxisAlignment.CENTER, # Centrado vertical
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centrado horizontal
            expand=True # Ocupa todo el espacio disponible entre cabecera y final
            )
        ]),
        padding=20,
        expand=True
    )