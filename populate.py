from app import app, db
from models import Machine
from machines import machine_type
from datetime import datetime

def populate_machines():
    with app.app_context():
        db.create_all()  # create tables if not exist

        # populate the table with machines if non existent
        for machine_id, machine_name in machine_type.items():
            if not Machine.query.filter_by(id=machine_id).first():
                new_machine = Machine(
                    id=machine_id,
                    machine_name=machine_name,
                    last_number=None,
                    last_date=datetime.today(),
                    Nec=""
                )
                db.session.add(new_machine)

        db.session.commit()

if __name__ == "__main__":
    populate_machines()