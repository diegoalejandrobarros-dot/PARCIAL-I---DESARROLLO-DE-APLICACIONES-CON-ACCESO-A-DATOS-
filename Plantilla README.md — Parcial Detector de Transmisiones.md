# Parcial — Detector de Transmisiones Sospechosas

Nombre:  Diego Barros 
Grupo: 4E

## 1. ¿Qué debe hacer el programa?

Escriba en máximo 3 o 4 líneas cuál es el objetivo del programa.

Respuesta:
el objetivo del programa es llevar un registro de los movimientos financieros y verificar
el riesgo de cada uno de ellos, para tener un control en los ingresos de la compañia
aumentar la veracidad de las transacciones y disminuir las estafas y perdidas.
---

## 2. Clase `Transmision`

La clase tendrá los siguientes atributos:

- `id`:
- `origen`:
- `mensaje`:
- `puntaje`:
- `clasificacion`:

Escriba brevemente qué representa cada uno.
id-> numero de identificacion de quien hace la transaccion 
origen-> es el lugar de donde el remitente realiza el movimiento financiero
mensaje-> asunto o tema con respecto a la transaccion
puntaje-> rango que sirve para medir el riesgo de la transaccion
clasificacion-> categoria del nivel de riesgo segun el puntaje obtenido
---

## 3. Métodos

### `analizar()`

Responsabilidad: calcular el riesgo de cada una de las transacciones segun valor, hora, dispositivo y pais.

### `clasificar()
Responsabilidad: categorizar el nivel de riesgo de las transacciones y posicinarlos ya sean normal, sospechosa o alto riesgo 

### `to_dict()`

Responsabilidad: Convierte el objeto Transaccion en un diccionario que pueda guardarse en JSON.

### `from_dict()`

Responsabilidad: Recibe un diccionario leído desde JSON y retorna un objeto Transaccion.



---

## 4. Algoritmo de análisis

Complete el siguiente pseudocódigo:

```text
puntaje = 0

SI el mensaje contiene _Valor mayor o igual a $2.000.000_________________
    sumar __30____ puntos

SI el mensaje contiene ___Hora entre 0 y 5_______________
    sumar ___20___ puntos

SI el mensaje contiene ____País diferente de Colombia______________
    sumar __25____ puntos

SI el mensaje contiene _____Dispositivo NO conocido_____________
    sumar ___30___ puntos
```

---

## 5. Persistencia

Explique brevemente qué ocurre al iniciar el programa:

```text
JSON
 ↓
________leer y cargar los datos____________
 ↓
______crear objetos de transmision______________
```

Explique qué ocurre al guardar:

```text
Objetos
 ↓
____convertir a diccionarios________________
 ↓
JSON
```

---

## 6. Menú

Indique qué debe hacer cada opción:

### Opción 1 — Registrar transmisión

1. solicitar al usuario los datos
2.  crear un objeto transmision con los datos ingresados
3.  analizar, clasificar y guardar la informacion en el archivo JSON

### Opción 2 — Listar transmisiones

1. mostrar todas las transmisiones registradas
2.  mostrar informacion como id, origen, mensaje, puntaje y clasificacion de riesgo

### Opción 3 — Salir

Acción: Cerrar el programa de forma segura, conservando las transmisiones registradas en el archivo JSON.

---

## Notas

Este archivo debe completarse durante los primeros 15 minutos del parcial, antes de comenzar la implementación.