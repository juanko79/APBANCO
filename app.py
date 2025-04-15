from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def calcular_prestamo():
    if request.method == "POST":
        try:
            # Obtener datos del formulario
            monto = float(request.form.get("monto"))
            tna = float(request.form.get("tna")) / 100
            cuotas = int(request.form.get("cuotas"))
            sistema = request.form.get("sistema", "frances")  # Por defecto francés

            # Validar datos
            if monto <= 0 or tna < 0 or cuotas <= 0:
                return jsonify({"error": "Todos los valores deben ser mayores a 0."})

            # Cálculos
            tnm = tna / 12
            tabla_amortizacion = []

            if sistema == "frances":
                cuota_mensual = monto * (tnm * (1 + tnm)**cuotas) / ((1 + tnm)**cuotas - 1) if tnm != 0 else monto / cuotas
                saldo = monto
                for cuota in range(1, cuotas + 1):
                    interes = saldo * tnm
                    capital = cuota_mensual - interes
                    saldo -= capital
                    tabla_amortizacion.append({
                        "cuota": cuota,
                        "interes": round(interes, 2),
                        "capital": round(capital, 2),
                        "saldo": round(max(saldo, 0), 2)
                    })

            elif sistema == "aleman":
                capital = monto / cuotas
                saldo = monto
                for cuota in range(1, cuotas + 1):
                    interes = saldo * tnm
                    cuota_total = capital + interes
                    saldo -= capital
                    tabla_amortizacion.append({
                        "cuota": cuota,
                        "interes": round(interes, 2),
                        "capital": round(capital, 2),
                        "saldo": round(max(saldo, 0), 2)
                    })
                cuota_mensual = tabla_amortizacion[0]["capital"] + tabla_amortizacion[0]["interes"]  # Cuota 1

            elif sistema == "americano":
                saldo = monto
                interes_mensual = monto * tnm
                for cuota in range(1, cuotas + 1):
                    if cuota == cuotas:
                        capital = monto
                    else:
                        capital = 0
                    interes = interes_mensual
                    cuota_total = capital + interes
                    saldo -= capital
                    tabla_amortizacion.append({
                        "cuota": cuota,
                        "interes": round(interes, 2),
                        "capital": round(capital, 2),
                        "saldo": round(max(saldo, 0), 2)
                    })
                cuota_mensual = interes_mensual if cuotas > 1 else monto + interes_mensual

            else:
                return jsonify({"error": "Sistema de amortización no válido."})

            monto_total = sum(item["interes"] + item["capital"] for item in tabla_amortizacion)
            interes_total = monto_total - monto

            return jsonify({
                "cuota_mensual": round(cuota_mensual, 2),
                "monto_total": round(monto_total, 2),
                "interes_total": round(interes_total, 2),
                "tabla_amortizacion": tabla_amortizacion
            })

        except Exception as e:
            return jsonify({"error": f"Error en los datos: {str(e)}"})

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
