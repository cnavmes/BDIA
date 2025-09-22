#Escribe un programa que pida una palabra al usuario y verifique si es un palíndromo (se lee igual hacia adelante que hacia atrás).

palabra = input("Introduce una palabra: ")

if palabra == palabra[::-1]:
    print(f"{palabra} es un palindromo")
else:
    print(f"{palabra} no es un palindromo") 