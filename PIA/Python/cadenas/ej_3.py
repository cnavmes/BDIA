'''
Pide una cadena y un carácter por teclado (valida que sea un carácter) y muestra cuantas veces aparece el carácter en la cadena. 
'''

cadena = input("Introduce una cadena: ")
caracter = input("Introduce un carácter: ")

if len(caracter) == 1 and caracter.isalpha():
    print(f"El carácter '{caracter}' aparece {cadena.count(caracter)} veces en la cadena '{cadena}'.")
else:
    print("El carácter introducido no es válido.")

    