import requests

BASE = "http://127.0.0.1:8000/productos"
TIME_OUT = 10

#Obtiene la lista de productos de FastAPI
def listar_productos(limit: int = 20, offset: int = 0) -> dict:
    try:
        #requests.get se conecta a la API y entrega la información en r
        r = requests.get(f"{BASE}/", params={"limit": limit, "offset": offset}, timeout=TIME_OUT)
        #si el estatus_code es cualquier código 200 se entrega el resultado en formato json
        if 200 <= r.status_code < 300:
            return r.json() if r.content else {}
        raise ValueError(f"Error {r.status_code}", r.status_code, r.text)
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error de conexión", None, str(e))

#Obtiene el producto con el id que se le pasa como parametro
def get_product(product_id: str) -> dict:
    try:
        r = requests.get(f"{BASE}/{product_id}", timeout=TIME_OUT)
        if 200 <= r.status_code < 300:
            return r.json() if r.content else {}
        raise ValueError(f"Error {r.status_code}", r.status_code, r.text)
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error de conexión", None, str(e))

#Crea un producto nuevo con los datos que se le pasan como parametro en un diccionario
def create_product(data:dict) -> dict:
    try:
        r = requests.post(f"{BASE}/", json=data, timeout=TIME_OUT)
        if 200 <= r.status_code < 300:
            return r.json() if r.content else {}
        raise ValueError(f"Error {r.status_code}", r.status_code, r.text)
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error de conexión", None, str(e))

#Actualiza el producto que se le indica con el ID y los datos nuevos en un diccionario
def update_product(product_id:str, data:dict) -> dict:
    try:
        r = requests.put(f"{BASE}/{product_id}", json=data, timeout=TIME_OUT)
        if r.status_code >= 400:
            try:
                playload = r.json()
                detail = playload.get("error") or playload.get("detail") or r.text
            except Exception:
                detail = r.text
            raise ApiError(detail, r.status_code)

        return r.json()
    except requests.Timeout:
        raise ApiError("El servidor tardo demasiado en responder", 0)
    except requests.ConnectionError:
        raise ApiError("No se pudo conectar al servidor", 0)
    except requests.RequestException as e:
        raise ApiError(f"Error de red {str(e)}",0)

#Borrar el producto que se le indica con el ID
def delete_product(product_id:str):
    try:
        r = requests.delete(f"{BASE}/{product_id}", timeout=TIME_OUT)
        if 200 <= r.status_code < 300:
            return r.json() if r.content else {}
        raise ValueError(f"Error {r.status_code}", r.status_code, r.text)
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error de conexión", None, str(e))

#print(listar_productos())