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
from datetime import datetime, date

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
#        POST
#------------------------------
@api.route('/machines', methods=['POST'])
def add():
    #read json file 

    new_machine = request.get_json(silent=True)#set silent to true so we do not  inform user in case of wrong data format

    if new_machine is None:
        return jsonify({'error' : 'You have to enter the machine in a json format'}), 400 #bad request
    
    #check if id and machine type available
    #id-machine_name
    required_fields = ['id','machine_name']
    missing_fields = [f for f in required_fields if f not in new_machine]

    #return error to user if any of the fields missing
    if missing_fields:
        return jsonify({'error' : f'you have to enter all fields {missing_fields}'})
    
    #check if values of each key is the correct type
    if not isinstance(new_machine.get('id'),int):
        return jsonify({'error' : 'id should be an int'}),400 # bad request
    if not isinstance(new_machine.get('machine_name'),str):
        return jsonify({'error' : 'machine_name should be a string'}),400 # bad request
    

    #read the entries of the json into variables
    machine_id = new_machine['id']
    

    #check if machine in machine dictionary
    machine_name = new_machine['machine_name']

    if machine_name not in machine_dictionary:
        return jsonify({'error' : 'Machine type-name is not registered'}),400 #bad request

    #check for the given id if already in db 
    existent_machine = Machine.query.get(machine_id)
    if existent_machine:
        return jsonify({'error' : f'machine id: {machine_id} already exists'}),409 #conflict
    
    new_machine_to_add = Machine(machine_name=machine_name,id=machine_id,last_number="",last_date=datetime.today())

    #add to db machine to db
    db.session.add(new_machine_to_add)
    db.session.commit()


    return jsonify({'success' : f'machine {machine_name}-{machine_id} added'}), 200 #status code ok