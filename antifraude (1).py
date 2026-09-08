"""
Sistema Antifraude
Parcial practico - clases, objetos, listas, diccionarios y persistencia en JSON.
"""

import json
import os

ARCHIVO_TRANSACCIONES = "transacciones.json"


class Transaccion:
    """Representa una transaccion financiera y su analisis de riesgo."""

    def __init__(self, id, titular, valor, hora, pais, dispositivo_conocido):
        # --- Validaciones minimas ---
        if titular is None or str(titular).strip() == "":
            raise ValueError("El titular no puede estar vacio.")
        if not isinstance(valor, (int, float)) or isinstance(valor, bool) or valor <= 0:
            raise ValueError("El valor debe ser mayor que cero.")
        if not isinstance(hora, int) or isinstance(hora, bool) or not (0 <= hora <= 23):
            raise ValueError("La hora debe estar entre 0 y 23.")
        if pais is None or str(pais).strip() == "":
            raise ValueError("El pais no puede estar vacio.")
        if not isinstance(dispositivo_conocido, bool):
            raise ValueError("dispositivo_conocido debe ser un valor booleano.")

        # --- Atributos iniciales ---
        self.id = id
        self.titular = titular
        self.valor = valor
        self.hora = hora
        self.pais = pais
        self.dispositivo_conocido = dispositivo_conocido

        # --- Atributos calculados automaticamente ---
        self.puntaje_riesgo = self.calcular_riesgo()
        self.clasificacion = self.clasificar()

    def calcular_riesgo(self):
        """Calcula y retorna el puntaje de riesgo de la transaccion."""
        puntaje = 0

        if self.valor >= 2_000_000:
            puntaje += 30

        if 0 <= self.hora <= 5:
            puntaje += 20

        if self.pais.strip().lower() != "colombia":
            puntaje += 25

        if not self.dispositivo_conocido:
            puntaje += 30

        return puntaje

    def clasificar(self):
        """Retorna la clasificacion correspondiente segun el puntaje de riesgo."""
        puntaje = self.puntaje_riesgo

        if puntaje >= 60:
            return "ALTO RIESGO"
        elif puntaje >= 30:
            return "SOSPECHOSA"
        else:
            return "NORMAL"

    def to_dict(self):
        """Convierte el objeto Transaccion en un diccionario para guardarlo en JSON."""
        return {
            "id": self.id,
            "titular": self.titular,
            "valor": self.valor,
            "hora": self.hora,
            "pais": self.pais,
            "dispositivo_conocido": self.dispositivo_conocido,
            "puntaje_riesgo": self.puntaje_riesgo,
            "clasificacion": self.clasificacion,
        }

    @classmethod
    def from_dict(cls, datos):
        """Recibe un diccionario leido desde JSON y retorna un objeto Transaccion."""
        return cls(
            id=datos["id"],
            titular=datos["titular"],
            valor=datos["valor"],
            hora=datos["hora"],
            pais=datos["pais"],
            dispositivo_conocido=datos["dispositivo_conocido"],
        )

    def __str__(self):
        return (f"ID: {self.id} | Titular: {self.titular} | "
                f"Puntaje: {self.puntaje_riesgo} | Clasificacion: {self.clasificacion}")


def cargar_transacciones(ruta=ARCHIVO_TRANSACCIONES):
    """Carga las transacciones desde el archivo JSON. Si no existe, retorna una lista vacia."""
    if not os.path.exists(ruta):
        return []

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Aviso: no se pudo leer '{ruta}' ({error}). Se inicia con lista vacia.")
        return []

    transacciones = []
    for item in datos:
        try:
            transacciones.append(Transaccion.from_dict(item))
        except (ValueError, KeyError) as error:
            print(f"Aviso: se omitio un registro invalido del archivo ({error}).")

    return transacciones


def guardar_transacciones(transacciones, ruta=ARCHIVO_TRANSACCIONES):
    """Convierte cada objeto a diccionario y guarda la lista completa en JSON."""
    datos = [t.to_dict() for t in transacciones]
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def siguiente_id(transacciones):
    """Calcula el proximo ID disponible (evita pedirlo manualmente y que se repita)."""
    if not transacciones:
        return 1
    return max(t.id for t in transacciones) + 1


def solicitar_texto(mensaje):
    """Pide un texto por consola hasta que no este vacio."""
    while True:
        valor = input(mensaje).strip()
        if valor != "":
            return valor
        print("Este campo no puede estar vacio. Intente de nuevo.")


def solicitar_valor(mensaje):
    """Pide un numero (valor de la transaccion) mayor que cero."""
    while True:
        texto = input(mensaje).strip()
        try:
            valor = float(texto)
        except ValueError:
            print("Ingrese un numero valido.")
            continue
        if valor <= 0:
            print("El valor debe ser mayor que cero.")
            continue
        return valor


def solicitar_hora(mensaje):
    """Pide la hora de la transaccion, entre 0 y 23."""
    while True:
        texto = input(mensaje).strip()
        try:
            hora = int(texto)
        except ValueError:
            print("Ingrese un numero entero valido.")
            continue
        if not (0 <= hora <= 23):
            print("La hora debe estar entre 0 y 23.")
            continue
        return hora


def solicitar_booleano(mensaje):
    """Pide una respuesta si/no y la convierte a booleano."""
    while True:
        texto = input(mensaje).strip().lower()
        if texto in ("s", "si", "si", "true", "1"):
            return True
        if texto in ("n", "no", "false", "0"):
            return False
        print("Respuesta no valida. Escriba 's' o 'n'.")


def ingresar_transaccion(transacciones):
    """Pide por consola los datos de una nueva transaccion y la agrega a la lista."""
    print("\n--- Nueva transaccion ---")
    id_nuevo = siguiente_id(transacciones)
    titular = solicitar_texto("Titular: ")
    valor = solicitar_valor("Valor: ")
    hora = solicitar_hora("Hora (0-23): ")
    pais = solicitar_texto("Pais: ")
    dispositivo_conocido = solicitar_booleano("¿Dispositivo conocido? (s/n): ")

    try:
        transaccion = Transaccion(id_nuevo, titular, valor, hora, pais, dispositivo_conocido)
    except ValueError as error:
        # Por si en el futuro se agregan reglas nuevas a la clase.
        print(f"No se pudo crear la transaccion: {error}")
        return

    transacciones.append(transaccion)
    print("\nTransaccion creada:")
    print(transaccion)


def mostrar_transacciones(transacciones):
    """Imprime todas las transacciones en memoria."""
    if not transacciones:
        print("No hay transacciones registradas.")
        return
    print("\n--- Transacciones registradas ---")
    for transaccion in transacciones:
        print(transaccion)


def cargar_casos_prueba(transacciones):
    """Crea y agrega los 3 casos de prueba del enunciado."""
    casos_prueba = [
        dict(id=siguiente_id(transacciones) + 0, titular="Laura Gomez", valor=3500000, hora=2,
             pais="Colombia", dispositivo_conocido=False),
    ]
    # Se generan de a uno para que los IDs queden consecutivos si ya habia transacciones cargadas.
    datos_restantes = [
        dict(titular="Carlos Perez", valor=500000, hora=14, pais="Colombia", dispositivo_conocido=True),
        dict(titular="Ana Torres", valor=2500000, hora=10, pais="Peru", dispositivo_conocido=True),
    ]

    for caso in casos_prueba:
        try:
            transaccion = Transaccion(**caso)
            transacciones.append(transaccion)
            print(transaccion)
        except ValueError as error:
            print(f"Error al crear la transaccion: {error}")

    for datos in datos_restantes:
        try:
            transaccion = Transaccion(id=siguiente_id(transacciones), **datos)
            transacciones.append(transaccion)
            print(transaccion)
        except ValueError as error:
            print(f"Error al crear la transaccion: {error}")


def mostrar_menu():
    print("\n===== SISTEMA ANTIFRAUDE =====")
    print("1. Agregar transaccion")
    print("2. Ver transacciones")
    print("3. Cargar los 3 casos de prueba del enunciado")
    print("4. Guardar y salir")
    return input("Seleccione una opcion: ").strip()


def main():
    transacciones = cargar_transacciones()
    print(f"Se cargaron {len(transacciones)} transaccion(es) desde '{ARCHIVO_TRANSACCIONES}'.")

    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            ingresar_transaccion(transacciones)
        elif opcion == "2":
            mostrar_transacciones(transacciones)
        elif opcion == "3":
            cargar_casos_prueba(transacciones)
        elif opcion == "4":
            guardar_transacciones(transacciones)
            print(f"{len(transacciones)} transaccion(es) guardadas en '{ARCHIVO_TRANSACCIONES}'.")
            break
        else:
            print("Opcion no valida. Intente de nuevo.")


if __name__ == "__main__":
    main()
