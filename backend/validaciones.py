"""Validaciones del lado del servidor (las del navegador no bastan)."""
import re

RFC = re.compile(r'^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$')
CORREO = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')


def texto(valor):
    return (valor or '').strip()


def rfc_valido(rfc):
    return bool(RFC.match(rfc))


def correo_valido(correo):
    return bool(CORREO.match(correo)) and len(correo) <= 120


def telefono_valido(telefono):
    return bool(re.fullmatch(r'\d{10}', telefono))


def cp_valido(cp):
    return bool(re.fullmatch(r'\d{5}', cp))


def password_valida(password):
    # Mínimo 8 caracteres y al menos un número
    return len(password) >= 8 and any(c.isdigit() for c in password)
