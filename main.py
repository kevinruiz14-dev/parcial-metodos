import lineal
import cuadratica
import exponencial
import grafico

def ingresar_datos():
    print("\n" + "─" * 40)
    print("  INGRESO DE DATOS")
    print("─" * 40)
    while True:
        try:
            n = int(input("  ¿Cuántos pares de datos vas a ingresar? "))
            if n < 2:
                print("  ⚠ Necesitas al menos 2 datos.")
                continue
            break
        except ValueError:
            print("  ⚠ Ingresa un número entero.")
    x_vals, y_vals = [], []
    for i in range(n):
        while True:
            try:
                x = float(input(f"  Dato {i+1} → X: "))
                y = float(input(f"  Dato {i+1} → Y: "))
                x_vals.append(x)
                y_vals.append(y)
                break
            except ValueError:
                print("  ⚠ Ingresa un número válido.")
    return x_vals, y_vals

def mostrar_ecuaciones(resultado):
    print("\n  SISTEMA DE ECUACIONES:")
    for eq in resultado["ecuaciones"]:
        print(f"  {eq}")
    if "nota" in resultado:
        print(f"  {resultado['nota']}")
    tipo = resultado["tipo"]
    if tipo == "Lineal":
        print(f"\n  {lineal.ecuacion_str(resultado)}")
    elif tipo == "Cuadrática":
        print(f"\n  {cuadratica.ecuacion_str(resultado)}")
    elif tipo == "Exponencial":
        print(f"\n  {exponencial.ecuacion_str(resultado)}")

def hacer_proyeccion(resultado, mod):
    print("\n  PROYECCIÓN:")
    while True:
        try:
            x_nuevo = float(input("  Ingresa el valor de X a proyectar: "))
            break
        except ValueError:
            print("  ⚠ Ingresa un número válido.")
    y_proj = mod.proyectar(resultado, x_nuevo)
    print(f"  Para X = {x_nuevo}  →  Y ≈ {y_proj:.6f}")

def ejecutar(mod, x_vals, y_vals):
    try:
        resultado = mod.calcular(x_vals, y_vals)
        resultado["x"] = resultado.get("x", resultado.get("t", x_vals))
    except ValueError as e:
        print(f"\n  ⚠ Error: {e}")
        return
    mostrar_ecuaciones(resultado)
    hacer_proyeccion(resultado, mod)
    grafico.graficar(resultado, mod)

def menu():
    print("\n" + "=" * 40)
    print("   SISTEMA DE REGRESIÓN NUMÉRICA")
    print("=" * 40)
    print("  [1] Regresión Lineal")
    print("  [2] Regresión Cuadrática")
    print("  [3] Regresión Exponencial")
    print("  [4] Cambiar datos")
    print("  [0] Salir")
    print("─" * 40)
    return input("  Elige una opción: ").strip()

def main():
    print("\n" + "=" * 40)
    print("   SISTEMA DE REGRESIÓN NUMÉRICA")
    print("=" * 40)
    
    x_vals, y_vals = ingresar_datos()

    while True:
        opcion = menu()
        if opcion == "0":
            print("\n  ¡Hasta luego!\n")
            break
        if opcion not in ("1", "2", "3", "4"):
            print("  ⚠ Opción inválida.")
            continue
        if opcion == "4":
            x_vals, y_vals = ingresar_datos()
            continue

        if opcion == "1":
            ejecutar(lineal, x_vals, y_vals)
        elif opcion == "2":
            ejecutar(cuadratica, x_vals, y_vals)
        elif opcion == "3":
            ejecutar(exponencial, x_vals, y_vals)
        input("\n  Presiona Enter para continuar...")

if __name__ == "__main__":
    main()