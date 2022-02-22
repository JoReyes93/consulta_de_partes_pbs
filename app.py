from flask import Flask, render_template, request, flash
import pandas as pd

app = Flask(__name__)
app.secret_key = "Jr201033330"

@app.route("/")
def index():
	#flash("Aqui va la pieza consultada")
	return render_template("index.html")

@app.route("/query", methods=["POST", "GET"])
def query():
        filename = "existbod.xls"
        columns = ["codigo", "descripcion", "reservado", "existencia"]

        df = pd.read_excel(filename, usecols = [0,1,11,12])
        df.columns = columns
        df.dropna(inplace=True)

        df["sin_reserva"] = df["existencia"] - df["reservado"]
        parte = str(request.form["part_name"]).upper()
        #resultado = df[df["codigo"].str.contains(parte)]
        #resultado = consulta.to_string(index=False)

        if parte.isdigit() != True:
                resultado = df[df["codigo"].str.contains(parte)]
                if len(resultado) > 0:
                        flash("Hay " + resultado["sin_reserva"].to_string(index=False) + " unidades disponibles en XNIC. Hay " + resultado["reservado"].to_string(index=False) + " unds reservadas.")
                else:
                        flash("No hay existencias por el momento")
                return render_template("index.html")
        else:
                flash("Ingrese un valor valido")
                return render_template("index.html")

if __name__=="__main__":
	app.run()
