import asyncio
import time
import aiohttp


ALUMNOS = [
    "Rodrigo",
    "Claudia",
    "Fran",
    "Jacinto",
    "Paula"
]


async def pedir_excusa(session, alumno):
    url = f"http://localhost:8080/excusa?alumno={alumno}"

    async with session.get(url) as respuesta:
        datos = await respuesta.json()
        print(datos)
        return datos


async def main():
    inicio = time.time()

    async with aiohttp.ClientSession() as session:
        tareas = []

        for alumno in ALUMNOS:
            tarea = pedir_excusa(session, alumno)
            tareas.append(tarea)

        await asyncio.gather(*tareas)

    fin = time.time()

    print()
    print(f"Tiempo total: {round(fin - inicio, 2)} segundos")


asyncio.run(main())