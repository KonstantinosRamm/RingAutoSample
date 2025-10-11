from flask import Blueprint,jsonify,request
from app import db
from models import Machine
from datetime import datetime
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
#           UPDATE
#------------------------------


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

    new_machine = request.get_json(silent=True)#set silent to true so we inform user in case of wrong data format

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