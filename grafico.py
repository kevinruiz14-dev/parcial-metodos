import numpy as np
import matplotlib.pyplot as plt

COLORES = {
    "Lineal":      "#2196F3",
    "Cuadrática": "#9C27B0",
    "Exponencial": "#F44336",
}

def graficar(resultado, modulo):
    t_datos = resultado["t"]
    y_datos = resultado["y"]
    tipo    = resultado["tipo"]
    color   = COLORES.get(tipo, "#333333")

    t_min = min(t_datos) - 0.5
    t_max = max(t_datos) + 0.5
    t_curva = np.linspace(t_min, t_max, 400)
    y_curva = np.array([modulo.proyectar(resultado, tv) for tv in t_curva])

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(t_curva, y_curva, color=color, linewidth=2.5,
            label=f"Curva: {modulo.ecuacion_str(resultado)}")

    ax.scatter(t_datos, y_datos, color="#212121", zorder=5,
               s=60, label="Datos originales")

    for ti, yi in zip(t_datos, y_datos):
        ax.annotate(f"({ti:.2g}, {yi:.2g})",
                    (ti, yi), textcoords="offset points",
                    xytext=(6, 6), fontsize=8, color="#444")

    ax.set_title(f"Regresión {tipo}", fontsize=14, fontweight="bold")
    ax.set_xlabel("t", fontsize=12)
    ax.set_ylabel("Y", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.show()