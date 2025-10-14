from flask_sqlalchemy import SQLAlchemy
from datetime import date
db=SQLAlchemy()

#machine model
class Machine(db.Model):
    __tablename__ = 'machines'
    #id 
    id = db.Column(db.Integer, primary_key=True, autoincrement = False, unique = True)
    machine_name = db.Column(db.String, nullable=False)
    #last number of each machine
    last_number = db.Column(db.String)
    #previous last number to retrieve the current ones
    previous_last_number = db.Column(db.String)
    #date of each selected machine
    last_date = db.Column(db.Date)

    """
    NEC Index in Textiles
    The NEC (Number English Count) is a standard measure used in the textile industry to express the fineness (thickness) of yarns.
    It is calculated as NEC = 1000/T
    T = yarn linear density in tex (grams per 1000 meters).
    """
    Nec = db.Column(db.String)

    #working machine 
    is_active = db.Column(db.Boolean, default=True)
    def __init__(self,last_number=None,last_date=None,machine_name=None,id=None,Nec=""):
        self.id = id
        self.last_date = last_date if last_date else date.today()
        self.last_number = last_number if last_number else "1-12"
        self.machine_name = machine_name
        self.Nec = Nec
        self.previous_last_number = self.last_number

    #helper function to create json object
    def to_dict(self):
        return {
            "id" : self.id,
            "machine_name" : self.machine_name,
            "last date" : self.last_date,
            "last number" : self.last_number,
            "nec" : self.Nec,
            "active" : self.is_active
        }

