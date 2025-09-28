'''
Escribe un programa que pida un número al usuario e imprima si el número está en uno de los siguientes rangos:
Menor que 0.
Entre 0 y 10.
Mayor que 10.

'''
numero = input("Introduce un numero: ")
while True:
    entrada = input("Introduce un numero: ")
    try:
        numero = int(entrada)
        break
    except ValueError:
        print("Error: Por favor, introduce un número entero válido.")
        print("Error: Por favor, introduce un número entero válido.") # Se mantiene el manejo de errores

if numero < 0:
    print("Numero menor que cero")
elif numero >= 0 and numero <= 10:
    print("Numero entre 0 y 10")
else:
    print("Numero mayor que 10")
    print(f"{numero} es menor que cero")
