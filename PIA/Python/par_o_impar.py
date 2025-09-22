#Escribe un programa que determine si un número ingresado por el usuario es par o impar.

while True:
    entrada = input("Introduce un numero: ")
    try:
        numero = int(entrada)
        break
    except ValueError:
        print("Error: introduce un número válido.")  

if numero % 2 == 0:
    print(f"{numero} es par")
else:
    print(f"{numero} es impar")

