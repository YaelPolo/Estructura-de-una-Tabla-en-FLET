from app.views.nuevo_editar import formulario_nuevo_editar_producto
import flet as ft
from typing import Any
from app.services.transacciones_api_productos import create_product, ApiError
from app.views.nuevo_editar import formulario_nuevo_editar_producto
from app.components.error import show_snackbar, show_popup, api_error_to_text
from app.views.mostrar_productos import actualizar_data

rows_data:list[dict[str,Any]]=[] #Paso 3. 
def products_view(page:ft.Page) -> ft.Control:
    ########### Nuevo producto ###########
    #Esta función se ejecuta al hacer click en "Nuevo producto"
    #lo que hace en primer lugar es abrir la ventana para captura de datos
    def inicio_nuevo_producto(_e):
        #Se crea la función para transferir al formulario de nuevo producto
        async def crear_nuevo_producto(data:dict):#Esta función se lleva a la ventana para capturar
            try:
                #Se conecta a transacciones_api_productos.py para crear en la BD un nuevo producto
                await create_product(data)
                await show_snackbar(page, "Éxito", "Producto creado.", bgcolor=ft.Colors.SUCCESS)
                await actualizar_data()
            except ApiError as ex:
                await show_popup(page, "Error", api_error_to_text(ex))
            except Exception as ex:
                await show_snackbar(page, "Error", str(ex), bgcolor=ft.Colors.DANGER)

        #Se llama a la función para abrir la ventana y poder capturar los datos,
        # regresa 3 funciones(dlg,open_ y close), se ejecuta open_()
        dlg, open_, close = formulario_nuevo_editar_producto(page, on_submit=crear_nuevo_producto, initial=None)
        open_() #Abre la ventana
    ########### FIN nuevo producto ###########
    btn_nuevo = ft.Button("Nuevo producto",icon=ft.Icons.ADD,on_click=inicio_nuevo_producto)

