from flask import Flask, render_template, request
import plotly.graph_objects as go
import json

app = Flask(__name__)

# 🧊 تحويل درجات الحرارة بين الوحدات المختلفة
def convert_temp(temp, unit):
    try:
        temp = float(temp)
        if unit == "Celsius to Fahrenheit":
            return f"{temp}°C = {(temp * 9/5) + 32:.2f}°F"
        elif unit == "Celsius to Kelvin":
            return f"{temp}°C = {temp + 273.15:.2f}K"
        elif unit == "Fahrenheit to Celsius":
            return f"{temp}°F = {(temp - 32) * 5/9:.2f}°C"
        elif unit == "Fahrenheit to Kelvin":
            return f"{temp}°F = {(temp - 32) * 5/9 + 273.15:.2f}K"
        else:
            return "❌ وحدة غير معروفة!"
    except ValueError:
        return "⚠ يرجى إدخال رقم صحيح!"

# 🔥 إنشاء منحنى التسخين التفاعلي
def generate_heating_curve():
    time = list(range(0, 25))  # الزمن بالثواني
    temp = [0, 10, 20, 30, 40, 50, 60, 60, 60, 70, 80, 90, 100, 100, 100, 110, 120, 130]  

    # إنشاء الرسم
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=temp, mode='lines+markers', name="درجة الحرارة"))

    fig.update_layout(title="منحنى التسخين",
                      xaxis_title="الزمن (ثانية)",
                      yaxis_title="درجة الحرارة (°C)",
                      template="plotly_dark")

    from plotly.utils import PlotlyJSONEncoder
    return json.dumps(fig, cls=PlotlyJSONEncoder)


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        temp = request.form["temperature"]
        unit = request.form["unit"]
        result = convert_temp(temp, unit)

    graph_json = generate_heating_curve()
    return render_template("index.html", result=result, graph_json=graph_json)

if __name__ == "__main__":
    app.run(debug=True)
