'''
Suponiendo que hemos introducido una cadena por teclado que representa una frase (palabras separadas por espacios), realiza un programa que cuente cuántas palabras tiene. 
'''

cadena = input("Introduce una cadena: ")

palabras = cadena.split()

print(f"La cadena '{cadena}' tiene {len(palabras)} palabras.")