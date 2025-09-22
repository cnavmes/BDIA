


def longitud_valida(cadena, longitud_minima = 8):
    return len(cadena) >= longitud_minima

def comprobar_mayuscula(cadena):
    for caracter in cadena:
        if caracter.isupper():
            return True
    return False

def comprobar_numero(cadena):
    for caracter in cadena:
        if caracter.isdigit():
            return True
    return False



while True:
    cadena = input("Introduce una contraseña valida: ")
    if longitud_valida(cadena) and comprobar_mayuscula(cadena) and comprobar_numero(cadena):
        print("Contraseña valida")
        break
    else:
        print("Contraseña invalida")
    

    