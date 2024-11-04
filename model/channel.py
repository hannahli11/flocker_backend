# channel.py
from sqlite3 import IntegrityError
from sqlalchemy import Text, JSON
from __init__ import app, db
from model.group import Group

class Channel(db.Model):
    """
    Channel Model
    
    The Channel class represents a channel within a group, with customizable attributes.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the channel.
        _name (db.Column): A string representing the name of the channel.
        _attributes (db.Column): A JSON blob representing customizable attributes for the channel.
        _group_id (db.Column): An integer representing the group to which the channel belongs.
    """
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), nullable=False)
    _attributes = db.Column(JSON, nullable=True)
    _group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)

    posts = db.relationship('Post', backref='channel', lazy=True)

    def __init__(self, name, group_id, attributes=None):
        """
        Constructor, 1st step in object creation.
        
        Args:
            name (str): The name of the channel.
            group_id (int): The group to which the channel belongs.
            attributes (dict, optional): Customizable attributes for the channel. Defaults to None.
        """
        self._name = name
        self._group_id = group_id
        self._attributes = attributes or {}

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr() built-in function.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"Channel(id={self.id}, name={self._name}, group_id={self._group_id}, attributes={self._attributes})"
    
    @property
    def name(self):
        """
        Gets the channel's name.
        
        Returns:
            str: The channel's name.
        """
        return self._name

    def create(self):
        """
        The create method adds the object to the database and commits the transaction.
        
        Uses:
            The db ORM methods to add and commit the transaction.
        
        Raises:
            Exception: An error occurred when adding the object to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        The read method retrieves the object data from the object's attributes and returns it as a dictionary.
        
        Returns:
            dict: A dictionary containing the channel data.
        """
        return {
            'id': self.id,
            'name': self._name,
            'attributes': self._attributes,
            'group_id': self._group_id
        }

def initChannels():
    """
    The initChannels function creates the Channel table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        Channel objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""

        # Home Page Channels
        general = Group.query.filter_by(_name='General').first()
        support = Group.query.filter_by(_name='Support').first()
        home_page_channels = [
            Channel(name='Announcements', group_id=general.id),
            Channel(name='Events', group_id=general.id),
            Channel(name='FAQ', group_id=support.id),
            Channel(name='Help Desk', group_id=support.id)
        ]
        
        # Shared Interest Channels 
        limitless_connection = Group.query.filter_by(_name='Limitless Connections').first() 
        dnhs_football = Group.query.filter_by(_name='DNHS Football').first() 
        school_subjects = Group.query.filter_by(_name='School Subjects').first()
        music = Group.query.filter_by(_name='Music').first()
        satire = Group.query.filter_by(_name='Satire').first()
        activity_hub = Group.query.filter_by(_name='Activity Hub').first()
        shared_interest_channels = [
            Channel(name='Penpal Letters', group_id=limitless_connection.id),
            Channel(name='Game vs Poway', group_id=dnhs_football.id),
            Channel(name='Game vs Westview', group_id=dnhs_football.id),
            Channel(name='Math', group_id=school_subjects.id),
            Channel(name='English', group_id=school_subjects.id),
            Channel(name='Artist', group_id=music.id),
            Channel(name='Music Genre', group_id=music.id),
            Channel(name='Humor', group_id=satire.id),
            Channel(name='Memes', group_id=satire.id),
            Channel(name='Irony', group_id=satire.id),
            Channel(name='Cyber Patriots', group_id=activity_hub.id),
            Channel(name='Robotics', group_id=activity_hub.id)
        ]
        
        channels = home_page_channels + shared_interest_channels
        for channel in channels:
            try:
                db.session.add(channel)
                db.session.commit()
                print(f"Record created: {repr(channel)}")
            except IntegrityError:
                db.session.rollback()
                print(f"Records exist, duplicate email, or error: {channel.name}")