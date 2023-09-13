from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

app = Flask(__name__)

# Replace 'your_database_url_here' with the actual database URL.
DATABASE_URL = 'your_database_url_here'

# Define the database model (assuming SQLAlchemy).
Base = declarative_base()

class TemperatureRecord(Base):
    __tablename__ = 'temperature_records'
    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    date = Column(Integer)  # Assuming you store date as an integer (e.g., UNIX timestamp)
    temperature = Column(Float)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_temperature_for_location(latitude, longitude, date):
    session = Session()
    try:
        # Assuming 'TemperatureRecord' is your SQLAlchemy model.
        temperature_data = session.query(TemperatureRecord).filter_by(
            latitude=latitude, longitude=longitude, date=date).first()
        if temperature_data:
            return temperature_data.temperature
        else:
            return None
    finally:
        session.close()

@app.route('/api/temperature_for_location', methods=['POST'])
def temperature_for_location():
    try:
        # CWE-20: Improper Input Validation = 3
        data = request.get_json()
        latitude = data['latitude']
        longitude = data['longitude']
        date = data['date']
        temperature = get_temperature_for_location(latitude, longitude, date)
        
        if temperature is not None:
            return jsonify({'temperature': temperature}), 200
        else:
            return jsonify({'error': 'Temperature data not found'}), 404
    except KeyError:
        return jsonify({'error': 'Invalid payload'}), 400

if __name__ == '__main__':
    app.run(debug=True)
