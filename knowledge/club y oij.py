from logic import And, Not, Implication, Or, Symbol, Biconditional, model_check



Sala_Servidores = Symbol("Sala_Servidores")
Sala_Reuniones = Symbol("Sala_Reuniones")
Targeta_Empleado = Symbol("Targeta_Empleado")
Codigo = Symbol("Codigo")
Visitante_Registrado = Symbol("Visitante_Registrado")
Modo_Emergencia = Symbol("Modo_Emergencia")
Alerta = Symbol("Alerta")





# knowledge
ana = And()


ana.add(
    Implication(
        And(Targeta_Empleado, Codigo), Sala_Servidores
    )
)

ana.add(
    Implication(
        Or(Targeta_Empleado,Visitante_Registrado),
        Sala_Reuniones

    )
)


ana.add(
    Implication(Visitante_Registrado,Not(Sala_Servidores))
)


ana.add(
    Implication(Modo_Emergencia,And(Sala_Servidores,Sala_Reuniones))
)

ana.add(
    Implication(Alerta,Not(Modo_Emergencia))
)






# Si no llovió, Harry visitó a Hagrid hoy
ana.add(Targeta_Empleado)
ana.add(Not(Codigo))
ana.add(Not(Modo_Emergencia))



if model_check(ana, Sala_Servidores):
    print(f"Ana puede entrar a la sala de servidores")
else:
    print(f"Ana no puede entrar a la sala de servidores")



if model_check(ana, Sala_Reuniones):
    print(f"Ana puede entrar a la sala de reuniones")
else:
    print(f"Ana no puede entrar a la sala de reuniones")


ana.add(Alerta)

if model_check(ana, Sala_Servidores):
    print(f"se cambio el acceso de servidores de ana")
else:
    print(f"no se cambio el acceso de servidores de ana")




# knowledge
Crimen = And()


ColMustard=Symbol("ColMustard")
ProfPlum = Symbol("ProfPlum")
Sra_Scarlet = Symbol("Sra_Scarlet")


salón_baile = Symbol("salón_baile")
cocina = Symbol("cocina")
biblioteca  = Symbol("biblioteca")

cuchillo = Symbol("cuchillo")   
revólver = Symbol("revólver")
llave_inglesa = Symbol("llave_inglesa")

Crimen.add (Or(ColMustard, ProfPlum, Sra_Scarlet))

Crimen.add(Or(salón_baile, cocina , biblioteca))

Crimen.add (Or(cuchillo, revólver , llave_inglesa))

Crimen.add (Not(ColMustard))
Crimen.add(Not(cocina))
Crimen.add(Not(revólver))



Crimen.add(
    Implication(
        And(Sra_Scarlet,biblioteca), Not(llave_inglesa)
    )

)


Crimen.add(
    Implication(
        And(Sra_Scarlet,llave_inglesa), Not(biblioteca)
    )

)

Crimen.add(
    Implication(
        And(biblioteca,llave_inglesa), Not(Sra_Scarlet)
    )
)

Crimen.add(Not(ProfPlum))
Crimen.add(Not(salón_baile))


print("==========================")

print("Los simbolos")
print("==========================")

print(f"ProfPlum: {model_check(Crimen, ProfPlum)}")
print(f"ColMustard: {model_check(Crimen, ColMustard)}")
print(f"Sra_Scarlet: {model_check(Crimen, Sra_Scarlet)}")
print(f"salón_baile: {model_check(Crimen, salón_baile)}")
print(f"cocina: {model_check(Crimen, cocina)}")
print(f"biblioteca: {model_check(Crimen, biblioteca)}")
print(f"cuchillo: {model_check(Crimen, cuchillo)}")
print(f"revólver: {model_check(Crimen, revólver)}") 
print(f"llave_inglesa: {model_check(Crimen, llave_inglesa)}")

print("==========================")
for x in [ProfPlum, ColMustard, Sra_Scarlet]:
    if model_check(Crimen, x):
        print(f"El asesino es {x}")

for x in [cocina, salón_baile, biblioteca]:
    if model_check(Crimen, x):
        print(f"El asesinato fue en la {x}")


for x in [cuchillo, revólver, llave_inglesa]:
    if model_check(Crimen, x):
        print(f"El asesino uso {x}")


print("==========================")

for x in Crimen.conjuncts:
    if model_check(Crimen, x):
        print(f"{x} es verdadero")













