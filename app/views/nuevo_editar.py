import flet as ft
from app.components.popup import show_popup

def formulario_nuevo_editar_producto(page: ft.Page, on_submit, initial: dict | None = None):
    initial = initial or {}
    es_edicion = True if initial.get("id") else False
    
    # Campos de texto
    name = ft.TextField(label="Nombre", value=initial.get("name", ""))
    quantity = ft.TextField(label="Cantidad", value=str(initial.get("quantity", 0)))
    ingreso_date = ft.TextField(label="Ingreso (YYYY-MM-DD)", value=initial.get("ingreso_date", ""))
    min_stock = ft.TextField(label="Stock mínimo", value=str(initial.get("min_stock", 0)))
    max_stock = ft.TextField(label="Stock máximo", value=str(initial.get("max_stock", 0)))

    def close_dialog(e=None):
        dlg.open = False
        page.update()

    async def save(e):
        if not name.value.strip():
            await show_popup(page, "Validación", "El nombre es obligatorio.")
            return
        try:
            ingreso_str = ingreso_date.value.strip()
            data = {
                "name": name.value.strip(),
                "quantity": int(quantity.value),
                "ingreso_date": ingreso_str if ingreso_str else None,
                "min_stock": int(min_stock.value),
                "max_stock": int(max_stock.value),
            }
            if es_edicion:
                data["id"] = initial["id"]
            
            await on_submit(data) # Llama a la lógica de la base de datos
            close_dialog()
        except ValueError:
            await show_popup(page, "Error", "Datos numéricos inválidos.")

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Editar producto" if es_edicion else "Nuevo producto"),
        content=ft.Column([name, quantity, ingreso_date, min_stock, max_stock], tight=True),
        actions=[
            ft.TextButton("Cancelar", on_click=close_dialog),
            ft.FilledButton("Guardar", on_click=save)
        ],
    )

    def open_form():
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    return dlg, open_form, close_dialog