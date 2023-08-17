import firebase_admin
from firebase_admin import credentials

from ..src.code.utils.constants import Constants
Firebase = Constants.Config.Firebase

def initialize(config):
    firebase_key = Constants.Config.Key.FIREBASE

    if firebase_key in config:
        print('\n\n---------- Initializing firebase connection ----------')
        db_url = config[firebase_key][Firebase.DB_URL]

        try:
            cred = credentials.Certificate(f'{Constants.FirebaseAccountKey.LOCATION}\{Constants.FirebaseAccountKey.FILE_NAME}')
            firebase_admin.initialize_app(
                cred, 
                {'databaseURL': db_url}
            )
            print(f'Successfully established connection with \'{db_url}\'')
        except:
            raise ConnectionError(f'Could not established connection with \'{db_url}\'')

    else:
        raise ConnectionError(f'Configuration not found for the firebase connection')









# // Import the functions you need from the SDKs you need
# import { initializeApp } from "firebase/app";
# import { getAnalytics } from "firebase/analytics";
# // TODO: Add SDKs for Firebase products that you want to use
# // https://firebase.google.com/docs/web/setup#available-libraries

# // Your web app's Firebase configuration
# // For Firebase JS SDK v7.20.0 and later, measurementId is optional
# const firebaseConfig = {
#   apiKey: "AIzaSyD113UahTnGfJyYjDuPIIygamBgxif2yxg",
#   authDomain: "learn-tornado.firebaseapp.com",
#   projectId: "learn-tornado",
#   storageBucket: "learn-tornado.appspot.com",
#   messagingSenderId: "805974203777",
#   appId: "1:805974203777:web:70e6e1ede9661925425c80",
#   measurementId: "G-JPYXQ4756D"
# };

# // Initialize Firebase
# const app = initializeApp(firebaseConfig);
# const analytics = getAnalytics(app);