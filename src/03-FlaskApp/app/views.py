from flask import jsonify, render_template, request, redirect
from app import app
from app import flight_api 


@app.route('/')
@app.route('/flightsearch')
def flight_search_form():
   return render_template("flight_search_form.html")

@app.route('/slides')
def slides():
   return redirect ('https://docs.google.com/presentation/d/1e0jVsC-qtnaulvlq5WJLWjPDX4jHaJgMaYt6xHXScCs/',code=302)


@app.route('/', methods=['POST'])
@app.route('/flightsearch', methods=['POST'])
def flight_search_post():
   origin = request.form['origin']
   destination = request.form['destination']
   travel_date = request.form['date']
   results = flight_api.get_flights(origin,destination,travel_date)
   return (jsonify(results))

