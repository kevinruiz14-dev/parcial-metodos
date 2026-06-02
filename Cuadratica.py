import numpy as np

def calcular(t_vals, y_vals):
    n = len(t_vals)
    t  = np.array(t_vals, dtype=float)
    y  = np.array(y_vals, dtype=float)

    St   = np.sum(t)
    St2  = np.sum(t**2)
    St3  = np.sum(t**3)
    St4  = np.sum(t**4)
    Sy   = np.sum(y)
    Sty  = np.sum(t * y)
    St2y = np.sum(t**2 * y)

    M = np.array([
        [n,   St,  St2],
        [St,  St2, St3],
        [St2, St3, St4],
    ])
    b = np.array([Sy, Sty, St2y])
    A, B, C = np.linalg.solve(M, b)

    return {
        "tipo": "Cuadrática",
        "A": A, "B": B, "C": C,
        "ecuaciones": [
            f"{n}A + {St:.4f}B + {St2:.4f}C = {Sy:.4f}",
            f"{St:.4f}A + {St2:.4f}B + {St3:.4f}C = {Sty:.4f}",
            f"{St2:.4f}A + {St3:.4f}B + {St4:.4f}C = {St2y:.4f}",
        ],
        "t": t, "y": y,
    }

def proyectar(resultado, t_nuevo):
    A, B, C = resultado["A"], resultado["B"], resultado["C"]
    return A + B * t_nuevo + C * t_nuevo**2

def ecuacion_str(resultado):
    A, B, C = resultado["A"], resultado["B"], resultado["C"]
    sb = "+" if B >= 0 else "-"
    sc = "+" if C >= 0 else "-"
    return f"Y = {A:.4f} {sb} {abs(B):.4f}·t {sc} {abs(C):.4f}·t²"