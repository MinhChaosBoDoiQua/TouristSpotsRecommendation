CREATE TABLE data_spot ( 
	spot_id SERIAL PRIMARY KEY, 
	spot_area TEXT,
	spot_name TEXT,
	spot_latitude TEXT, 
	spot_longitude TEXT, 
	spot_history_culture INTEGER, 
	spot_food_product INTEGER, 
	spot_nature INTEGER, 
	spot_view INTEGER, 
	spot_experience INTEGER, 
	spot_opentime TIME, 
	spot_closetime TIME
);
