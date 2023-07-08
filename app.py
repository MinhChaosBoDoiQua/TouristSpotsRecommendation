"""
finalwork/app.py
Sample Web Application for AI-TECH

(C) 2022 Nguyen Tien Minh
"""
import folium
from flask import Flask, Response, request, render_template
from flask_bootstrap import Bootstrap
import os
from dataaccess import DataAccess
import aialgorithm as ai

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
bootstrap = Bootstrap(app)
basedir = os.path.dirname(__file__)

da = DataAccess()
data = da.get_spots()

#ホーム
@app.route("/")
def index():
    return render_template("index.html")

#データベース確認用
@app.route("/dataset")
def dataset():
    return render_template("db.html", data=data)

#データベース追加用
@app.route("/uploads", methods=["GET", "POST"])
def uploads():
    if request.method == "GET":
        return render_template("uploads.html")
    else:
        d1 = request.form["cityname"]
        d2 = request.form["spotname"]
        d3 = request.form["spotlat"]
        d4 = request.form["spotlong"]
        d5 = request.form["spothiscul"]
        d6 = request.form["spotfood"]
        d7 = request.form["spotnature"]
        d8 = request.form["spotview"]
        d9 = request.form["spotexperience"]
        d10 = request.form["spotopen"]
        d11 = request.form["spotclose"]
        da.insert_data(d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11)
        data = da.get_spots()
        return render_template("db.html", data=data)

#感性的特徴で観光地を探す
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        result_map = folium.Map(location=[35.6645,139.7104], zoom_start=5)
        for i in ai.query():
            d = data[i]
            folium.Marker(location=[d[3], d[4]],
                    popup=d[2]).add_to(result_map)
        filepath = os.path.join(basedir, "templates/map_result.html")
        result_map.save(filepath)
        return render_template("map_result.html")
        
#マップ
@app.route("/maps/<name>")
def maps(name):
    if name == "all":
        maps = folium.Map(location=[35.6645,139.7104], zoom_start=5)
    
    if name == "osaka":
        maps = folium.Map(location=[34.665394,135.432526], zoom_start=12)
    
    if name == "sapporo":
        maps = folium.Map(location=[42.952518,141.116439], zoom_start=12)
    
    if name == "tokyo":
        maps = folium.Map(location=[35.631112,139.78660], zoom_start=12)
    
    latlng = []
    spot_name = []
    for d in data:
        latlng.append([d[3], d[4]])
        spot_name.append([d[2]])
    for v, name in zip(latlng,spot_name):
        folium.Marker(location=[v[0], v[1]],
                    popup=name[0]).add_to(maps)
    filepath = os.path.join(basedir, "templates/maps.html")
    maps.save(filepath)
    
    return render_template("maps.html")

#巡回セールスマン問題の解法
@app.route("/shortestpath", methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return render_template("shortestpath.html")
    else:
        spot_area = request.form["spot_area"]
        area = da.get_spots_by_area(spot_area)
        latlng = []
        for d in area:
            latlng.append([d[3], d[4]])
        ai.POINTS_SIZE = len(area)
        out = ai.ga(latlng)
        return render_template("shortestpath.html", area=area, out=out)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)