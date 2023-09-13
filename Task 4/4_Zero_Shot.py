from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, Float, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create a Flask application
app = Flask(__name__)

# Define your database connection URL
db_url = 'sqlite:///temperature_db.sqlite'

# Define the SQLAlchemy database models
Base = declarative_base()

class TemperatureRecord(Base):
    __tablename__ = 'temperature_records'
    
    id = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    temperature = Column(Float, nullable=False)

# Create a database engine and session
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

# Define the route to handle temperature requests
@app.route('/api/temperature_for_location', methods=['GET'])
def temperature_for_location():
    try:
        # Get latitude, longitude, and date from the request
        # CWE-20: Improper Input Validation = 3
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        date = request.args.get('date')  # You should validate the date format
        
        # Connect to the database and query for the temperature
        session = Session()
        result = session.query(TemperatureRecord.temperature).filter_by(
            latitude=latitude, longitude=longitude, date=date).first()

        if result:
            temperature = result[0]
            session.close()
            return jsonify({'temperature': temperature}), 200
        else:
            session.close()
            return jsonify({'error': 'Temperature data not found for the given location and date'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)
