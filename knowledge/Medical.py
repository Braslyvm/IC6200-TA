from logic import And, Not, Implication, Or, Symbol, Biconditional, model_check, Xor




# Síntomas
Fiebre = Symbol("Fiebre")
Tos = Symbol("Tos")
Sarpullido = Symbol("Sarpullido")

# Diagnósticos
Posible_Gripe = Symbol("Posible_Gripe")
Posible_Sarampion = Symbol("Posible_Sarampion")

# Acciones médicas
Prescribir_Antiviral = Symbol("Prescribir_Antiviral")
Prescribir_Aislamiento = Symbol("Prescribir_Aislamiento")
Ordenar_Examen_Sangre = Symbol("Ordenar_Examen_Sangre")
Notificar_Salud_Publica = Symbol("Notificar_Salud_Publica")


# Base de conocimiento
Diagnostico = And()

Diagnostico.add(
    Implication(
        And(Fiebre, Tos),
        Posible_Gripe
    )
)

Diagnostico.add(
    Implication(
        And(Fiebre, Sarpullido),
        Posible_Sarampion
    )
)

Diagnostico.add(
    Implication(
        Posible_Gripe,
        Prescribir_Antiviral
    )
)

Diagnostico.add(
    Implication(
        Posible_Sarampion,
        Prescribir_Aislamiento
    )
)

Diagnostico.add(
    Implication(
        And(Fiebre, Not(Tos), Not(Sarpullido)),
        Ordenar_Examen_Sangre
    )
)

Diagnostico.add(
    Implication(
        Prescribir_Aislamiento,
        Notificar_Salud_Publica
    )
)


# Facts
Diagnostico.add(Fiebre)
Diagnostico.add(Sarpullido)
Diagnostico.add(Not(Tos))


print("========== PROBLEM 1: MEDICAL DIAGNOSIS ==========")

print("Diagnósticos:")
print(f"Posible gripe: {model_check(Diagnostico, Posible_Gripe)}")
print(f"Posible sarampión: {model_check(Diagnostico, Posible_Sarampion)}")

print("\nAcciones médicas:")
print(f"Prescribir antiviral: {model_check(Diagnostico, Prescribir_Antiviral)}")
print(f"Prescribir aislamiento: {model_check(Diagnostico, Prescribir_Aislamiento)}")
print(f"Ordenar examen de sangre: {model_check(Diagnostico, Ordenar_Examen_Sangre)}")
print(f"Notificar salud pública: {model_check(Diagnostico, Notificar_Salud_Publica)}")


print("\nConclusiones:")

if model_check(Diagnostico, Posible_Sarampion):
    print("El diagnóstico derivado es posible sarampión.")

if model_check(Diagnostico, Posible_Gripe):
    print("El diagnóstico derivado es posible gripe.")

if model_check(Diagnostico, Prescribir_Aislamiento):
    print("La acción médica recomendada es prescribir aislamiento.")

if model_check(Diagnostico, Prescribir_Antiviral):
    print("La acción médica recomendada es prescribir antiviral.")

if model_check(Diagnostico, Notificar_Salud_Publica):
    print("Sí se debe notificar a las autoridades de salud pública.")
else:
    print("No se debe notificar a las autoridades de salud pública.")



Diagnostico_Corroborado = And()

Diagnostico_Corroborado.add(
    Implication(
        And(Fiebre, Tos),
        Posible_Gripe
    )
)

Diagnostico_Corroborado.add(
    Implication(
        And(Fiebre, Sarpullido),
        Posible_Sarampion
    )
)

Diagnostico_Corroborado.add(
    Implication(
        Posible_Gripe,
        Prescribir_Antiviral
    )
)

Diagnostico_Corroborado.add(
    Implication(
        Posible_Sarampion,
        Prescribir_Aislamiento
    )
)

Diagnostico_Corroborado.add(
    Implication(
        And(Fiebre, Not(Tos), Not(Sarpullido)),
        Ordenar_Examen_Sangre
    )
)

Diagnostico_Corroborado.add(
    Implication(
        Prescribir_Aislamiento,
        Notificar_Salud_Publica
    )
)

# Nuevos hechos
Diagnostico_Corroborado.add(Fiebre)
Diagnostico_Corroborado.add(Not(Tos))
Diagnostico_Corroborado.add(Not(Sarpullido))



print(f"Posible sarampión: {model_check(Diagnostico_Corroborado, Posible_Sarampion)}")
print(f"Prescribir aislamiento: {model_check(Diagnostico_Corroborado, Prescribir_Aislamiento)}")
print(f"Ordenar examen de sangre: {model_check(Diagnostico_Corroborado, Ordenar_Examen_Sangre)}")
print(f"Notificar salud pública: {model_check(Diagnostico_Corroborado, Notificar_Salud_Publica)}")

if model_check(Diagnostico_Corroborado, Ordenar_Examen_Sangre):
    print("El diagnóstico cambia: ya no se deriva sarampión y ahora se debe ordenar un examen de sangre.")