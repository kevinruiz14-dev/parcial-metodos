import numpy as np

def calcular(t_vals, y_vals):
    n  = len(t_vals)
    t  = np.array(t_vals, dtype=float)
    y  = np.array(y_vals, dtype=float)

    if np.any(y <= 0):
        raise ValueError("La regresión exponencial requiere Y > 0 en todos los datos.")

    lny   = np.log(y)
    St    = np.sum(t)
    St2   = np.sum(t**2)
    Slny  = np.sum(lny)
    Stlny = np.sum(t * lny)

    M = np.array([[n,  St ],
                  [St, St2]])
    b = np.array([Slny, Stlny])
    A_prima, B = np.linalg.solve(M, b)
    A = np.exp(A_prima)

    return {
        "tipo": "Exponencial",
        "A": A, "B": B, "A_prima": A_prima,
        "ecuaciones": [
            f"(linealizado)  {n}A' + {St:.4f}B = {Slny:.4f}",
            f"(linealizado)  {St:.4f}A' + {St2:.4f}B = {Stlny:.4f}",
        ],
        "nota": f"A = e^(A') = e^({A_prima:.4f}) = {A:.4f}",
        "t": t, "y": y,
    }

def proyectar(resultado, t_nuevo):
    return resultado["A"] * np.exp(resultado["B"] * t_nuevo)

def ecuacion_str(resultado):
    A, B = resultado["A"], resultado["B"]
    return f"Y = {A:.4f}·e^({B:.4f}·t)"