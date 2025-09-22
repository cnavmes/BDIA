#Escribe un programa que pida al usuario un número e imprima si es positivo o negativo.

while True:
    entrada = input("Introduce un numero: ")
    try:
       
        numero = int(entrada)
        
        break
    except ValueError:
        
        print("Error: Por favor, introduce un número válido.")
 
if numero == 0:
    print("Has introducido un cero")
elif numero > 0:
    print(f"{numero} es positivo")
else:
    print(f"{numero} es negativo")

