from flask import Flask, render_template, request, jsonify
import lineal
import cuadratica
import exponencial
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

def generar_grafica(resultado, mod, t_proyectar, y_proyectar):
    t_datos = resultado["t"]
    y_datos = resultado["y"]
    tipo = resultado["tipo"]

    COLORES = {
        "Lineal": "#2196F3",
        "Cuadrática": "#9C27B0",
        "Exponencial": "#F44336",
    }
    color = COLORES.get(tipo, "#333333")

    t_min = min(t_datos) - 0.5
    t_max = max(t_datos) + 0.5
    t_curva = np.linspace(t_min, t_max, 400)
    y_curva = np.array([mod.proyectar(resultado, tv) for tv in t_curva])

    fig, ax = plt.subplots(figsize=(8, 5))

    # Curva de regresión
    ax.plot(t_curva, y_curva, color=color, linewidth=2.5,
            label=f"Curva: {mod.ecuacion_str(resultado)}")

    # Puntos originales
    ax.scatter(t_datos, y_datos, color="#212121", zorder=5,
               s=60, label="Datos originales")

    # Punto proyectado
    ax.scatter([t_proyectar], [y_proyectar], color="#FF6F00", zorder=6,
               s=120, marker="*", label=f"Proyección t={t_proyectar} → Y={y_proyectar:.4f}")

    for ti, yi in zip(t_datos, y_datos):
        ax.annotate(f"({ti:.2g}, {yi:.2g})", (ti, yi),
                    textcoords="offset points", xytext=(6, 6),
                    fontsize=8, color="#444")

    ax.set_title(f"Regresión {tipo}", fontsize=14, fontweight="bold")
    ax.set_xlabel("t", fontsize=12)
    ax.set_ylabel("Y", fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.get_json()
    tipo = data.get('tipo')
    t_vals = data.get('t_vals')
    y_vals = data.get('y_vals')
    t_proyectar = data.get('t_proyectar')

    try:
        if tipo == 'lineal':
            mod = lineal
        elif tipo == 'cuadratica':
            mod = cuadratica
        elif tipo == 'exponencial':
            mod = exponencial
        else:
            return jsonify({'error': 'Tipo inválido'})

        resultado = mod.calcular(t_vals, y_vals)
        y_proyectar = mod.proyectar(resultado, t_proyectar)

        texto = "SISTEMA DE ECUACIONES:\n"
        for eq in resultado["ecuaciones"]:
            texto += f"  {eq}\n"
        if "nota" in resultado:
            texto += f"\n  {resultado['nota']}\n"
        texto += f"\nECUACIÓN AJUSTADA:\n  {mod.ecuacion_str(resultado)}"
        texto += f"\n\nPROYECCIÓN:\n  Para t = {t_proyectar}  →  Y ≈ {y_proyectar:.6f}"

        grafica = generar_grafica(resultado, mod, t_proyectar, y_proyectar)

        return jsonify({'texto': texto, 'grafica': grafica})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)