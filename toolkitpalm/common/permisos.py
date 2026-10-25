# -*- coding: utf-8 -*-
"""Quién puede ver las funciones que todavía no están publicadas."""


def es_administrador():
    """True si la cuenta con sesión iniciada es del dueño del servicio."""
    try:
        from ..config import ADMIN_EMAILS, ADMIN_API_KEY
        if not ADMIN_EMAILS or not ADMIN_API_KEY:
            return False
        from .. import google_auth
        datos = google_auth.perfil() or {}
        return (datos.get("email", "") or "").lower() in ADMIN_EMAILS
    except Exception:
        return False
