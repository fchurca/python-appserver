import flask
from datetime import datetime
from flask import request
from flask_restful import Resource
from geopy.distance import vincenty
from appserver.applog import LoggerFactory
from appserver.auth import Auth
from appserver.persistence.mongodb.user import UserRepository
from appserver.persistence.mongodb.trip import TripRepository
from appserver.remotes.usig import USIGRemote

logger = LoggerFactory().getLogger('PositionResource')
userRepository = UserRepository()
tripRepository = TripRepository()
usigRemote = USIGRemote()

MINIMUM_STEP=100

class PositionResource(Resource):
    def post(self):
        logger.info('post')
        user = Auth.authenticate()
        if (user is None):
            logger.info('wrong username')
            return 'Wrong username and/or password', 401
        logger.info('existing user')
        content = request.get_json()
        latitude = content['latitude']
        longitude = content['longitude']
        username = user['username']
        timestamp = str(datetime.now())
        data={
                'position':{
                    'latitude':latitude,
                    'longitude':longitude},
                'time':timestamp}
        logger.debug(data)
        if not userRepository.update(username, data):
            return "There was an error processing the request", 500
        logger.info('User position updated')
        if 'trip_id' not in user or user['trip_id'] is None:
            logger.info('User not in trip')
            return data, 200
        logger.info('User in trip')
        trip_id = user['trip_id']
        trip = tripRepository.find_one(trip_id)
        logger.debug(trip)
        if trip['passenger_ssId'] != user['ssId']:
            logger.info('User not trip passenger')
            return data, 200
        logger.debug(trip)
        if trip['state'] != 'in_car':
            logger.info('Trip not in_car')
            return data, 200
        logger.info('Trip in_car')
        route = trip['route']
        lastDistance=trip['distance']
        lastPosition=route[-1]['location']
        step = vincenty((latitude, longitude), (lastPosition['lat'], lastPosition['lon'])).meters
        if step < MINIMUM_STEP:
            logger.info('short step')
            return data, 200
        distance = lastDistance + step
        logger.debug(step)
        logger.debug(distance)
        street = usigRemote.normalizar({
            'lat':latitude,
            'lng':longitude}).json()['direccion']
        logger.debug(street)
        del route[-1]['street']
        route.append({
            'street':street,
            'location':{
                'lat':latitude,
                'lon':longitude},
            'timestamp':timestamp})
        logger.debug(route)
        logger.debug(tripRepository.update(trip_id,{
            'distance':distance,
            'route':route}))
        logger.info('success')
        return data, 200

