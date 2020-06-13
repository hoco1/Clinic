from . import nurse
from flask import render_template,redirect,request,url_for,flash,session
from .utils import nurse_only_view
from mod_operator.models import Sick,Personnel,sicks_personnels
from .forms import ResNoskhe,SearchForm,LoginNurse
from sqlalchemy.exc import IntegrityError
from app import db
from sqlalchemy import or_

@nurse.route('/')
@nurse_only_view
def index():
    search_form = SearchForm()
    sicks=Sick.query.order_by(Sick.bimarid.desc())
    return render_template('nurse/index.html',sicks=sicks,search_form=search_form)

@nurse.route('/login',methods=['POST','GET'])
def login():
    search_form = SearchForm()
    form = LoginNurse(request.form)
    personnelname = form.personnelname.data 
    password = form.password.data 
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Not Validate !!',category='danger')
            return render_template('nurse/login.html',form=form,search_form=search_form)
        personnel = Personnel.query.filter(Personnel.personnelname == personnelname).first_or_404()
        if not personnel:
            flash('personnel Not Found !!',category='warning')
            return render_template('nurse/login.html',form=form,search_form=search_form)
        if not personnel.is_nurse():
            flash('personnel is Not Operator !!',category='danger')
            return render_template('nurse/login.html',form=form,search_form=search_form)
        if not personnel.check_password(password):
            flash('Not Validate !!',category='danger')
            return render_template('doctor/login.html',form=form,search_form=search_form)
        session['NurseName'] = personnel.personnelname
        session['Nurse_id'] = personnel.personnelid 
        session['role'] = personnel.role
        flash('Loggedd in success',category='success')
        return redirect(url_for('nurse.index'))

    if session.get('Nurse_id') is not None:
        flash('You all ready logged in !!',category='danger')
        return redirect(url_for('nurse.index'))

    return render_template('nurse/login.html',form=form,search_form=search_form)

@nurse.route('/res/sick/<int:sick_id>',methods=['POST','GET'])
@nurse_only_view
def ressick(sick_id):
    search_form = SearchForm()
    sick = Sick.query.get_or_404(sick_id)
    form = ResNoskhe(obj=sick)

    results = {1:'Accept',2:'Reject'}
    form.result.choices = [(k,v) for k,v in results.items()]
    result = form.result.data
    if request.method != 'POST':
        form.result.data=[sick.resnoskheid]

    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Not validate!!')
            return render_template('nurse/ressick.html',sick=sick,form=form,search_form=search_form)
        sick.resnoskheid = result[0]
        try:
            db.session.commit()
            flash('Message add')
            return redirect(url_for('nurse.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Integirty Error')
            return render_template('nurse/ressick.html',sick=sick,form=form,search_form=search_form)
        
    return render_template('nurse/ressick.html',sick=sick,form=form,search_form=search_form)
@nurse.route('/serch')
@nurse_only_view
def search_sick():
    search_form = SearchForm()
    search_query = request.args.get('search_query','')
    bimarname_cond = Sick.bimarname.ilike(f'%{search_query}%')
    mellicode_cond = Sick.mellicode.ilike(f'%{search_query}%')
    bimaritype_cond = Sick.bimaritype.ilike(f'%{search_query}%')
    found_sicks = Sick.query.filter(or_(bimarname_cond,
                                        mellicode_cond,
                                        bimaritype_cond)).all()
    return render_template('nurse/index.html',sicks=found_sicks,search_form=search_form)

@nurse.route('/sick/<int:sick_id>')
@nurse_only_view
def sick(sick_id):
    search_form = SearchForm()
    sick = Sick.query.filter(Sick.bimarid == sick_id).first_or_404()
    return render_template('nurse/sick.html',sick=sick,search_form=search_form)

@nurse.route('/logout')
@nurse_only_view
def logout():
    session.clear()
    flash('You Successfully log out')
    return redirect(url_for('nurse.login'))