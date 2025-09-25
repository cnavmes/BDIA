#Escribe un programa que verifique si la longitud de una cadena ingresada por el usuario es mayor a 5 caracteres.

cadena = input("Introduce una cadena: ")

if len(cadena) > 5:
    print("La cadena tiene mas de 5 caracteres")
else:
    print("La cadena tiene menos de 5 caracteres")  
    print("La cadena tiene 5 caracteres o menos")