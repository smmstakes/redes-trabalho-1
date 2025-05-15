# Utilities
import os
from typing import Self
from datetime import date
from dotenv import load_dotenv
from typing import ForwardRef

# Flask application
from flask import Flask
from openai import OpenAI
from flask_sqlalchemy import SQLAlchemy

# Loading .env file
load_dotenv()

# Creating flask app
app: Flask = Flask(__name__)

# Setting database up
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///python-notebot.sqlite3'
db: SQLAlchemy = SQLAlchemy(app)

# Flask app settings
app.secret_key = os.getenv('APP_SECRET_KEY')
app.app_context().push()

# Creating OpenAI client
client: OpenAI = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

# Creating forward refs
User = ForwardRef('User')
Note = ForwardRef('Note')


class DB:
    '''
    DB class
    
    Class containing methods to create tables and add, commit, delete data to db.
    '''

    # Singleton setup
    __instance = None

    # Creating singleton
    def __new__(cls) -> Self:
        if not DB.__instance:
            DB.__instance = super().__new__(cls)
        return DB.__instance

    def __init__(self) -> None:
        self.db: SQLAlchemy = db

    def create_all(self) -> None:
        '''
        Calls the 'create_all()' function, to create tables in the database.
        '''
        db.create_all()

    def commit_session(self) -> None:
        '''
        Calls the 'commit()' function, to commit changes to the database.
        '''
        db.session.commit()

    def add_data(self, data: User | Note) -> None:
        '''
        Adds the data to the session, and calls the 'commit_session()' method.
        '''
        db.session.add(data)
        self.commit_session()

    def delete_data(self, data: User | Note) -> None:
        '''
        Deletes the data from the session, and calls the 'commit_session()' method.
        '''
        db.session.delete(data)
        self.commit_session()


# User class
class User(db.Model):
    '''
    User class.
    
    Create new user objects.
    '''

    # Creating table fields
    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String, unique=True)
    password: str = db.Column(db.String)

    def __init__(self, name: str, password: str) -> None:
        super().__init__()
        self.name: str = name
        self.password: str = password
        self.db: DB = DB()

    @staticmethod
    def verify_credentials_login(
        name: str = None,
        password: str = None,
    ) -> bool:
        '''
        Verifies whether the user's credentials are valid for login.
        
        Takes a name and a password.
        
        Returns true if the name is found in the database and the password matches
        and false whether the name isn't found or the password is invalid.
        '''
        if User.query.filter_by(name=name, password=password).first():
            return True
        return False

    @staticmethod
    def verify_credentials_sign_up(name: str = None, ) -> bool:
        '''
        Verifies whether the user's credentials are valid for sign-up.
        
        Takes a name and returns true if the name is found in the database
        and false whether it isn't.
        '''
        if User.query.filter_by(name=name).first():
            return False
        return True

    @staticmethod
    def get_user(name: str) -> Self:
        '''
        Gets the user based on the name passed as the 'name' parameter
        '''
        return User.query.filter_by(name=name).first()


# Assistant bot class
class AssistantBot:
    '''
    AssistantBot class
    
    This class is where the ChatGPT API is used.
    '''

    # Singleton setup
    __instance = None

    # Creating singleton
    def __new__(cls) -> Self:
        if not AssistantBot.__instance:
            AssistantBot.__instance = super().__new__(cls)
        return AssistantBot.__instance

    def __init__(self) -> None:
        self.__model: str = 'gpt-3.5-turbo-0125'
        self.__response_format: dict[str, str] = {'type': 'text'}

    def prompt(self, prompt: str) -> str:
        '''
        Takes a string as prompt and returns a response generated based 
        on said prompt.
        
        All of the responses are based on Python concepts.
        '''

        # Generating ChatGPT response
        response = client.chat.completions.create(
            model=self.__model,
            response_format=self.__response_format,
            messages=[
                {
                    'role':
                    'system',
                    'content':
                    f'Com base na anotação passada como nota, elabore nos assuntos abordados sobre PYTHON, não use exemplos com markdown, simplesmente elabore nos assuntos'
                },
                {
                    'role': 'user',
                    'content': prompt
                },
            ],
        )

        # Returning response content
        return response.choices[0].message.content


# Note class
class Note(db.Model):
    '''
    Note class for creating new notes.
    
    This class manages the AssistantBot class with Aggregation.
    
    This class is also responsible for formatting the prompt of the Assistant bot,
    being the middle man between the prompt and it's log into the database.
    '''

    # Creating table fields
    __tablename__ = 'notes'

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String)
    author_id: int = db.Column(db.Integer)
    notes: str = db.Column(db.String)
    assistant_bot_notes: str = db.Column(db.String)

    def __init__(
        self,
        name: str,
        author_id: int,
        notes: str,
        assistant_bot: AssistantBot,
    ) -> None:
        super().__init__()
        self.name: str = name
        self.author_id: int = author_id
        self.notes: str = notes
        self.assistant_bot: AssistantBot = assistant_bot
        self.assistant_bot_notes: str = ''
        self.db: DB = DB()

    def create_prompt(self) -> None:
        '''
        Decorates the prompt and sets the 'self.assistant_bot_notes'
        to the value obtained from its assistant bot property's prompt.
        '''

        # Getting prompt
        prompt = self.assistant_bot.prompt(self.notes)

        # Getting date
        today = date.today().strftime('%d/%m/%Y')

        # Setting assistant bot notes to decorated prompt
        self.assistant_bot_notes = f'{today}: {prompt}'
