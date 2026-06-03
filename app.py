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

def generar_grafica(resultado, mod, x_proyectar, y_proyectar):
    x_datos = resultado.get("x", resultado.get("t"))
    y_datos = resultado["y"]
    tipo = resultado["tipo"]

    COLORES = {
        "Lineal": "#2196F3",
        "Cuadrática": "#9C27B0",
        "Exponencial": "#F44336",
    }
    color = COLORES.get(tipo, "#333333")

    x_min = min(x_datos) - 0.5
    x_max = max(x_datos) + 0.5
    x_curva = np.linspace(x_min, x_max, 400)
    y_curva = np.array([mod.proyectar(resultado, xv) for xv in x_curva])

    fig, ax = plt.subplots(figsize=(8, 5))

    # Curva de regresión
    ax.plot(x_curva, y_curva, color=color, linewidth=2.5,
            label=f"Curva: {mod.ecuacion_str(resultado)}")

    # Puntos originales
    ax.scatter(x_datos, y_datos, color="#212121", zorder=5,
               s=60, label="Datos originales")

    # Punto proyectado
    ax.scatter([x_proyectar], [y_proyectar], color="#FF6F00", zorder=6,
               s=120, marker="*", label=f"Proyección X={x_proyectar} → Y={y_proyectar:.4f}")

    for xi, yi in zip(x_datos, y_datos):
        ax.annotate(f"({xi:.2g}, {yi:.2g})", (xi, yi),
                    textcoords="offset points", xytext=(6, 6),
                    fontsize=8, color="#444")

    ax.set_title(f"Regresión {tipo}", fontsize=14, fontweight="bold")
    ax.set_xlabel("X", fontsize=12)
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
    x_vals = data.get('x_vals')
    y_vals = data.get('y_vals')
    x_proyectar = data.get('x_proyectar')

    try:
        if tipo == 'lineal':
            mod = lineal
        elif tipo == 'cuadratica':
            mod = cuadratica
        elif tipo == 'exponencial':
            mod = exponencial
        else:
            return jsonify({'error': 'Tipo inválido'})

        resultado = mod.calcular(x_vals, y_vals)
        resultado["x"] = resultado.get("x", resultado.get("t", x_vals))
        y_proyectar = mod.proyectar(resultado, x_proyectar)

        texto = "SISTEMA DE ECUACIONES:\n"
        for eq in resultado["ecuaciones"]:
            texto += f"  {eq}\n"
        if "nota" in resultado:
            texto += f"\n  {resultado['nota']}\n"
        texto += f"\nECUACIÓN AJUSTADA:\n  {mod.ecuacion_str(resultado)}"
        texto += f"\n\nPROYECCIÓN:\n  Para X = {x_proyectar}  →  Y ≈ {y_proyectar:.6f}"

        grafica = generar_grafica(resultado, mod, x_proyectar, y_proyectar)

        tabla_html = "<table class='tabla-regresion'><thead>"
        x_arr = np.array(x_vals)
        y_arr = np.array(y_vals)
        
        if tipo == 'lineal':
            tabla_html += "<tr><th>X</th><th>Y</th><th>X²</th><th>X·Y</th></tr></thead><tbody>"
            for x, y in zip(x_arr, y_arr):
                tabla_html += f"<tr><td>{x:.4f}</td><td>{y:.4f}</td><td>{x**2:.4f}</td><td>{x*y:.4f}</td></tr>"
            tabla_html += f"<tr class='totales'><td>{np.sum(x_arr):.4f}</td><td>{np.sum(y_arr):.4f}</td><td>{np.sum(x_arr**2):.4f}</td><td>{np.sum(x_arr*y_arr):.4f}</td></tr>"
        elif tipo == 'cuadratica':
            tabla_html += "<tr><th>X</th><th>Y</th><th>X²</th><th>X³</th><th>X⁴</th><th>X·Y</th><th>X²·Y</th></tr></thead><tbody>"
            for x, y in zip(x_arr, y_arr):
                tabla_html += f"<tr><td>{x:.4f}</td><td>{y:.4f}</td><td>{x**2:.4f}</td><td>{x**3:.4f}</td><td>{x**4:.4f}</td><td>{x*y:.4f}</td><td>{(x**2)*y:.4f}</td></tr>"
            tabla_html += f"<tr class='totales'><td>{np.sum(x_arr):.4f}</td><td>{np.sum(y_arr):.4f}</td><td>{np.sum(x_arr**2):.4f}</td><td>{np.sum(x_arr**3):.4f}</td><td>{np.sum(x_arr**4):.4f}</td><td>{np.sum(x_arr*y_arr):.4f}</td><td>{np.sum((x_arr**2)*y_arr):.4f}</td></tr>"
        elif tipo == 'exponencial':
            lny_arr = np.log(y_arr)
            tabla_html += "<tr><th>X</th><th>Y</th><th>ln(Y)</th><th>X·ln(Y)</th><th>X²</th></tr></thead><tbody>"
            for x, y, lny in zip(x_arr, y_arr, lny_arr):
                tabla_html += f"<tr><td>{x:.4f}</td><td>{y:.4f}</td><td>{lny:.4f}</td><td>{x*lny:.4f}</td><td>{x**2:.4f}</td></tr>"
            tabla_html += f"<tr class='totales'><td>{np.sum(x_arr):.4f}</td><td>{np.sum(y_arr):.4f}</td><td>{np.sum(lny_arr):.4f}</td><td>{np.sum(x_arr*lny_arr):.4f}</td><td>{np.sum(x_arr**2):.4f}</td></tr>"
        tabla_html += "</tbody></table>"

        return jsonify({'texto': texto, 'grafica': grafica, 'tabla': tabla_html})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)