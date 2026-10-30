
import random

from personajes import generar_personajes
from relaciones import generar_relaciones
from casos import generar_caso
from ia import InterrogatorioIA


# =============================================
# CONFIGURACIÓN DEL JUEGO
# =============================================

TOTAL_SOSPECHOSOS = 10
TOTAL_IMPOSTORES = 4
TOTAL_INOCENTES = 5

PREGUNTAS_POR_PERSONA = 2


# =============================================
# INTERROGATORIO
# =============================================

def interrogar(personaje, ia):

    print("\n" + "=" * 55)
    print(
        f"SOSPECHOSO {personaje['id']}: "
        f"{personaje['nombre']}"
    )
    print("=" * 55)

    print(f"Profesión: {personaje['profesion']}")
    print(f"Personalidad: {personaje['personalidad']}")

    numero = 1

    while numero <= PREGUNTAS_POR_PERSONA:

        print(f"\nPREGUNTA {numero}/{PREGUNTAS_POR_PERSONA}")

        pregunta = input("Detective: ").strip()

        if not pregunta:
            print("Debes escribir una pregunta.")
            continue

        print(f"\n{personaje['nombre']} está pensando...")

        respuesta = ia.preguntar(pregunta)

        print(f"\n{personaje['nombre']}:")
        print(respuesta)

        numero += 1

    print("\n" + "-" * 55)
    print("FINALIZÓ EL INTERROGATORIO")
    print("-" * 55)

    while True:

        decision = input(
            "\n¿Qué decides? "
            "(L)iberar / (C)apturar: "
        ).strip().lower()

        if decision in ["l", "liberar"]:
            return "liberado"

        elif decision in ["c", "capturar"]:
            return "capturado"

        print("Decisión inválida. Inténtalo nuevamente.")


# =============================================
# RESULTADOS DE LA PARTIDA
# =============================================

def mostrar_resultados(
    sospechosos,
    capturados,
    liberados,
    impostores_capturados,
    inocentes_capturados
):

    print("\n" + "=" * 55)
    print("              RESULTADOS DE LA PARTIDA")
    print("=" * 55)

    print(f"\nSospechosos procesados: {len(capturados) + len(liberados)}")
    print(f"Personas capturadas: {len(capturados)}")
    print(f"Personas liberadas: {len(liberados)}")

    print(f"Impostores capturados: {impostores_capturados}/4")
    print(f"Inocentes capturados: {inocentes_capturados}/5")

    print("\nDETALLES:")

    for personaje in sospechosos:

        estado = (
            "CAPTURADO"
            if personaje in capturados
            else "LIBERADO"
            if personaje in liberados
            else "SIN PROCESAR"
        )

        print(
            f"- {personaje['nombre']}: "
            f"{estado} | Rol: {personaje['rol']}"
        )


# =============================================
# INICIAR PARTIDA
# =============================================

def jugar():

    # Generar el mundo del juego.
    caso = generar_caso()

    sospechosos = generar_personajes(caso)

    generar_relaciones(sospechosos)

    # Estadísticas.
    capturados = []
    liberados = []

    impostores_capturados = 0
    inocentes_capturados = 0

    derrota = False
    victoria = False

    # =========================================
    # PRESENTACIÓN
    # =========================================

    print("\n" + "=" * 55)
    print("                 NO, I'M LYING")
    print("=" * 55)

    print(f"\nCASO: {caso['titulo']}")

    print(f"\n{caso['acontecimiento']}")
    print(caso["incidente"])

    print("\nINFORMACIÓN DEL OPERATIVO:")
    print(f"- Sospechosos: {TOTAL_SOSPECHOSOS}")
    print(f"- Impostores: {TOTAL_IMPOSTORES}")
    print(f"- Inocentes: {TOTAL_INOCENTES}")
    print("- Alcalde: 1")

    print("\nREGLAS:")
    print("- Tienes 2 preguntas por sospechoso.")
    print("- Debes decidir si liberar o capturar.")
    print("- Si dejas escapar a un impostor, pierdes.")
    print("- Si capturas al alcalde, pierdes.")
    print("- Si capturas a los 5 inocentes, pierdes.")
    print("- Debes capturar a los 4 impostores para ganar.")

    input("\nPresiona ENTER para comenzar...")

    # =========================================
    # PROCESAR SOSPECHOSOS
    # =========================================

    for personaje in sospechosos:

        # Crear una IA independiente para cada persona.
        ia = InterrogatorioIA(personaje, caso)

        decision = interrogar(personaje, ia)

        # -------------------------------------
        # CAPTURAR
        # -------------------------------------

        if decision == "capturado":

            capturados.append(personaje)

            print(
                f"\n{personaje['nombre']} "
                "ha sido detenido."
            )

            # Capturar al alcalde = derrota.
            if personaje["rol"] == "Alcalde":

                print("\n¡CAPTURASTE AL ALCALDE!")
                print("¡DERROTA INSTANTÁNEA!")

                derrota = True
                break

            # Capturar a un inocente.
            elif personaje["rol"] == "Inocente":

                inocentes_capturados += 1

                print("\nEra una persona inocente.")

                print(
                    f"Inocentes capturados: "
                    f"{inocentes_capturados}/5"
                )

                if inocentes_capturados == TOTAL_INOCENTES:

                    print("\n¡CAPTURASTE A LOS 5 INOCENTES!")
                    print("¡DERROTA!")

                    derrota = True
                    break

            # Capturar a un impostor.
            elif personaje["rol"] == "Impostor":

                impostores_capturados += 1

                print("\n¡IMPOSTOR CAPTURADO!")

                print(
                    f"Impostores capturados: "
                    f"{impostores_capturados}/4"
                )

                # Capturar los 4 impostores = victoria.
                if impostores_capturados == TOTAL_IMPOSTORES:

                    print("\n¡ENCONTRASTE A LOS 4 IMPOSTORES!")
                    print("¡VICTORIA!")

                    victoria = True
                    break

        # -------------------------------------
        # LIBERAR
        # -------------------------------------

        else:

            liberados.append(personaje)

            print(
                f"\n{personaje['nombre']} "
                "ha sido liberado."
            )

            # Dejar escapar a un impostor = derrota.
            if personaje["rol"] == "Impostor":

                print("\n¡DEJASTE ESCAPAR A UN IMPOSTOR!")
                print("¡DERROTA!")

                derrota = True
                break

            else:

                print("La persona no era un impostor.")

    # =========================================
    # RESULTADO FINAL
    # =========================================

    if not derrota and not victoria:

        if impostores_capturados == TOTAL_IMPOSTORES:

            victoria = True

        else:

            derrota = True

    print("\n" + "=" * 55)

    if victoria:

        print("             ¡HAS GANADO!")
        print("Capturaste a los 4 impostores.")

    elif derrota:

        print("             HAS PERDIDO")
        print("No lograste completar el operativo.")

    print("=" * 55)

    mostrar_resultados(
        sospechosos,
        capturados,
        liberados,
        impostores_capturados,
        inocentes_capturados
    )


# =============================================
# EJECUCIÓN
# =============================================

if __name__ == "__main__":
    jugar()
