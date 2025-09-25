'''
Escribe un programa que simule una calculadora. El programa debe pedir al usuario dos números y una operación (+, -, *, /) y realizar el cálculo correspondiente. vuelve a empezar para hacer otra operación hasta que el usuario pulse s para salir.
'''

def calculo(num1, num2, operacion):
    if operacion == "+":
        return num1 + num2
    elif operacion == "-":
        return num1 - num2
    elif operacion == "*":
        return num1 * num2
    elif operacion == "/":
        if num2 == 0:
            print("Error: No se puede dividir por cero.")
            return None
        return num1 / num2
    print("Operación no válida.")
    return None 

try:
    resultado_actual = float(input("Introduce el número inicial: "))
except ValueError:
    print("Error: Debes empezar con un número válido. Reiniciando...")
    resultado_actual = 0

while True:
    
    operacion = input("Introduce una operación (+, -, *, /) o 's' para salir: ")

    if operacion.lower() == 's':
        print(f"Resultado final: {resultado_actual}.")
        break
    
    if operacion not in ["+", "-", "*", "/"]:
        print("Error: Operación no válida.")
        continue

    try:
        num_2 = float(input("Introduce el siguiente número: "))
    except ValueError:
        print("Error: Introduce un número válido.")
        continue

    nuevo_resultado = calculo(resultado_actual, num_2, operacion)

    
    if nuevo_resultado is None:
        print("Se ha producido un error en el cálculo. Reinicia la calculadora.")
        break
    
    
    resultado_actual = nuevo_resultado
    print(f"= {resultado_actual}")
