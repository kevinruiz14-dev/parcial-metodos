import numpy as np

def calcular(x_vals, y_vals):
    n  = len(x_vals)
    x  = np.array(x_vals, dtype=float)
    y  = np.array(y_vals, dtype=float)

    if np.any(y <= 0):
        raise ValueError("La regresión exponencial requiere Y > 0 en todos los datos.")

    lny   = np.log(y)
    Sx    = np.sum(x)
    Sx2   = np.sum(x**2)
    Slny  = np.sum(lny)
    Sxlny = np.sum(x * lny)

    M = np.array([[n,  Sx ],
                  [Sx, Sx2]])
    b = np.array([Slny, Sxlny])
    A_prima, B = np.linalg.solve(M, b)
    A = np.exp(A_prima)

    return {
        "tipo": "Exponencial",
        "A": A, "B": B, "A_prima": A_prima,
        "ecuaciones": [
            f"(linealizado)  {n}A' + {Sx:.4f}B = {Slny:.4f}",
            f"(linealizado)  {Sx:.4f}A' + {Sx2:.4f}B = {Sxlny:.4f}",
        ],
        "nota": f"A = e^(A') = e^({A_prima:.4f}) = {A:.4f}",
        "x": x, "y": y,
    }

def proyectar(resultado, x_nuevo):
    return resultado["A"] * np.exp(resultado["B"] * x_nuevo)

def ecuacion_str(resultado):
    A, B = resultado["A"], resultado["B"]
    return f"Y = {A:.4f}·e^({B:.4f}·X)"