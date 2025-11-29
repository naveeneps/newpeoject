from flask import Flask, render_template

app= Flask('my prod app')

@app.route("/")
def Index():
    return render_template("index.html")

app.run()


app.route("/save")
def save():
    return " This is a buttn click handler"

app.run(debug=True)