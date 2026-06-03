import numpy as np
import matplotlib.pyplot as plt

COLORES = {
    "Lineal":      "#2196F3",
    "Cuadrática": "#9C27B0",
    "Exponencial": "#F44336",
}

def graficar(resultado, modulo):
    x_datos = resultado.get("x", resultado.get("t"))
    y_datos = resultado["y"]
    tipo    = resultado["tipo"]
    color   = COLORES.get(tipo, "#333333")

    x_min = min(x_datos) - 0.5
    x_max = max(x_datos) + 0.5
    x_curva = np.linspace(x_min, x_max, 400)
    y_curva = np.array([modulo.proyectar(resultado, xv) for xv in x_curva])

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(x_curva, y_curva, color=color, linewidth=2.5,
            label=f"Curva: {modulo.ecuacion_str(resultado)}")

    ax.scatter(x_datos, y_datos, color="#212121", zorder=5,
               s=60, label="Datos originales")

    for xi, yi in zip(x_datos, y_datos):
        ax.annotate(f"({xi:.2g}, {yi:.2g})",
                    (xi, yi), textcoords="offset points",
                    xytext=(6, 6), fontsize=8, color="#444")

    ax.set_title(f"Regresión {tipo}", fontsize=14, fontweight="bold")
    ax.set_xlabel("X", fontsize=12)
    ax.set_ylabel("Y", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.show()