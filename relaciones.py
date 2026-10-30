
import random

VINCULOS = {
    "compañeros de trabajo": (50, 80),
    "amigos desde hace años": (75, 100),
    "conocidos del edificio": (30, 60),
    "familiares": (70, 100),
    "antiguos compañeros de estudio": (50, 85),
    "tienen una mala relación": (10, 35),
    "mantienen una relación de desconfianza": (10, 30),
    "son buenos amigos": (80, 100)
}


def generar_relaciones(personajes):

    for personaje in personajes:

        otros = [
            p for p in personajes
            if p["id"] != personaje["id"]
        ]

        # Cada personaje conoce a dos personas.
        conocidos = random.sample(otros, 2)

        relaciones = []
        conocimientos = []

        for otro in conocidos:

            # Generar vínculo y confianza coherentes.
            vinculo = random.choice(list(VINCULOS.keys()))

            confianza_min, confianza_max = VINCULOS[vinculo]
            confianza = random.randint(
                confianza_min,
                confianza_max
            )

            relacion = {
                "personaje": otro["nombre"],
                "vinculo": vinculo,
                "confianza": confianza
            }

            relaciones.append(relacion)

            # Información real sobre esa persona.
            datos = otro["datos_reales"]

            conocimiento = {
                "personaje": otro["nombre"],
                "informacion": (
                    f"Sabe que {otro['nombre']} estuvo en "
                    f"{datos['lugar']} a las {datos['hora']}, "
                    f"{datos['actividad']}."
                ),
                "lugar": datos["lugar"],
                "hora": datos["hora"],
                "actividad": datos["actividad"]
            }

            conocimientos.append(conocimiento)

        personaje["relaciones"] = relaciones
        personaje["conocimientos"] = conocimientos

        # El secreto está relacionado con uno de sus conocidos.
        relacion_secreta = random.choice(relaciones)
        vinculo = relacion_secreta["vinculo"]

        if vinculo == "tienen una mala relación":
            descripcion = "tiene una mala relación"
        elif vinculo == "mantienen una relación de desconfianza":
            descripcion = "mantiene una relación de desconfianza"
        else:
            descripcion = vinculo

        personaje["secreto"] = (
            f"Prefiere no revelar que {descripcion} con "
            f"{relacion_secreta['personaje']}."
        )

    return personajes
