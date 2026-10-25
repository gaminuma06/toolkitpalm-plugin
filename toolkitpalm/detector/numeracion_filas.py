# -*- coding: utf-8 -*-
"""
Estados de las palmas numeradas y pedidos al servidor para el trazo de las
líneas y la renumeración después de editar a mano.

El método (armado de filas, palmas muertas, trazo y renumeración) corre en el
servidor de ToolkitPalm y no viaja en el plugin.
"""
import requests

VIVA, MUERTA, REVISAR = "viva", "muerta", "revisar"

DETECTADA, CALCULADA, MANUAL = "detectada", "calculada", "manual"


def _pedir(ruta, cuerpo):
    from ..client_identity import cabeceras_autenticacion
    from ..config import NUMERACION_BASE_URL
    r = requests.post(f"{NUMERACION_BASE_URL}/{ruta}", json=cuerpo,
                      headers=cabeceras_autenticacion(), timeout=180)
    if r.status_code == 401:
        raise RuntimeError("Inicie sesión con su cuenta de Google en ToolkitPalm.")
    r.raise_for_status()
    return r.json()


def trazos_de_filas(filas, ux, uy):
    """Trazo de cada fila (listas ordenadas de (x, y)) que sigue su curva real."""
    datos = _pedir("trazos", {"filas": [[[float(x), float(y)] for x, y in f] for f in filas],
                              "ux": float(ux), "uy": float(uy)})
    return [[tuple(p) for p in t] for t in datos["trazos"]]


def renumerar(puntos):
    """Reasigna línea y número después de agregar, borrar o mover palmas.

    puntos: lista de (fid, x, y, linea, palma). Devuelve (asignacion, filas, trazos):
    asignacion {fid: (linea, palma)}, filas {linea: [fid, ...]} en orden y
    trazos {linea: [(x, y), ...]}.
    """
    datos = _pedir("renumerar", {"puntos": [[int(f), float(x), float(y), int(l or 0), int(p or 0)]
                                            for f, x, y, l, p in puntos]})
    asignacion = {int(k): tuple(v) for k, v in datos["asignacion"].items()}
    filas = {int(k): v for k, v in datos["filas"].items()}
    trazos = {int(k): [tuple(p) for p in v] for k, v in datos["trazos"].items()}
    return asignacion, filas, trazos
