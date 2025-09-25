'''
Pide una cadena y dos caracteres por teclado (valida que sea un carácter), sustituye la aparición del primer carácter en la cadena por el segundo carácter. 
'''

cadena = input("Introduce una cadena: ")

caracter1 = input("Introduce un carácter a sustituir: ")
while len(caracter1) != 1:
    caracter1 = input("Introduce un carácter válido: ")

caracter2 = input("Introduce carácter para la sustitución: ")  
while len(caracter2) != 1:
    caracter2 = input("Introduce un carácter válido: ")

print(cadena.replace(caracter1, caracter2))
