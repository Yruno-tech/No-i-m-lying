from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    Response,
    stream_with_context
)

import json

from casos import generar_caso
from personajes import generar_personajes
from relaciones import generar_relaciones
from ia import InterrogatorioIA


app = Flask(__name__)

# Partida actual.
partida = None


# -----------------------------------------
# FUNCIONES AUXILIARES
# -----------------------------------------

def personaje_actual():

    if partida is None:
        return None

    indice = partida["indice"]

    if indice >= len(partida["personajes"]):
        return None

    return partida["personajes"][indice]


def informacion_personaje(personaje):

    return {
        "id": personaje["id"],
        "nombre": personaje["nombre"],
        "genero": personaje["genero"],
        "profesion": personaje["profesion"],
        "personalidad": personaje["personalidad"]
    }


def estado_actual():

    personaje = personaje_actual()

    if personaje is None:
        return None

    return {
        "personaje": informacion_personaje(personaje),
        "preguntas_restantes": 2 - partida["preguntas"],
        "numero": partida["indice"] + 1
    }


def terminar_partida(resultado, motivo):

    partida["terminada"] = True
    partida["resultado"] = resultado
    partida["motivo"] = motivo


# -----------------------------------------
# PANTALLA PRINCIPAL
# -----------------------------------------

@app.route("/")
def inicio():

    return render_template("index.html")


# -----------------------------------------
# INICIAR PARTIDA
# -----------------------------------------

@app.route("/api/start", methods=["POST"])
def iniciar_partida():

    global partida

    caso = generar_caso()

    personajes = generar_personajes(caso)

    generar_relaciones(personajes)

    interrogatorios = {}

    for personaje in personajes:

        interrogatorios[personaje["id"]] = InterrogatorioIA(
            personaje,
            caso
        )

    partida = {

        "caso": caso,

        "personajes": personajes,

        "interrogatorios": interrogatorios,

        "indice": 0,

        "preguntas": 0,

        "capturados": [],

        "liberados": [],

        "terminada": False,

        "resultado": None,

        "motivo": None
    }

    return jsonify({
        "ok": True,
        "estado": estado_actual()
    })


# -----------------------------------------
# HACER UNA PREGUNTA
# -----------------------------------------

@app.route("/api/ask", methods=["POST"])
def preguntar():

    if partida is None or partida["terminada"]:
        return jsonify({
            "error": "No hay una partida activa."
        }), 400

    personaje = personaje_actual()

    if personaje is None:
        return jsonify({
            "error": "No hay sospechosos disponibles."
        }), 400

    if partida["preguntas"] >= 2:
        return jsonify({
            "error": "Ya utilizaste las dos preguntas."
        }), 400

    datos = request.get_json(silent=True) or {}

    pregunta = datos.get("pregunta", "").strip()

    if not pregunta:
        return jsonify({
            "error": "La pregunta no puede estar vacía."
        }), 400

    # Consumimos la pregunta antes de comenzar el streaming.
    partida["preguntas"] += 1

    ia = partida["interrogatorios"][personaje["id"]]

    def generar_respuesta():

        yield json.dumps({
            "tipo": "inicio",
            "preguntas_restantes": 2 - partida["preguntas"]
        }, ensure_ascii=False) + "\n"

        try:

            for fragmento in ia.preguntar_stream(pregunta):

                yield json.dumps({
                    "tipo": "fragmento",
                    "texto": fragmento
                }, ensure_ascii=False) + "\n"

            yield json.dumps({
                "tipo": "final"
            }, ensure_ascii=False) + "\n"

        except Exception as error:

            print("Error en respuesta:", error)

            yield json.dumps({
                "tipo": "error",
                "mensaje": "No se pudo completar la respuesta."
            }, ensure_ascii=False) + "\n"

    return Response(
        stream_with_context(generar_respuesta()),
        content_type="application/x-ndjson; charset=utf-8"
    )


# -----------------------------------------
# EXPEDIENTE
# -----------------------------------------

@app.route("/api/expediente")
def expediente():

    if partida is None:
        return jsonify({
            "error": "No hay una partida activa."
        }), 400

    caso = partida["caso"]

    sospechosos = [
        informacion_personaje(personaje)
        for personaje in partida["personajes"]
    ]

    return jsonify({

        "caso": {
            "titulo": caso["titulo"],
            "acontecimiento": caso["acontecimiento"],
            "incidente": caso["incidente"],
            "evidencias": caso["evidencias"]
        },

        "sospechosos": sospechosos
    })


# -----------------------------------------
# DECIDIR: CAPTURAR O LIBERAR
# -----------------------------------------

@app.route("/api/decision", methods=["POST"])
def decidir():

    if partida is None or partida["terminada"]:
        return jsonify({
            "error": "No hay una partida activa."
        }), 400

    if partida["preguntas"] < 2:
        return jsonify({
            "error": "Debes utilizar las dos preguntas antes de decidir."
        }), 400

    datos = request.get_json(silent=True) or {}

    decision = datos.get("decision")

    if decision not in ["capturar", "liberar"]:
        return jsonify({
            "error": "Decisión inválida."
        }), 400

    personaje = personaje_actual()

    rol = personaje["rol"]

    nombre = personaje["nombre"]

    if decision == "capturar":

        partida["capturados"].append(personaje)

        # Capturar al alcalde provoca derrota inmediata.
        if rol == "Alcalde":

            terminar_partida(
                "derrota",
                f"Capturaste al alcalde, {nombre}. "
                "Tu investigación terminó."
            )

        # Contabilizar los inocentes capturados.
        elif rol == "Inocente":

            inocentes_capturados = sum(
                1 for p in partida["capturados"]
                if p["rol"] == "Inocente"
            )

            if inocentes_capturados == 5:

                terminar_partida(
                    "derrota",
                    "Capturaste a los cinco inocentes."
                )

        # Contabilizar los impostores capturados.
        elif rol == "Impostor":

            impostores_capturados = sum(
                1 for p in partida["capturados"]
                if p["rol"] == "Impostor"
            )

            if impostores_capturados == 4:

                terminar_partida(
                    "victoria",
                    "Capturaste a los cuatro impostores."
                )

    else:

        partida["liberados"].append(personaje)

        # Dejar escapar a un impostor provoca derrota.
        if rol == "Impostor":

            terminar_partida(
                "derrota",
                f"Liberaste a {nombre}, que era un impostor."
            )

    # Si la partida sigue activa, avanzar al siguiente.
    if not partida["terminada"]:

        partida["indice"] += 1
        partida["preguntas"] = 0

        if partida["indice"] >= len(partida["personajes"]):

            terminar_partida(
                "derrota",
                "Terminaste todos los interrogatorios "
                "sin capturar a los cuatro impostores."
            )

    return jsonify({

        "ok": True,

        "terminada": partida["terminada"],

        "resultado": partida["resultado"],

        "motivo": partida["motivo"],

        "estado": estado_actual(),

        "personaje_anterior": informacion_personaje(personaje)

    })


# -----------------------------------------
# RESULTADOS FINALES
# -----------------------------------------

@app.route("/api/results")
def resultados():

    if partida is None or not partida["terminada"]:
        return jsonify({
            "error": "La partida todavía no terminó."
        }), 400

    personajes = []

    for personaje in partida["personajes"]:

        if personaje in partida["capturados"]:
            estado = "Capturado"

        elif personaje in partida["liberados"]:
            estado = "Liberado"

        else:
            estado = "Sin interrogar"

        personajes.append({

            "nombre": personaje["nombre"],

            "rol": personaje["rol"],

            "estado": estado

        })

    return jsonify({

        "resultado": partida["resultado"],

        "motivo": partida["motivo"],

        "personajes": personajes

    })


# -----------------------------------------
# EJECUTAR SERVIDOR
# -----------------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        threaded=True
    )