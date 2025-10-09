from flask import Blueprint,jsonify
from app import db
from models import Machine


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
#        CREATE-POST
#------------------------------