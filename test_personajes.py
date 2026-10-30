from personajes import generar_personajes
from ia import InterrogatorioIA

personajes = generar_personajes()

personaje = personajes[0]

print("Personaje:", personaje["nombre"])
print("Personalidad:", personaje["personalidad"])
print("Debe decir verdad:", personaje["dice_verdad"])

ia = InterrogatorioIA(personaje)

print("\nEnviando pregunta...")

respuesta = ia.preguntar(
    "¿Dónde estabas durante el incidente?"
)

print("\nRESPUESTA FINAL:")
print(repr(respuesta))