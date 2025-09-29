from flask import Flask,redirect,url_for,render_template,session,request,flash
from datetime import date,datetime
from models import db,Machine
from machines import *
import secrets


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#connect database to current app
db.init_app(app)


#---------------------------------
#           index page
#---------------------------------

@app.route('/',methods = ['POST','GET'])
def index():
    #make a query to get all machines
    machines = Machine.query.filter_by(is_active=True).order_by(Machine.last_date).all()
    if request.method == 'POST':
        selected_machines = request.form.getlist('selected_machines')
        
        #convert to int
        selected_machines = list(map(int,selected_machines))
        for machine in machines:
            if machine.id in selected_machines:
                numbers = get_next_numbers(machine.id,machine.last_number)
                machine.last_number = f"{numbers[0]}-{numbers[1]}"#update number
                machine.last_date = date.today()
        #commit to database
        db.session.commit()
        #sort again
        machines.sort(key=lambda m: m.last_date)
    return render_template('index.html', machines = machines)



#---------------------------------
#           MACHINES EDIT
#---------------------------------
@app.route('/edit',methods = ['POST','GET'])
def edit():
    machines = Machine.query.order_by(Machine.last_date).all()
    #get all changes
    if request.method == 'POST':
        #check for modifications
        modified = False
        for machine in machines:
            last_number = request.form.get(f'last_number_{machine.id}')
            last_date = request.form.get(f'last_date_{machine.id}')
            nec = request.form.get(f'nec_{machine.id}')

            #update all machines
            if last_number and last_number != machine.last_number:
                machine.last_number = last_number
                modified = True
            if last_date:
                #first parse the date as string to compare with db
                parsed_date = datetime.strptime(last_date, "%Y-%m-%d").date()
                if parsed_date != machine.last_date:
                    machine.last_date = parsed_date
                    modified = True

            if nec and nec != machine.Nec:
                machine.Nec = nec
                modified = True


        #sort the db again if modifications occured
        if modified:
            machines.sort(key = lambda x : x.last_date)
        #update db
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', machines = machines)





#---------------------------------
#           ALL MACHINES
#---------------------------------
@app.route('/machines',methods=['POST','GET'])
def machines():


    # get all machines no matter if active or not
    all_machines = Machine.query.order_by(Machine.id).all()
    if request.method == "POST":
        
        machine_id = request.form.get("status_change")
        #get the selected machine to change its status 
        if machine_id:
            machine = db.session.get(Machine,int(machine_id))
            if machine:
                machine.is_active = not machine.is_active
                db.session.commit()
    #request method = post
    return render_template('machines.html',all_machines = all_machines)


#---------------------------------
#           ADD MACHINE
#---------------------------------
@app.route('/add',methods=['POST','GET'])
def add():
    if request.method == 'POST':
        id = request.form.get('machine_id')
        #check if id already in database or if valid
        if not id.isdigit():
            flash('id should be consisted of numbers only', 'danger')
            return redirect(url_for('add'))
        
        id_exists = db.session.get(Machine,int(id))
        if id_exists :
            flash(f'{id} already exists', 'danger')
            return redirect(url_for('add'))
        
        machine_name = request.form.get('machine_type')
        if not machine_name:
            flash()
            #check if all fields filled
        if not machine_name or machine_name == '':
            flash('machine type must be filled','danger')
        #check if machine already in registered machine types
        if machine_name in machine_dictionary:
            new_machine = Machine(machine_name=machine_name,id=int(id),last_number="",last_date=datetime.today())
            db.session.add(new_machine)
            db.session.commit()
            flash('machine added','success')       
    return render_template('add.html')


#---------------------------------
#           DELETE MACHINE
#---------------------------------
@app.route('/delete',methods=['POST','GET'])
def delete():
    machines = Machine.query.order_by(Machine.id).all()
    #get checked ids
    machines_to_delete = request.form.getlist('available_machines')
    machine_ids = [int(id) for id in machines_to_delete]

    #delete machines
    for machine in machines:
        if machine.id in machine_ids:
            db.session.delete(machine)
    db.session.commit()
    machines = Machine.query.order_by(Machine.id).all()
    return render_template('delete.html', machines=machines)

#---------------------------------
#           HANDLE ERROR 500
#---------------------------------
@app.errorhandler(500)
def error500(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()

