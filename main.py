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
    t_vals, y_vals = [], []
    for i in range(n):
        while True:
            try:
                t = float(input(f"  Dato {i+1} → t: "))
                y = float(input(f"  Dato {i+1} → Y: "))
                t_vals.append(t)
                y_vals.append(y)
                break
            except ValueError:
                print("  ⚠ Ingresa un número válido.")
    return t_vals, y_vals

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
            t_nuevo = float(input("  Ingresa el valor de t a proyectar: "))
            break
        except ValueError:
            print("  ⚠ Ingresa un número válido.")
    y_proj = mod.proyectar(resultado, t_nuevo)
    print(f"  Para t = {t_nuevo}  →  Y ≈ {y_proj:.6f}")

def ejecutar(mod, t_vals, y_vals):
    try:
        resultado = mod.calcular(t_vals, y_vals)
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
    print("  [0] Salir")
    print("─" * 40)
    return input("  Elige una opción: ").strip()

def main():
    t_vals, y_vals = None, None
    while True:
        opcion = menu()
        if opcion == "0":
            print("\n  ¡Hasta luego!\n")
            break
        if opcion not in ("1", "2", "3"):
            print("  ⚠ Opción inválida.")
            continue
        if t_vals is not None:
            reusar = input("\n  ¿Usar los mismos datos? (s/n): ").strip().lower()
            if reusar != "s":
                t_vals, y_vals = ingresar_datos()
        else:
            t_vals, y_vals = ingresar_datos()
        if opcion == "1":
            ejecutar(lineal, t_vals, y_vals)
        elif opcion == "2":
            ejecutar(cuadratica, t_vals, y_vals)
        elif opcion == "3":
            ejecutar(exponencial, t_vals, y_vals)
        input("\n  Presiona Enter para continuar...")

if __name__ == "__main__":
    main()