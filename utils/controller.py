from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from utils.db.db_clients import DbClient
#from utils.localizations.localizations import localizations
import os
from dotenv import dotenv_values

class Controller:
    def __init__(self):
        self.env_file_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        self.config = dotenv_values(".env")

        self.HOST = str()
        #self.SECRET_KEY = str()
        #self.ALGORITHM = str()

        self.SWAGGER_URL = str()
        self.REDOC_URL = str()
        self.OPENAPI_URL = str()

        # self.PASSWORD_MIN_LEN = int()
        # self.PASSWORD_MAX_LEN = int()

        self.load_env_variables()
        #self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")
        self.db = DbClient("db.sqlite")
        #self.locales = localizations


    def load_env_variables(self):
        try:
            self.HOST = self.config.get("HOST")
            #self.SECRET_KEY = self.config.get("SECRET_KEY")# TODO load from .env
            #self.ALGORITHM = self.config.get("ALGORITHM")
            self.SWAGGER_URL = self.config.get("SWAGGER_URL")
            self.REDOC_URL = self.config.get("REDOC_URL")
            self.OPENAPI_URL = self.config.get("OPENAPI_URL")
            #self.PASSWORD_MIN_LEN = int(float(str(self.config.get("PASSWORD_MIN_LEN")))) 
            #self.PASSWORD_MAX_LEN = int(float(str(self.config.get("PASSWORD_MAX_LEN")))) 
        except Exception as e:
            raise AttributeError(f".env file not found or doens't have proper key=values - {e}")

        return

controller = Controller()

