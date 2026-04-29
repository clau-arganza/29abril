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
    "El pendrive desapareció misteriosamente",
    "Mi gato pisó el teclado y borró el trabajo",
    "Lo tenía hecho, pero no se guardó",
    "Mi madre me borró todo el trabajo sin querer"
]


async def health(request):
    return web.json_response({
        "estado": "Servidor funcionando correctamente"
    })


async def obtener_excusa(request):
    alumno = request.query.get("alumno", "Alumno anónimo")

    inicio = time.time()

    print(f"Inicio generando excusa para {alumno}")

    await asyncio.sleep(3)

    excusa_elegida = random.choice(EXCUSAS)

    fin = time.time()

    print(f"Fin generando excusa para {alumno}")

    return web.json_response({
        "alumno": alumno,
        "excusa": excusa_elegida,
        "tiempo_generacion": round(fin - inicio, 2)
    })


async def crear_excusa(request):
    nueva_excusa = request.query.get("excusa")

    if not nueva_excusa:
        return web.json_response({
            "error": "Tienes que escribir una excusa en la URL",
            "ejemplo": "http://localhost:8080/crear?excusa=Se me olvidó entregar el trabajo"
        }, status=400)

    EXCUSAS.append(nueva_excusa)

    return web.json_response({
        "mensaje": "Excusa creada correctamente",
        "excusa_creada": nueva_excusa,
        "total_excusas": len(EXCUSAS)
    })


async def listar_excusas(request):
    return web.json_response({
        "total_excusas": len(EXCUSAS),
        "excusas": EXCUSAS
    })


app = web.Application()

app.add_routes([
    web.get("/health", health),
    web.get("/excusa", obtener_excusa),
    web.get("/crear", crear_excusa),
    web.get("/excusas", listar_excusas),
])

web.run_app(app, host="0.0.0.0", port=8080)