'''
Escribe un programa que pida una cadena al usuario y la convierta a:
Mayúsculas si la cadena tiene más de 10 caracteres.
Minúsculas si tiene 10 o menos caracteres.

'''

cadena = input("Introduce una cadena: ")

if len(cadena) > 10:
    print(cadena.upper())
else:
    print(cadena.lower())