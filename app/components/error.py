import flet as ft

async def show_snackbar(page: ft.Page, title: str, message: str, bgcolor=ft.Colors.BLUE):
    page.snack_bar = ft.SnackBar(
        content=ft.Text(f"{title}: {message}"),
        bgcolor=bgcolor
    )
    page.snack_bar.open = True
    page.update()

async def show_popup(page: ft.Page, title: str, message: str):
    def close_dlg(e):
        dlg.open = False
        page.update()
    
    dlg = ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Text(message),
        actions=[ft.TextButton("OK", on_click=close_dlg)]
    )

    page.dialog = dlg
    dlg.open = True
    page.update()

def close_popup(page: ft.Page):
    if page.dialog:
        page.dialog.open = False
        page.update()