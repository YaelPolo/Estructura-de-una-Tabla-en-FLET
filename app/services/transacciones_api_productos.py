import requests

BASE = "http://127.0.0.1:8000/productos"
TIME_OUT = 10

def listar_productos(limit: int = 20, offset: int = 0) -> dict:
    r = requests.get(f"{BASE}/", params={"limit": limit, "offset": offset}, timeout=TIME_OUT)
    return r.json()

def create_product(data: dict) -> dict:
    r = requests.post(f"{BASE}/", json=data, timeout=TIME_OUT)
    print("POST:", r.status_code, r.text)
    return r.json()

def update_product(product_id: str, data: dict) -> dict:
    r = requests.put(f"{BASE}/{product_id}", json=data, timeout=TIME_OUT)
    print("PUT:", r.status_code, r.text)
    return r.json()

def delete_product(product_id: str) -> dict:
    r = requests.delete(f"{BASE}/{product_id}", timeout=TIME_OUT)
    print("DELETE:", r.status_code, r.text)
    if r.text:
        return r.json()
    return {}