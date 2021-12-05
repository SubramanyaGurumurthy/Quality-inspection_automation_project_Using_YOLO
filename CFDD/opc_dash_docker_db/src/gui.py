from typing import Tuple
from flask import Flask
import dash
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime
from helpers import datetime_to_url_string, get_new_Data, datetime_for_table
import datetime

from constants import DEBUG, MAX_NUM_TIMESTAMPS, PORT_GUI, HOST_GUI, UPDATE_FREQUENCY_GUI, GUI_ERROR_THRESHOLD, UPDATE_FREQUENCY_YOLO, HOST_DATABASE_BROWSER, PORT_DATABASE, IMAGE_STANDARD

# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP]) # external_stylesheet needed for progressBar

# adding stylesheet
stylesheets = ['stylesheet.css']
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

start_timestamp = datetime.datetime.now()
latest_timestamps = []
newest_detection_datetime = start_timestamp

app.layout = html.Div(
    className="mainDiv",
    children=[
        html.H1("Latest Outputs"),
        html.Div(
            className="container",
            children=[
                html.Div(
                    className="table",
                    children=[
                        dbc.Alert(
                            id="alert",
                            children="This is a primary alert",
                            color="primary"),
                        dash_table.DataTable(
                        id='table',
                        columns=[{"name": "timestamps", "id": "timestamps"}],
                        data=[],
                        ),
                    ]
                ),
                html.Img(
                    className="image",
                    id="image",
                    src='http://' + HOST_DATABASE_BROWSER + ':' + str(PORT_DATABASE) + '/get_image/' + IMAGE_STANDARD,
                )
            ]
        ),
        dcc.Interval(id="interval", n_intervals=0, interval=int(UPDATE_FREQUENCY_GUI/0.001)),
    ]
)

def get_newest_image_url(latest_timestamps):
    if len(latest_timestamps) > 0:
        timestamp_latest_received = datetime_to_url_string(latest_timestamps[0])
    else:
        timestamp_latest_received = IMAGE_STANDARD
    
    image_url = 'http://' + 'localhost' + ':' + str(PORT_DATABASE) + '/get_image/' + timestamp_latest_received
    print(image_url)
    return image_url

@app.callback(
    [Output("table", "data"), Output("alert", "color"), Output("alert", "children"), Output("image", "src")],
    [Input("interval", "n_intervals")],
)
# updating table with boolean values and timestamps every half second
def update_table(n_intervals) -> Tuple[list, bool, bool]:

    # load new timestamps and format them for the table
    global latest_timestamps
    global start_timestamp
    global newest_detection_datetime
    
    new_data = get_new_Data(newest_detection_datetime)
    latest_timestamps = latest_timestamps + new_data
    latest_timestamps = list(reversed(sorted(set(latest_timestamps))))
    latest_timestamps = latest_timestamps[:MAX_NUM_TIMESTAMPS]

    if len(latest_timestamps) > 0:
        newest_detection_datetime = latest_timestamps[0]
    else:
        newest_detection_datetime = start_timestamp
    
    image_url = get_newest_image_url(latest_timestamps)
    datetime_now = datetime.datetime.now()
    seconds_passed = (datetime_now - newest_detection_datetime).total_seconds()

    if (seconds_passed > UPDATE_FREQUENCY_YOLO + GUI_ERROR_THRESHOLD):
        alertCol="success"
        alertText="Everything is fine:)"
    else:
        alertCol="danger"
        alertText="Seems like something's wrong!"
    latest_timestamps_strings = list(map(datetime_for_table, latest_timestamps))
    data_for_datatable = [{'timestamps': s} for s in latest_timestamps_strings]
    
    return data_for_datatable, alertCol, alertText, image_url

def startGUI() -> None:
    global app
    app.run_server(host=HOST_GUI, port=PORT_GUI, debug=DEBUG)

if __name__ == "__main__":
    startGUI()