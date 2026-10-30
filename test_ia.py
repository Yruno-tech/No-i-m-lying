from personajes import generar_personajes
from casos import generar_caso
from relaciones import generar_relaciones
from ia import InterrogatorioIA

caso = generar_caso()
personajes = generar_personajes(caso)

generar_relaciones(personajes)

print("\nCASO:")
print(caso["titulo"])
print(caso["incidente"])

print("\nPERSONAJES Y SUS UBICACIONES REALES:")

for p in personajes:
    print(
        f"{p['nombre']}: "
        f"{p['datos_reales']['lugar']} "
        f"a las {p['datos_reales']['hora']}"
    )

print("\n" + "=" * 55)
print("INFORMACIÓN INTERNA DE LOS SOSPECHOSOS")
print("=" * 55)

for personaje in personajes:

    print(f"\nPERSONAJE: {personaje['nombre']}")

    print("\nRELACIONES:")
    for relacion in personaje["relaciones"]:
        print(
            f"- {relacion['personaje']}: "
            f"{relacion['vinculo']} "
            f"(Confianza: {relacion['confianza']})"
        )

    print("\nCONOCIMIENTOS:")
    for conocimiento in personaje["conocimientos"]:
        print(f"- {conocimiento['informacion']}")

    print("\nSECRETO:")
    print(personaje["secreto"])
