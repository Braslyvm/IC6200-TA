from logic import And, Not, Implication, Or, Symbol, Biconditional, model_check



print("Ejemplo")
# Symbols
# "Rain"
# "Hagrid"
# "Dumbledore"
rain = Symbol("Rain")
hagrid = Symbol("Hagrid")
dumbledore = Symbol("Dumbledore")

# knowledge
knowledge1 = And()


# Si no llovió, Harry visitó a Hagrid hoy
knowledge1.add(Implication(Not(rain),hagrid))

# Harry visitó a Hagrid o a Dumbledore hoy, pero no a ambos
knowledge1.add(
    Or( And (hagrid,Not(dumbledore)), And (Not(hagrid),dumbledore))
)

# Harry visitó a Dumbledore hoy
knowledge1.add(dumbledore)

# print(f"Rain: {model_check(knowledge, rain)}")
print(f"Hagrid: {model_check(knowledge1, hagrid)}")
print(f"Rain: {model_check(knowledge1, rain)}")
print(f"Dumbledore: {model_check(knowledge1, dumbledore)}")
# print(f"Hagrid: {model_check(knowledge, hagrid)}")
# print(f"Dumbledore: {model_check(knowledge, dumbledore)}")



"""
## 1. Si estudio o hago tareas, entonces paso el curso, pero si no estudio, no paso.
"""

print("")
print("")
print("")
print("1. Si estudio o hago tareas, entonces paso el curso, pero si no estudio, no paso.lo")
print("")

estudio = Symbol("Estudio")
tarea = Symbol("Tarea")
curso  = Symbol("Curso")

knowledge2 = And()

knowledge2.add(
    And(
        Implication(
            Or(
                estudio, tarea
            ),
            curso
        )
        ,
        Implication(
            Not(estudio), Not(curso)
        )
    )
)


knowledge2.add(estudio)


if model_check(knowledge2, curso):
    print(f"paso el curso")
else:
    print(f"no paso el curso")




print("")
print("")
print("2. Si estudio, entonces si hago tareas paso el curso.")
print("")



estudio = Symbol("Estudio")
tarea = Symbol("Tarea")
curso  = Symbol("Curso")

knowledge3 = And()

knowledge3.add(
        Implication(
            estudio
            ,
            Implication(
                tarea,curso
            )
        )
    )

knowledge3.add(And(estudio,tarea))



if model_check(knowledge3, curso):
    print(f"paso el curso")
else:
    print(f"no paso el curso")






print("")
print("")
print("3. Voy al cine si y solo si termino la tarea y no estoy cansado.")
print("")



cine = Symbol("Cine")
tarea = Symbol("Tarea")
cansado  = Symbol("Cansado")

knowledge4 = And()
knowledge4.add(
        Biconditional(
            cine
            ,
            And(
                tarea, Not(cansado)
            )
        )
    )

knowledge4.add(tarea)
knowledge4.add(Not(cansado))


if model_check(knowledge4, cine):
    print(f"voy al cine ")
else:
    print(f"no voy al cine ")





print("")
print("")

print("4. Si el sistema responde y no hay timeout, entonces la transacción se procesa; de lo contrario, falla.")
print("")

sistema = Symbol("Sistema")
timeout = Symbol("Timeout")
transacciones  = Symbol("Transacciones")

knowledge5 = And()
knowledge5.add(
        Biconditional(

            Implication(
                And(sistema , Not(transacciones)),
                transacciones
            )
            
            , 
            Not(transacciones)

        )
    )

knowledge5.add(sistema)
knowledge5.add(Not(timeout))


if model_check(knowledge5, transacciones):
    print(f"la transacción se procesa ")
else:
    print(f"la transacción falla")


print("")
print("")
print("## 5. No es cierto que si estudio entonces paso.")
print("")

estudio = Symbol("estudio")
paso = Symbol("paso")
knowledge6 = And()
knowledge6.add(
        Not (
            Implication(
                estudio , paso
            )
        )
    )

if model_check(knowledge6, estudio):
    print(f"estudio")
else:
    print(f"no estudio")

if model_check(knowledge6, paso):
    print(f"paso")
else:
    print(f"no paso")
