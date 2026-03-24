import flet as ft
from typing import Any
# Paso 1. Imports de la práctica
from app.views.nuevo_editar import formulario_nuevo_editar_producto 
from app.services.transacciones_api_productos import create_product, ApiError
from app.components.error import show_snackbar, show_popup, api_error_to_text
from app.views.mostrar_productos import actualizar_data

# Paso 3. Estructura de datos
rows_data: list[dict[str, Any]] = []

def products_view(page: ft.Page) -> ft.Control:
    
    # --- Lógica para Nuevo Producto ---
    async def inicio_nuevo_producto(_e):
        async def crear_nuevo_producto(data: dict):
            try:
                # Se conecta a la API para guardar
                await create_product(data)
                # ft.Colors corrige el error amarillo de la captura
                await show_snackbar(page, "Éxito", "Producto guardado.", bgcolor=ft.Colors.SUCCESS)
                # Refresca la lista de la pantalla
                await actualizar_data()
            except ApiError as ex:
                await show_popup(page, "Error", api_error_to_text(ex))
            except Exception as ex:
                await show_snackbar(page, "Error", str(ex), bgcolor=ft.Colors.DANGER)

        # Se abre el formulario (initial=None indica que es nuevo)
        dlg, open_, close = formulario_nuevo_editar_producto(page, on_submit=crear_nuevo_producto, initial=None)
        open_()

    # Botón definido para el Paso 4
    btn_nuevo = ft.ElevatedButton(
        "Nuevo producto", 
        icon=ft.Icons.ADD, 
        on_click=inicio_nuevo_producto
    )

    # Paso 4. Construcción de la interfaz (Aprox línea 190)
    # Aquí es donde se visualiza la lista de la imagen
    total_text = ft.Text(f"Total de productos: {len(rows_data)}")
    
    # Contenedor de la tabla (ajusta 'tabla' según tu código de visualización)
    return ft.Column(
        expand=True,
        controls=[
            btn_nuevo,
            total_text,
            ft.Container(content=ft.Text("Aquí se renderiza tu tabla de productos"))
        ]
    )