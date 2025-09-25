'''
 Realizar un programa que comprueba si una cadena leída por teclado comienza por una subcadena introducida por teclado. 
'''

subcadena = input("Introduce una subcadena: ")
cadena = input("Introduce una cadena: ")

if cadena.startswith(subcadena):
    print(f"{subcadena} es una subcadena de {cadena}")
else:
    print(f"{subcadena} no es una subcadena de {cadena}")