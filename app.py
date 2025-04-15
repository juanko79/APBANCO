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
            
            # Validar datos
            if monto <= 0 or tna <= 0 or cuotas <= 0:
                return jsonify({"error": "Todos los valores deben ser mayores a 0."})
            
            # Cálculos
            tnm = tna / 12
            cuota_mensual = monto * (tnm * (1 + tnm)**cuotas) / ((1 + tnm)**cuotas - 1) if tnm != 0 else monto / cuotas
            
            monto_total = cuota_mensual * cuotas
            interes_total = monto_total - monto
            
            # Generar tabla de amortización
            tabla_amortizacion = []
            saldo = monto
            for cuota in range(1, cuotas + 1):
                pago_interes = saldo * tnm
                pago_capital = cuota_mensual - pago_interes
                saldo -= pago_capital
                tabla_amortizacion.append({
                    "cuota": cuota,
                    "interes": round(pago_interes, 2),
                    "capital": round(pago_capital, 2),
                    "saldo": round(max(saldo, 0), 2)
                })
            
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