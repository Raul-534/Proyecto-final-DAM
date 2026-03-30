import flet as ft

def ResultadoView(page: ft.Page, nombre_usuario, kcal, al_volver):
    proteinas = (kcal * 0.30) / 4
    carbohidratos = (kcal * 0.40) / 4
    grasas = (kcal * 0.30) / 9

    def card_macro(label, value, unit, color, icon):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, color=color, size=30),
                ft.Text(label, size=12, color=ft.Icons.GREY_400),
                ft.Text(f"{value:.0f}{unit}", size=20, weight="bold", color=color),
            ], horizontal_alignment="center", spacing=5),
            bgcolor="#1E1E1E",
            padding=15,
            border_radius=15,
            expand=True,
            border=ft.border.all(1, "#333333")
        )

    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, on_click=lambda _: al_volver(nombre_usuario)),
                ft.Text("TU RESULTADO", size=22, weight="bold"),
            ]),
            ft.Container(
                content=ft.Column([
                    ft.Text("CALORÍAS DIARIAS", size=12, weight="bold", color="white70"),
                    ft.Text(f"{kcal:.0f}", size=55, weight="bold", color="white"),
                    ft.Text("KILOCALORÍAS", size=14, color="white70"),
                ], horizontal_alignment="center", spacing=0),
                padding=30,
                width=400,
                border_radius=25,
                gradient=ft.LinearGradient(["#007BFF", "#0056b3"]),
            ),
            ft.Divider(height=10, color="transparent"),
            ft.Row([
                card_macro("Prot", proteinas, "g", "red", ft.Icons.RESTAURANT),
                card_macro("Carbs", carbohidratos, "g", "orange", ft.Icons.GRAIN),
            ], spacing=10),
            ft.Row([
                card_macro("Grasas", grasas, "g", "yellow", ft.Icons.WATER_DROP),
                card_macro("Agua", (kcal/1000)*1.2, "L", "cyan", ft.Icons.OPACITY),
            ], spacing=10),
            ft.Divider(height=20, color="transparent"),
            ft.FilledButton(
                "GUARDAR Y FINALIZAR",
                icon=ft.Icons.CHECK_CIRCLE_ROUNDED,
                width=400,
                height=55,
                on_click=lambda _: al_volver(nombre_usuario)
            ),
        ], horizontal_alignment="center", scroll=ft.ScrollMode.AUTO),
        padding=20
    )