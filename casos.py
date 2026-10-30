
import random


LUGARES = [
    "el laboratorio",
    "la oficina principal",
    "el depósito",
    "la sala de control",
    "la biblioteca"
]

HORAS = [
    "21:30",
    "22:00",
    "22:30",
    "23:00"
]


def generar_caso():

    lugar = random.choice(LUGARES)
    hora = random.choice(HORAS)

    casos = [
        {
            "titulo": "El apagón del edificio",
            "acontecimiento": (
                "Se produjo un apagón inesperado "
                "en el edificio municipal."
            ),
            "incidente": (
                f"A las {hora}, alguien manipuló "
                f"el sistema eléctrico en {lugar}."
            ),
            "lugar_incidente": lugar,
            "hora_incidente": hora,
            "evidencias": [
                "Se encontraron marcas recientes "
                "en el panel eléctrico.",
                "Una cámara dejó de funcionar "
                "durante varios minutos.",
                "Se encontró una herramienta "
                "cerca del lugar del incidente."
            ]
        },

        {
            "titulo": "La desaparición del expediente",
            "acontecimiento": (
                "Desapareció un expediente importante "
                "del edificio municipal."
            ),
            "incidente": (
                f"A las {hora}, alguien retiró "
                f"un expediente de {lugar}."
            ),
            "lugar_incidente": lugar,
            "hora_incidente": hora,
            "evidencias": [
                "El armario donde se guardaba "
                "el expediente estaba abierto.",
                "Se encontró una hoja rota "
                "cerca del lugar.",
                "Alguien utilizó una llave "
                "fuera del horario habitual."
            ]
        },

        {
            "titulo": "El sabotaje de seguridad",
            "acontecimiento": (
                "El sistema de seguridad del edificio "
                "fue manipulado."
            ),
            "incidente": (
                f"A las {hora}, alguien desactivó "
                f"un sistema de seguridad en {lugar}."
            ),
            "lugar_incidente": lugar,
            "hora_incidente": hora,
            "evidencias": [
                "Se detectó un acceso no autorizado.",
                "Una cámara registró movimientos "
                "extraños.",
                "El sistema fue desconectado "
                "manualmente."
            ]
        }
    ]

    caso = random.choice(casos)

    return caso
