'''
Realizar un programa que dada una cadena de caracteres por caracteres, genere otra cadena resultado de invertir la primera. 
'''

# caracter = input("Introduce un carácter(enter para terminar): ")
# cadena = []
# while caracter != "":
#     cadena.append(caracter)
#     caracter = input("Introduce un carácter: ")

# print("".join(cadena[::-1]))


cadena = ""
caracter = input("Introduce un caracter (enter para terminar): ")
while caracter != "":
    if len(caracter) == 1:
        cadena += caracter
        caracter = input("Introduce un carácter: ")
    
print(cadena[::-1])