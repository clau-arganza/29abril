import asyncio
import random
import time
from aiohttp import web

EXCUSAS = [
    "Los apuntes se los comió mi perro",
    "Se cayó el WiFi justo cuando iba a entregar",
    "Mi portátil decidió actualizarse durante 3 horas",
    "El campus virtual no cargaba",
    "Pensé que la entrega era mañana",
    "Me confundí de asignatura",
    "El archivo estaba en el ordenador de mi primo",
    "El pendrive desapareció ",
    "Mi madre me borró todo el trabajo sin querer",
    "Lo tenía hecho, pero no se guardó"
]


async def health(request):
    return web.json_response({
        "estado": "Servidor funcionando correctamente"
    })


async def excusa(request):
    alumno = request.query.get("alumno", "Alumno anónimo")

    inicio = time.time()

    print(f"Inicio generando excusa para {alumno}")

    # Simulamos una operación lenta de entrada/salida
    # Por ejemplo: consultar una base de datos, llamar a otra API, etc.
    await asyncio.sleep(3)

    excusa_elegida = random.choice(EXCUSAS)

    fin = time.time()

    print(f"Fin generando excusa para {alumno}")

    return web.json_response({
        "alumno": alumno,
        "excusa": excusa_elegida,
        "tiempo_generacion": round(fin - inicio, 2)
    })


app = web.Application()

app.add_routes([
    web.get("/health", health),
    web.get("/excusa", excusa),
])

web.run_app(app, host="0.0.0.0", port=8080)