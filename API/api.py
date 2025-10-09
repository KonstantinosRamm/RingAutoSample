from flask import Blueprint,jsonify
from app import db
from models import Machine


api = Blueprint("api",__name__)


#------------------------------
#           GET
#------------------------------

#   GET ALL MACHINES
@api.route('/get_all')
def get_all():
    #query all machines 
    machines = Machine.query.all()

    #convert all machines into dicts 
    result = [machine.to_dict() for machine in machines]
    return jsonify(result)


# GET A SPECIFIC MACHINE 
@api.route('/get_machine/', defaults={'machine_id': None})
@api.route('/get_machine/<string:machine_id>')
def get_machine(machine_id: str):
    # Check if machine ID was provided
    if machine_id is None:
        return jsonify({'error': "No machine ID provided"}), 400

    # Validate and convert to int
    try:
        machine_id = int(machine_id)
    except ValueError:
        return jsonify({'error': "Machine ID must be a number"}), 400  # Bad request

    # Try to get machine from DB
    m = Machine.query.get(machine_id)
    if not m:
        return jsonify({"error": f"Machine with ID {machine_id} does not exist"}), 404 #not found

    return jsonify(m.to_dict()), 200 #status code ok


#------------------------------
#           UPDATE
#------------------------------


#------------------------------
#           DELETE
#------------------------------
@api.route('/delete/', defaults={'machine_id': None})
@api.route('/delete/<string:machine_id>', methods=['GET','DELETE'])
def delete(machine_id: str):
    if not machine_id:
        return jsonify({"error":"No Machine id provided"}), 400 #bad request
    #check if machine id is valid
    try:
        machine_id = int(machine_id)
    except ValueError:
        return jsonify({'error': "Machine ID must be a number"}), 400  # Bad request

    #check if exists 
    m = Machine.query.get(machine_id)
    if not m:
        return jsonify({'error' : f"Machine {machine_id} not found"}), 404 #not found
    
    # delete the machine
    db.session.delete(m)
    db.session.commit()
    return jsonify({'message': f'Machine with ID {machine_id} deleted successfully'}), 200#status code ok
    


#------------------------------
#        CREATE-POST
#------------------------------