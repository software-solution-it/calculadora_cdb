from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        aporte_mensal = float(request.form['investment'])
        prazo_meses = 3 * 12  
        taxa_cdi_anual = 0.1365  
        taxa_cdb_anual = taxa_cdi_anual * 1.06  
        taxa_cdb_mensal = (1 + taxa_cdb_anual) ** (1/12) - 1 

        saldo_acumulado = 0
        rendimento_total = 0
        total_investido = 0
        historico_saldo = []

        for mes in range(1, prazo_meses + 1):
            saldo_acumulado += aporte_mensal
            total_investido += aporte_mensal 
            rendimento_mensal = saldo_acumulado * taxa_cdb_mensal
            saldo_acumulado += rendimento_mensal
            rendimento_total += rendimento_mensal
            historico_saldo.append(round(saldo_acumulado, 2))

        if prazo_meses <= 180:
            aliquota_ir = 0.225
        elif prazo_meses <= 360:
            aliquota_ir = 0.20
        elif prazo_meses <= 720:
            aliquota_ir = 0.175
        else:
            aliquota_ir = 0.15

        imposto_renda = rendimento_total * aliquota_ir
        saldo_liquido = saldo_acumulado - imposto_renda

        margem_de_lucro = saldo_liquido - total_investido

        return jsonify({
            "historico_saldo": historico_saldo,
            "total_investido": round(total_investido, 2),
            "saldo_final": round(saldo_liquido, 2),
            "margem_de_lucro": round(margem_de_lucro, 2)
        })
    except ValueError:
        return jsonify({"error": "Invalid input. Please enter a valid number."}), 400

if __name__ == '__main__':
    app.run(debug=True)
