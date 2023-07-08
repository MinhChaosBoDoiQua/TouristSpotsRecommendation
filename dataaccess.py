from var import Var
from db import DB 

class DataAccess:

    def get_spots(self):
        query = "SELECT * FROM data_spot "
        data = ()
        db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
        return db.execute(query, data)

    def get_spots_by_area(self, spot_area):
        query = "SELECT * FROM data_spot WHERE spot_area = %s "
        data = (str(spot_area), )
        db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
        return db.execute(query, data)

    def get_latlng_by_spot_name(self, spot_name):
        query = "SELECT spot_latitude, spot_longitude FROM data_spot WHERE spot_name = %s "
        data = (str(spot_name), )
        db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
        return db.execute(query, data)

    def get_openclose_by_spot_name(self, spot_name):
        query = "SELECT spot_opentime, spot_closetime FROM data_spot WHERE spot_name = %s "
        data = (str(spot_name), )
        db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
        return db.execute(query, data)

    def get_spot_by_features(self, feat1, feat2, feat3, feat4, feat5):
        query = "SELECT * FROM data_spot WHERE spot_history_culture = %s AND spot_food_product = %s AND spot_nature = %s AND spot_view = %s AND spot_experience = %s "
        data = (str(feat1), str(feat2), str(feat3), str(feat4), str(feat5), )
        db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
        return db.execute(query, data)

    def get_spot_by_branch(self, branch):
        query = "SELECT * FROM data_spot WHERE spot_opentime < %s AND spot_closetime > %s "
        data = (str(branch), str(branch), )
        db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
        return db.execute(query, data)
    
    #データベースを追加
    def insert_data(self,data1,data2,data3,data4,data5,data6,data7,data8,data9,data10,data11):
        query = """INSERT INTO data_spot (spot_area,spot_name,spot_latitude,spot_longitude,
        spot_history_culture,spot_food_product ,spot_nature,spot_view,spot_experience,
        spot_opentime,spot_closetime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        data = (str(data1), str(data2), str(data3), str(data4), str(data5), str(data6), str(data7), str(data8), str(data9),
                    str(data10), str(data11), )                                                                                               
        db = DB(Var.hostname, Var.port, Var.dbname, Var.username, Var.password)
        return db.update(query, data)