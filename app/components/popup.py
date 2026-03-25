import flet as ft
import asyncio
from app.styles.estilos import Colors, Buttons

# Función para diálogos informativos simples
async def show_popup(page: ft.Page, title: str, message: str, bgcolor: str = Colors.DANGER, txtcolor: str = Colors.WHITE):
    def close_dlg(e):
        dlg.open = False
        page.update()

    dlg = ft.AlertDialog(
        title_padding=0,
        content_padding=0,
        title=ft.Container(
            bgcolor=bgcolor,
            padding=12,
            border_radius=ft.BorderRadius(18, 18, 0, 0),
            content=ft.Text(title, color=txtcolor, weight=ft.FontWeight.BOLD)
        ),
        content=ft.Container(padding=20, content=ft.Text(message)),
        actions=[ft.TextButton("OK", on_click=close_dlg)]
    )
    page.overlay.append(dlg) # Recomendado en versiones recientes de Flet
    dlg.open = True
    page.update()

# Función para mensajes rápidos en la parte inferior
async def show_snackbar(page: ft.Page, message: str, bgcolor: str = Colors.DANGER, txtcolor: str = Colors.WHITE):
    page.snack_bar = ft.SnackBar(
        content=ft.Text(message, color=txtcolor),
        bgcolor=bgcolor,
    )
    page.snack_bar.open = True
    page.update()