import os


class Config:
    def __init__(self):
        """Base configuration variables."""
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        if not self.SECRET_KEY:
            raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
        
        self.TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
        if not self.TRELLO_API_KEY:
            raise ValueError("No TRELLO_API_KEY set for Flask application. Did you follow the setup instructions?")
        
        self.TRELLO_API_TOKEN = os.environ.get('TRELLO_API_TOKEN')
        if not self.TRELLO_API_TOKEN:
            raise ValueError("No TRELLO_API_TOKEN set for Flask application. Did you follow the setup instructions?")
        
        self.TRELLO_BOARD_ID = os.environ.get('TRELLO_BOARD_ID')
        if not self.TRELLO_BOARD_ID:
            raise ValueError("No TRELLO_BOARD_ID set for Flask application. Did you follow the setup instructions?")
        
        self.TRELLO_LIST_ID_TODO = os.environ.get('TRELLO_LIST_ID_TODO')
        if not self.TRELLO_LIST_ID_TODO:
            raise ValueError("No TRELLO_LIST_ID_TODO set for Flask application. Did you follow the setup instructions?")
        
        self.TRELLO_LIST_ID_DONE = os.environ.get('TRELLO_LIST_ID_DONE')
        if not self.TRELLO_LIST_ID_DONE:
            raise ValueError("No TRELLO_LIST_ID_DONE set for Flask application. Did you follow the setup instructions?")
