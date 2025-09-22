#Escribe un programa que pida al usuario dos números y muestre cuál de ellos es mayor o si son iguales.

numeros:list[int] = []

for i in range(2):
    while True:
        entrada = input(f"Introduce el numero {i+1}: ")
        try:
            numero = int(entrada)
            numeros.append(numero)
            break
        except ValueError:
            print("Error: Por favor, introduce un número válido.")

if numeros[0] == numeros[1]:
    print("Los numeros son iguales")
elif numeros[0] > numeros[1]:
    print(f"{numeros[0]} es mayor que {numeros[1]}")
else:
    print(f"{numeros[1]} es mayor que {numeros[0]}")