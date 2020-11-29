import json
beer = {}
wifi = {"ssid" : "" , "pass" : ""}

with open('wifi.json', 'r') as f:
  wifi = json.load(f)
  print("Load Wifi")

with open('beer.json', 'r') as f:
  beer = json.load(f)
  print(beer)


def update_beer():
    with open('beer.json', 'w') as f:
        json.dump(beer, f)
        print("Beer Update")
        
        
def update_wifi():
    with open('wifi.json', 'w') as f:
        json.dump(wifi, f)
        print("wifi Update")


