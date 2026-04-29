import asyncio
import os
import random
import time
from aiohttp import web
import redis.asyncio as redis


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


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


async def health(request):
    try:
        await redis_client.ping()
        estado_redis = "Redis conectado"
    except Exception:
        estado_redis = "Redis no disponible"

    return web.json_response({
        "estado": "API funcionando correctamente",
        "redis": estado_redis
    })


async def obtener_excusa(request):
    alumno = request.query.get("alumno", "Alumno anónimo")
    cache = request.query.get("cache", "on").lower()

    inicio = time.time()
    clave_cache = f"excusa:{alumno}"

    if cache == "on":
        try:
            excusa_cacheada = await redis_client.get(clave_cache)

            if excusa_cacheada:
                fin = time.time()
                return web.json_response({
                    "alumno": alumno,
                    "excusa": excusa_cacheada,
                    "cache": "HIT",
                    "tiempo_generacion": round(fin - inicio, 4)
                })

        except Exception:
            pass

    await asyncio.sleep(1)

    excusa_elegida = random.choice(EXCUSAS)

    estado_cache = "OFF"

    if cache == "on":
        try:
            await redis_client.set(clave_cache, excusa_elegida, ex=15)
            estado_cache = "MISS"
        except Exception:
            estado_cache = "REDIS_ERROR"

    fin = time.time()

    return web.json_response({
        "alumno": alumno,
        "excusa": excusa_elegida,
        "cache": estado_cache,
        "tiempo_generacion": round(fin - inicio, 4)
    })


async def crear_excusa(request):
    nueva_excusa = request.query.get("excusa")

    if not nueva_excusa:
        return web.json_response({
            "error": "Tienes que escribir una excusa en la URL",
            "ejemplo": "http://localhost:8080/crear?excusa=Se me olvidó entregar el trabajo"
        }, status=400)

    EXCUSAS.append(nueva_excusa)

    try:
        await redis_client.flushdb()
    except Exception:
        pass

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


async def fact(request):
    return await obtener_excusa(request)


app = web.Application()

app.add_routes([
    web.get("/health", health),
    web.get("/excusa", obtener_excusa),
    web.get("/crear", crear_excusa),
    web.get("/excusas", listar_excusas),
    web.get("/fact", fact),
])

web.run_app(app, host="0.0.0.0", port=8080)