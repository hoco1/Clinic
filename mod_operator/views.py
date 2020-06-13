from . import operator
from app import db
from flask import render_template,request,session,flash,redirect,url_for
from .utils import operator_only_view
from .forms import LoginOperator,PersonnelForm,SickForm,SearchForm
from .models import Sick,Personnel
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

@operator.route('/')
@operator_only_view
def index():
    personnels=Personnel.query.all()
    search_form = SearchForm()
    return render_template('operator/index.html',personnels=personnels,search_form=search_form)

@operator.route('/login',methods=['POST','GET'])
def login():
    search_form = SearchForm()
    form = LoginOperator(request.form)
    personnelname = form.personnelname.data 
    password = form.password.data 
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Not Validate !!',category='danger')
            return render_template('operator/login.html',form=form,search_form=search_form)
        personnel = Personnel.query.filter(Personnel.personnelname == personnelname).first_or_404()
        if not personnel:
            flash('personnel Not Found !!',category='warning')
            return render_template('operator/login.html',form=form,search_form=search_form)
        if not personnel.is_operator():
            flash('personnel is Not Operator !!',category='danger')
            return render_template('operator/login.html',form=form,search_form=search_form)
        if not personnel.check_password(password):
            flash('Not Validate !!',category='danger')
            return render_template('doctor/login.html',form=form,search_form=search_form)
        session['OpName'] = personnel.personnelname
        session['Op_id'] = personnel.personnelid 
        session['role'] = personnel.role
        flash('Loggedd in success',category='success')
        return redirect(url_for('operator.index'))

    if session.get('Op_id') is not None:
        flash('You all ready logged in !!',category='danger')
        return redirect(url_for('operator.index'))

    return render_template('operator/login.html',form=form,search_form=search_form)

@operator.route('/logout')
@operator_only_view
def logout():
    session.clear()
    flash('You Successfully log out')
    return redirect(url_for('operator.login'))

@operator.route('/create/personnel',methods=['POST','GET'])
@operator_only_view
def create_personnel():
    form = PersonnelForm(request.form)
    search_form = SearchForm()
    sicks = Sick.query.order_by(Sick.bimarid.asc()).all()
    form.sicks.choices = [(sick.bimarid,sick.bimarname) for sick in sicks]

    roles = {1:'Doctor',2:'nurse',3:'Operator'}
    form.role.choices = [(k,v) for k,v in roles.items()]

    personnelname=form.personnelname.data
    madraktype=form.madraktype.data
    phone=form.phone.data
    mobile=form.mobile.data
    mellicode=form.mellicode.data
    address=form.address.data
    password=form.password.data
    confirm_pass=form.confirm_pass.data
    role = form.role.data

    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Not Validate!!',category='warning')
            return render_template('operator/create_personnel.html',form=form,search_form=search_form)
        if not password == confirm_pass:
            flash('Not Equal !!',category='warning')
            return render_template('operator/create_personnel.html',form=form,search_form=search_form)

        new_personnel = Personnel()
        new_personnel.personnelname = personnelname
        new_personnel.madraktype=madraktype
        new_personnel.phone=phone
        new_personnel.mobile=mobile
        new_personnel.mellicode=mellicode
        new_personnel.address=address
        new_personnel.role=role[0] 
        new_personnel.set_password(password)
        new_personnel.sicks = [Sick.query.get(sick_id) for sick_id in form.sicks.data]
        try:
            db.session.add(new_personnel)
            db.session.commit()
            flash('New Personnel add !!',category='success')
            return redirect(url_for('operator.index'))

        except IntegrityError:
            db.session.rollback()
            flash('Slug is Use !!',category='danger')
            return render_template('operator/create_personnel.html',form=form,search_form=search_form)
    return render_template('operator/create_personnel.html',form=form,search_form=search_form)

@operator.route('/create/sick',methods=['POST','GET'])
@operator_only_view
def create_sick():
    search_form = SearchForm()
    form = SickForm(request.form)
 
    personnels = Personnel.query.order_by(Personnel.personnelid.asc()).all()
    form.personnels.choices = [(personnel.personnelid,personnel.personnelname) for personnel in personnels]


    bimetypes = {1:'BimehSalamat' , 2:'BimehTamin',3:'BimehComplete' }
    haghalzahmehtype = {1:'CashPayment',2:'CreditCard'}
    
    form.bimetype.choices = [(k,v) for k,v in bimetypes.items()]
    form.haghalzahmeh.choices = [(k,v) for k,v in haghalzahmehtype.items()]

    bimarname=form.bimarname.data
    bimehcode=form.bimehcode.data
    telph=form.telph.data
    mobile=form.mobile.data
    mellicode=form.mellicode.data
    address=form.address.data
    notes=form.notes.data
    bimetype=form.bimetype.data
    haghalzahmeh=form.haghalzahmeh.data

    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Not Validate!!',category='warning')
            return render_template('operator/create_sick.html',form=form,search_form=search_form)
        
        new_sick = Sick()
        new_sick.bimarname = bimarname
        new_sick.bimehcode=bimehcode
        new_sick.telph=telph
        new_sick.mobile=mobile
        new_sick.mellicode=mellicode
        new_sick.address=address
        new_sick.notes=notes
        new_sick.bimetypeid=bimetype[0]
        new_sick.haghalzahmehid=haghalzahmeh[0]
        new_sick.personnels=[Personnel.query.get(personnel_id) for personnel_id in form.personnels.data]
        try:
            db.session.add(new_sick)
            db.session.commit()
            flash('Sick add !!',category='success')
            return redirect(url_for('operator.index'))

        except IntegrityError:
            db.session.rollback()
            flash('Slug is Use !!',category='danger')
            return render_template('operator/create_sick.html',form=form,search_form=search_form)
    return render_template('operator/create_sick.html',form=form,search_form=search_form)

@operator.route('/list/sick')
@operator_only_view
def list_sick():
    search_form = SearchForm()
    sicks = Sick.query.order_by(Sick.bimarid.desc()).all()
    return render_template('operator/list_sick.html',sicks=sicks,search_form=search_form)

@operator.route('/list/personnel')
@operator_only_view
def list_personnel():
    search_form = SearchForm()
    personnels = Personnel.query.order_by(Personnel.personnelid.desc()).all()
    return render_template('operator/list_personnel.html',personnels=personnels,search_form=search_form)

@operator.route('/delete/sick/<int:sick_id>',methods=['POST','GET'])
@operator_only_view
def delete_sick(sick_id):
    sick = Sick.query.get_or_404(sick_id)
    db.session.delete(sick)
    db.session.commit()
    flash('Delete sick success',category='success')
    return redirect(url_for('operator.list_sick'))

@operator.route('/delete/personnel/<int:personnel_id>',methods=['POST','GET'])
@operator_only_view
def delete_personnel(personnel_id):
    personnel = Personnel.query.get_or_404(personnel_id)
    db.session.delete(personnel)
    db.session.commit()
    flash('Delete Personnel success',category='success')
    return redirect(url_for('operator.list_personnel'))

@operator.route('/modify/sick/<int:sick_id>',methods=['POST','GET'])
@operator_only_view
def modify_sick(sick_id):
    search_form = SearchForm()
    sick = Sick.query.get_or_404(sick_id)
    form = SickForm(obj=sick)

    personnels = Personnel.query.order_by(Personnel.personnelid.asc()).all()
    form.personnels.choices = [(personnel.personnelid,personnel.personnelname) for personnel in personnels]

    bimetypes = {1:'BimehSalamat' , 2:'BimehTamin',3:'BimehComplete' }
    haghalzahmehtype = {1:'CashPayment',2:'CreditCard'}
    
    form.bimetype.choices = [(k,v) for k,v in bimetypes.items()]
    form.haghalzahmeh.choices = [(k,v) for k,v in haghalzahmehtype.items()]

    bimarname=form.bimarname.data
    bimehcode=form.bimehcode.data
    telph=form.telph.data
    mobile=form.mobile.data
    mellicode=form.mellicode.data
    address=form.address.data
    notes=form.notes.data
    bimetype=form.bimetype.data
    haghalzahmeh=form.haghalzahmeh.data

    if request.method != 'POST':
        form.personnels.data = [personnels.personnelid for personnels in sick.personnels]
        form.bimetype.data=[sick.bimetypeid]
        form.haghalzahmeh.data=[sick.haghalzahmehid]

    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Not Validate !!',category='warning')
            return render_template('operator/modify_sick.html',form=form,sick=sick,search_form=search_form)

        sick.bimarname = bimarname
        sick.bimehcode=bimehcode
        sick.telph=telph
        sick.mobile=mobile
        sick.mellicode=mellicode
        sick.address=address
        sick.notes=notes
        sick.bimetypeid=bimetype[0]
        sick.haghalzahmehid=haghalzahmeh[0]
        sick.personnels=[Personnel.query.get(personnel_id) for personnel_id in form.personnels.data]

        try:
            db.session.commit()
            flash('Modify success',category='success')
            return redirect(url_for('operator.list_sick'))
        except IntegrityError:
            db.session.rollback()
            flash('Intergirty Error',category='warning')
            return render_template('operator/modify_sick.html',form=form,sick=sick,search_form=search_form)
    return render_template('operator/modify_sick.html',form=form,sick=sick,search_form=search_form)

@operator.route('/personnel/<int:personnel_id>')
@operator_only_view
def personnel(personnel_id):
    search_form = SearchForm()
    personnel = Personnel.query.filter(Personnel.personnelid == personnel_id).first_or_404()
    return render_template('operator/personnel.html',personnel=personnel,search_form=search_form)

@operator.route('/search')
@operator_only_view
def search_personnel():
    search_form = SearchForm()
    search_query = request.args.get('search_query','')
    personnelname_cond = Personnel.personnelname.ilike(f'%{search_query}%')
    madraktype_cond = Personnel.madraktype.ilike(f'%{search_query}%')
    role_cond = Personnel.role.ilike(f'%{search_query}%')
    found_personnels = Personnel.query.filter(or_(personnelname_cond,
                                        madraktype_cond,
                                        role_cond)).all()
    return render_template('operator/index.html',personnels=found_personnels,search_form=search_form)