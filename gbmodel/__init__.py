model_backend = 'firestore'

from .model_firestore import model

appmodel = model()

def get_model():
    return appmodel
