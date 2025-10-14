from flask import Blueprint,jsonify,request
from app import db
from models import Machine
from datetime import datetime,date
from machines import machine_dictionary


api = Blueprint("api",__name__)


#------------------------------
#           GET
#------------------------------

#   GET ALL MACHINES
@api.route('/machines',methods = ['GET'])
def get_machines():
    machines = Machine.query.all()
    result = [machine.to_dict() for machine in machines]
    return jsonify(result),200

#   GET SPECIFIC MACHINE
@api.route('/machines/<string:id>',methods = ['GET'])
def get_machine(id : str):
    #check if id provided
    if not id:
        return jsonify({'error':'No Machine ID provided'}), 400 #bad request
    #check if id is valid
    try:
        id = int(id)
    except ValueError:
        return jsonify({'error' : 'Machine ID should be an integer!'}), 400 #bad request
    #check if id exists in machines
    machine = Machine.query.get(id)
    if not machine:
        return jsonify({'error' : f'Machine {id} not found!'}), 404 #not found
    return jsonify(machine.to_dict()), 200 #status ok


#------------------------------
#         PATCH-UPDATE
#------------------------------

@api.route('/machines', methods=['PATCH'])
def update():
    # expected fields with types
    machine_fields = {
        "machine_name": str,
        "last_number": str,
        "previous_last_number": str,
        "last_date": date,
        "Nec": str,
        "is_active": bool
    }

    result = []
    data = request.get_json(silent=True)
    if not data:
        return jsonify([{'error': 'no valid machines provided'}]), 400

    for machine in data:
        machine_id = machine.get("machine_id")
        if not isinstance(machine_id, int):
            result.append({'error': f'machine_id {machine_id} should be an integer'})
            continue

        m = Machine.query.get(machine_id)
        if not m:
            result.append({'error': f'machine_id {machine_id} not found'})
            continue

        for field, expected_type in machine_fields.items():
            if field in machine:
                value = machine[field]

                # type check and conversion for date
                #correct format year-month-date
                if expected_type == date:
                    if isinstance(value, str):
                        try:
                            value = datetime.strptime(value, "%Y-%m-%d").date()
                        except ValueError:
                            result.append({'error': f"invalid date format for field '{field}' in machine {machine_id}"})
                            continue
                    elif not isinstance(value, date):
                        result.append({'error': f"field '{field}' must be a date for machine {machine_id}"})
                        continue

                # type check for bool and str
                elif not isinstance(value, expected_type):
                    result.append({'error': f"field '{field}' must be {expected_type.__name__} for machine {machine_id}"})
                    continue

                setattr(m, field, value)
                result.append({'success': f"field '{field}' updated in machine {machine_id}"})

    db.session.commit()

    status_code = 200 if any('success' in r for r in result) else 400
    return jsonify(result), status_code


        
    
#------------------------------
#           DELETE
#------------------------------
@api.route('/machines/<string:id>',methods=['DELETE'])
def delete(id : str):
    machine = Machine.query.get(id)
    #check if machine exists
    if not machine:
        return jsonify({'error' : f'Machine {id} not found'}), 404 # not found
    db.session.delete(machine)
    db.session.commit()
    return jsonify({'status' : f'Machine {id} deleted'}), 200 #status code ok


#------------------------------
#           POST
#------------------------------
@api.route('/machines', methods=['POST'])
def add():
    from datetime import datetime, date

    # all fields and types
    machine_fields = {
        "machine_id": int,
        "machine_name": str,
        "last_number": str,
        "previous_last_number": str,
        "last_date": date,
        "Nec": str,
        "is_active": bool
    }

    # required fields
    required_fields = ["machine_id", "machine_name", "last_number", "last_date"]

    new_machines = request.get_json(silent=True)
    if not new_machines:
        return jsonify({'error': 'You have to enter the machines in a JSON format'}), 400

    result = []

    for machine in new_machines:
        # check nessecary fields
        missing_fields = [f for f in required_fields if f not in machine or machine[f] is None]
        if missing_fields:
            result.append({'error': f"missing required fields: {', '.join(missing_fields)}"})
            continue
        # check machine_name exists in machines_dictionary
        if machine["machine_name"] not in machine_dictionary:
            result.append({'error': f"machine_name '{machine['machine_name']}' not found in machines_dictionary"})
            continue

        # check if current id already exists
        machine_id = machine["machine_id"]
        m = Machine.query.get(machine_id)
        if m:
            result.append({'error': f"machine_id {machine_id} already exists"})
            continue

        # Create new machine
        new_machine = Machine(id=machine_id)

        # fill all fields
        for field, expected_type in machine_fields.items():
            if field not in machine:
                continue

            value = machine[field]

            # check if date format is correct
            if expected_type == date:
                if isinstance(value, str):
                    try:
                        value = datetime.strptime(value, "%Y-%m-%d").date()
                    except ValueError:
                        result.append({'error': f"invalid date format for field '{field}' in machine {machine_id}"})
                        break
                elif not isinstance(value, date):
                    result.append({'error': f"field '{field}' must be a date in machine {machine_id}"})
                    break

            # Check for appropriate types in json file
            elif not isinstance(value, expected_type):
                result.append({'error': f"field '{field}' must be {expected_type.__name__} in machine {machine_id}"})
                break

            setattr(new_machine, field, value)
        else:
            # add to db
            db.session.add(new_machine)
            result.append({'success': f"machine '{new_machine.machine_name}' added"})

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        result.append({'error': str(e)})
        return jsonify(result), 500

    status_code = 200 if any('success' in r for r in result) else 400
    return jsonify(result), status_code

