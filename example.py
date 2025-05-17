import requests
import json
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token


BASE_URL = 'http://127.0.0.1:5000/'  # URL de la API Flask

def registrar_usuario():
    print("\n--- Registro de Usuario ---")
    nombre = input("Nombre de usuario: ")
    contrasenya = input("Contraseña: ")
    rol = input("Rol (comprador / vendedor / administrador): ")

    datos = {
        "nombre": nombre,
        "contrasenya": contrasenya,
        "rol": rol
    }
    try:
        respuesta = requests.post(f"{BASE_URL}/register", json=datos)

        if respuesta.status_code == 201:
            data = respuesta.json()
            print("Usuario registrado con éxito.")
            print("Token:", data.get("access_token"))
        else:
            try:
                error = respuesta.json().get("error")
            except ValueError:
                error = respuesta.text
            print(f"Error ({respuesta.status_code}):", error)
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar con la API. ¿Está corriendo?")

def iniciar_sesion():
    print("\n--- Inicio de Sesión ---")
    nombre = input("Nombre de usuario: ")
    contrasenya = input("Contraseña: ")

    datos = {
        "nombre": nombre,
        "contrasenya": contrasenya
    }

    respuesta = requests.post(f"{BASE_URL}/login", json=datos)

    if respuesta.status_code == 200:
        data = respuesta.json()
        print("Inicio de sesión correcto.")
        print("Token:", data.get("access_token"))
    else:
        print("Error:", respuesta.json().get("error"))

def menu():
    while True:
        print("\n=== MENÚ DE PRUEBA DE LA API ===")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
