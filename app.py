import asyncio
import os
import random
import time
from aiohttp import web
import redis.asyncio as redis


FACTS = [
    "Docker Compose permite levantar varios servicios con un solo comando.",
    "Redis se puede usar como sistema de cache en memoria.",
    "Locust sirve para hacer pruebas de carga concurrentes.",
    "Una cache puede reducir el tiempo de respuesta de una API.",
    "Docker permite ejecutar aplicaciones en contenedores.",
    "Una API puede atender muchas peticiones al mismo tiempo si usa programación asíncrona.",
]

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


async def health(request):
    return web.json_response({
        "status": "ok",
        "message": "API funcionando correctamente"
    })


async def fact(request):
    cache_mode = request.query.get("cache", "on")
    cache_key = "random_fact"

    inicio = time.time()

    if cache_mode == "on":
        try:
            cached_fact = await redis_client.get(cache_key)

            if cached_fact:
                fin = time.time()
                return web.json_response({
                    "fact": cached_fact,
                    "cache": "HIT",
                    "tiempo_respuesta": round(fin - inicio, 4)
                })

        except Exception:
            pass

    await asyncio.sleep(1)

    selected_fact = random.choice(FACTS)

    if cache_mode == "on":
        try:
            await redis_client.set(cache_key, selected_fact, ex=10)
            cache_status = "MISS"
        except Exception:
            cache_status = "REDIS_ERROR"
    else:
        cache_status = "OFF"

    fin = time.time()

    return web.json_response({
        "fact": selected_fact,
        "cache": cache_status,
        "tiempo_respuesta": round(fin - inicio, 4)
    })


app = web.Application()

app.add_routes([
    web.get("/health", health),
    web.get("/fact", fact),
])

web.run_app(app, host="0.0.0.0", port=8080)