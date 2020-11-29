from microdot_asyncio import Microdot, redirect, send_file
import cfg
from machine import reset

app = Microdot()


@app.route('/', methods=['GET', 'POST'])
def index(request):
    response = send_file('index.html')
    if request.method == 'POST':
       
        cfg.beer["strike_temp"] = request.form["strike_temp"]
        cfg.beer["mash"]["temp"] = request.form["mash_temp"]
        cfg.beer["mash"]["time"] = request.form["mash_time"]
        cfg.beer["boil_time"] = request.form["boil_time"]

        cfg.update_beer()

    return response

@app.route('/data', methods=['GET', 'POST'])
def index(request):
    return cfg.beer



@app.route('/wifi', methods=['GET', 'POST'])
def wifi(request):
    response = send_file('wifi.html')
    
    if request.method == 'POST':
       
        cfg.wifi["ssid"] = request.form["ssid"]
        cfg.wifi["pass"] = request.form["pass"]
        cfg.update_wifi()
        reset()
    
    return response
    