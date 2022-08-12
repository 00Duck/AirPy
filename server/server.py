from flask import Flask, render_template, request
import atexit
import db
import plotly.express as px

database = db.DB()
database.connect()

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def root_path():
    if request.method == 'GET':
        data = database.retrieve_data()
        fig = px.line(data_frame=data, x="measured_at", y=["pm_two_five", "pm_ten"], labels={"measured_at":"Measured At", "pm_two_five":"PM 2.5", "pm_ten": "PM 10"})
        return render_template('index.html', plotly_json=fig.to_json())
    if request.method == 'POST':
        req = (request.form['pm_two_five'], request.form['pm_ten'], request.form['measured_at'])
        database.collect(req)
        return {"status": "ok"}, 200

@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html'), 404

def onExitApp(user):
    database.conn.close()
    print(user, " exiting.")

atexit.register(onExitApp, user='AirPy')

if __name__ == "__main__":
    app.run()