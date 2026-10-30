
from personajes import generar_personajes
from relaciones import generar_relaciones


personajes = generar_personajes()

generar_relaciones(personajes)


for personaje in personajes:

    print("\n" + "=" * 50)
    print(f"PERSONAJE: {personaje['nombre']}")
    print("=" * 50)

    print("\nRELACIONES:")

    for relacion in personaje["relaciones"]:

        print(
            f"- {relacion['personaje']}: "
            f"{relacion['vinculo']} "
            f"(Confianza: {relacion['confianza']})"
        )

    print("\nCONOCIMIENTOS:")

    for conocimiento in personaje["conocimientos"]:

        print(
            f"- {conocimiento['informacion']}"
        )

    print("\nSECRETO:")
    print(personaje["secreto"])
