
import random

NOMBRES = [
    "Andrés", "Lucía", "Martín", "Sofía", "Diego",
    "Valentina", "Tomás", "Camila", "Nicolás", "Julieta"
]
GENEROS = {
    "Andrés": "hombre",
    "Lucía": "mujer",
    "Martín": "hombre",
    "Sofía": "mujer",
    "Diego": "hombre",
    "Valentina": "mujer",
    "Tomás": "hombre",
    "Camila": "mujer",
    "Nicolás": "hombre",
    "Julieta": "mujer"
}
PERSONALIDADES = [
    "Nervioso y desconfiado",
    "Tranquilo y reservado",
    "Arrogante y desafiante",
    "Amable y colaborador",
    "Impulsivo y temperamental",
    "Tímido e inseguro",
    "Serio y calculador",
    "Hablador y extrovertido",
    "Sarcástico y provocador",
    "Frío y distante"
]

PROFESIONES = [
    "Guardia de seguridad",
    "Empleado administrativo",
    "Bibliotecario",
    "Técnico de mantenimiento",
    "Médico",
    "Profesor",
    "Periodista",
    "Abogado",
    "Cocinero",
    "Estudiante"
]

LUGARES = [
    "la biblioteca",
    "la cafetería",
    "el estacionamiento",
    "la oficina",
    "el laboratorio",
    "la entrada principal",
    "el pasillo norte",
    "el depósito"
]

ACTIVIDADES = [
    "leyendo unos documentos",
    "hablando por teléfono",
    "trabajando en la computadora",
    "esperando a un compañero",
    "caminando por el edificio",
    "descansando"
]

HORARIOS = [
    "21:00",
    "21:15",
    "21:30",
    "21:45",
    "22:00"
]


def generar_personajes(caso):

    roles = (
        ["Inocente"] * 5
        + ["Impostor"] * 4
        + ["Alcalde"]
    )

    declaraciones = [True] * 5 + [False] * 5

    random.shuffle(roles)
    random.shuffle(declaraciones)

    personajes = []

    # Elegimos algunos personajes que estuvieron
    # en el lugar del incidente a la hora del incidente.
    cantidad_testigos = random.randint(2, 4)

    testigos = set(
        random.sample(range(10), cantidad_testigos)
    )

    for i in range(10):

        nombre = NOMBRES[i]
        profesion = random.choice(PROFESIONES)
        
        lugar_real = random.choice(LUGARES)
        hora_real = random.choice(HORARIOS)
        actividad_real = random.choice(ACTIVIDADES)

        # Algunos personajes estuvieron en el lugar
        # del incidente exactamente a esa hora.
        if i in testigos:
            lugar_real = caso["lugar_incidente"]
            hora_real = caso["hora_incidente"]

        persona_vista = random.choice(
            [n for n in NOMBRES if n != nombre]
        )

        lugar_falso = random.choice(
            [l for l in LUGARES if l != lugar_real]
        )

        actividad_falsa = random.choice(
            [a for a in ACTIVIDADES if a != actividad_real]
        )

        hora_falsa = random.choice(
            [h for h in HORARIOS if h != hora_real]
        )

        persona_falsa = random.choice(
            [
                n for n in NOMBRES
                if n not in [nombre, persona_vista]
            ]
        )

        personaje = {
            "id": i + 1,
            "nombre": nombre,
            "genero": GENEROS[nombre],
            "rol": roles[i],
            "dice_verdad": declaraciones[i],

            "personalidad": random.choice(PERSONALIDADES),
            "profesion": profesion,

            "historia": (
                f"{nombre} trabaja como {profesion}."
            ),

            "datos_reales": {
                "lugar": lugar_real,
                "hora": hora_real,
                "actividad": actividad_real,
                "persona_vista": persona_vista
            },

            "datos_falsos": {
                "lugar": lugar_falso,
                "hora": hora_falsa,
                "actividad": actividad_falsa,
                "persona_vista": persona_falsa
            },

            "secreto": ""
        }

        personajes.append(personaje)

    return personajes
