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
        # Information on AQI breakpoints taken from https://www.epa.gov/sites/default/files/2016-04/documents/2012_aqi_factsheet.pdf
        # As this is designed for indoor use, I have omitted the following breakpoints:
        # Unhealthy (red) 55.5 - 150.4
        # Very Unhealthy (purple-ish?) 150.5 - 250.4
        # Hazardout (dark red) 250.5 - 500
        fig.add_hrect(y0=0.0, y1=12, fillcolor="lightgreen", opacity=0.4, line_width=0) # Good
        fig.add_hrect(y0=12.1, y1=35.4, fillcolor="yellow", opacity=0.3, line_width=0) # Moderate
        fig.add_hrect(y0=35.5, y1=55.4, fillcolor="orange", opacity=0.4, line_width=0) # Unhealthy for Sensitive Groups

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