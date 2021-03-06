from appserver.persistence.mongodb import MONGO_CONFIG
from appserver.applog import LoggerFactory

logger = LoggerFactory().getLogger('UserRepository')
cn = MONGO_CONFIG.get_connection()
db = MONGO_CONFIG.get_database_from(cn)
collection=db.users

class UserRepository(object):
    def __init__(self):
        self.collection = collection
    def insert(self, user):
        logger.info('insert')
        user_id = collection.insert_one(user)
        return None if user_id == None else str(user_id)
    def update(self, username, payload):
        logger.info('update')
        return collection.update_one({'username': username}, {'$set':payload})
    def update_ssId(self, ssId, payload):
        logger.info('update_ssId')
        return collection.update_one({'ssId': ssId}, {'$set':payload})
    def find(self, filter = {}, projection={}):
        logger.info('find')
        projection['_id'] = False
        projection['password'] = False
        projection['token'] = False
        return collection.find(filter, projection)
    def find_one(self, username, projection={}):
        logger.info('find_one')
        logger.debug(username)
        projection['_id'] = False
        return collection.find_one({'username': username}, projection)
    def find_one_ssId(self, ssId, projection={}):
        logger.info('find_one_ssId')
        logger.debug(ssId)
        projection['_id'] = False
        return collection.find_one({'ssId': ssId}, projection)
