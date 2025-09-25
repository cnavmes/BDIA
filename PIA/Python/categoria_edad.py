'''
Escribe un programa que pida la edad del usuario y determine en qué categoría se encuentra:
Niño: Menor de 12 años.
Adolescente: Entre 12 y 18 años.
Adulto: Mayor de 18 años.

'''

while True:
    try:
        entrada = int(input("Introduce tu edad"))
        if entrada < 12:
            print("Eres un niño")
        elif entrada >= 12 and entrada <= 18:
            print("Eres adolescente")
        else:
            print("Eres adulto")
        break
    except ValueError:
        print("Introduce una edad válida")
            
