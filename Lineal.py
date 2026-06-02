import numpy as np

def calcular(t_vals, y_vals):
    n = len(t_vals)
    t  = np.array(t_vals, dtype=float)
    y  = np.array(y_vals, dtype=float)

    St  = np.sum(t)
    St2 = np.sum(t**2)
    Sy  = np.sum(y)
    Sty = np.sum(t * y)

    M = np.array([[n,  St],
                  [St, St2]])
    b = np.array([Sy, Sty])
    A, B = np.linalg.solve(M, b)

    return {
        "tipo": "Lineal",
        "A": A, "B": B,
        "ecuaciones": [
            f"{n}A + {St:.4f}B = {Sy:.4f}",
            f"{St:.4f}A + {St2:.4f}B = {Sty:.4f}",
        ],
        "t": t, "y": y,
    }

def proyectar(resultado, t_nuevo):
    return resultado["A"] + resultado["B"] * t_nuevo

def ecuacion_str(resultado):
    A, B = resultado["A"], resultado["B"]
    signo = "+" if B >= 0 else "-"
    return f"Y = {A:.4f} {signo} {abs(B):.4f}·t"