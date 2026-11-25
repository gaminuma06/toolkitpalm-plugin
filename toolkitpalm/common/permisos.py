# -*- coding: utf-8 -*-
"""Quién es administrador: lo decide el SERVIDOR (GET /apis/creditos/yo -> es_admin).

En el plugin no hay claves ni listas de correos: solo se pregunta al servidor con
la sesión de Google del usuario, y se guarda la respuesta unos minutos.
"""
import time

_CACHE = {"t": 0.0, "datos": None, "sesion": ""}
_DURACION = 300  # segundos


def perfil_servidor(forzar=False):
    """Datos de la cuenta según el servidor, o None si no hay sesión/conexión."""
    try:
        from .. import google_auth
        token = google_auth.obtener_id_token()
    except Exception:
        token = None
    if not token:
        return None
    if (not forzar and _CACHE["datos"] is not None and _CACHE["sesion"] == token
            and time.time() - _CACHE["t"] < _DURACION):
        return _CACHE["datos"]
    try:
        import requests
        from ..config import CREDITS_BASE_URL, API_KEY
        r = requests.get(f"{CREDITS_BASE_URL}/yo",
                         headers={"X-API-Key": API_KEY, "Authorization": f"Bearer {token}"},
                         timeout=10)
        datos = r.json() if r.status_code == 200 else None
    except Exception:
        datos = None
    _CACHE.update(t=time.time(), datos=datos, sesion=token)
    return datos


def es_administrador():
    """True si el servidor dice que la cuenta con sesión iniciada es administradora."""
    datos = perfil_servidor()
    return bool(datos and datos.get("es_admin"))
