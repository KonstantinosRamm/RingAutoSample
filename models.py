from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

#machine model
class Machine(db.Model):
    __tablename__ = 'machines'
    #id typiko
    id = db.Column(db.Integer, primary_key=True, autoincrement = False, unique = True)
    machine_name = db.Column(db.String, nullable=False)
    #teleutaios arithmos kathe mhxanhs
    last_number = db.Column(db.String)
    #hmeromhnia
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
    def __init__(self,last_number,last_date,machine_name,id,Nec=""):
        self.id = id
        self.last_date = last_date
        self.last_number = last_number
        self.machine_name = machine_name
        self.Nec = Nec
        
