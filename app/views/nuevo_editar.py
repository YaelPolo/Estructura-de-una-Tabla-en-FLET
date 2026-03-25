import flet as ft

def formulario_nuevo_editar_producto(page: ft.Page, on_submit, initial: dict | None = None):
    initial = initial or {}
    es_edicion = True if initial.get("id") else False
    
    titulo = ft.Text("Editar producto" if es_edicion else "Nuevo producto")
    name = ft.TextField(label="Nombre", value=initial.get("name", ""))
    quantity = ft.TextField(label="Cantidad", value=str(initial.get("quantity", 0)))
    ingreso_date = ft.TextField(label="Ingreso (YYYY-MM-DD)", value=initial.get("ingreso_date", ""))
    min_stock = ft.TextField(label="Stock mínimo", value=str(initial.get("min_stock", 0)))
    max_stock = ft.TextField(label="Stock máximo", value=str(initial.get("max_stock", 0)))

    def close():
        dlg.open = False
        page.update()

    async def save(_e):
        # ... (tu lógica de validación se mantiene igual)
        data = {
            "name": name.value.strip(),
            "quantity": int(quantity.value),
            "ingreso_date": ingreso_date.value.strip(),
            "min_stock": int(min_stock.value),
            "max_stock": int(max_stock.value)
        }
        if es_edicion: data["id"] = initial["id"] # Mantener el ID si es edición
        
        await on_submit(data)
        close()

    btn_cancelar = ft.TextButton("Cancelar", on_click=lambda e: close())
    btn_guardar = ft.Button("Guardar", on_click=lambda e: page.run_task(save, e))

    dlg = ft.AlertDialog(
        title=titulo,
        content=ft.Container(
            width=400,
            content=ft.Column([name, quantity, ingreso_date, min_stock, max_stock], tight=True)
        ),
        actions=[btn_cancelar, btn_guardar],
    )

    def open_():
        page.dialog = dlg
        dlg.open = True
        page.update()

    return dlg, open_, close