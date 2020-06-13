from . import doctor
from flask import render_template,request,session,flash,redirect,url_for
from .utils import doctor_only_view
from .forms import LoginDoctor,SickDoctorForm,SearchForm
from mod_operator.models import Personnel,Sick
from mod_upload.forms import FileUploadForm
import uuid
from werkzeug.utils import secure_filename
from app import db
from sqlalchemy.exc import IntegrityError
from mod_upload.models import File
from sqlalchemy import or_

@doctor.route('/')
@doctor_only_view
def index():
    search_form = SearchForm()
    sicks=Sick.query.order_by(Sick.bimarid.desc())
    return render_template('doctor/index.html',sicks=sicks,search_form=search_form)
@doctor.route('/login',methods=['POST','GET'])
def login():
    search_form = SearchForm()
    form = LoginDoctor(request.form)
    personnelname = form.personnelname.data 
    password = form.password.data 
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Not Validate !!',category='danger')
            return render_template('admin/login.html',form=form,search_form=search_form)
        personnel = Personnel.query.filter(Personnel.personnelname == personnelname).first_or_404()
        if not personnel:
            flash('personnel Not Found !!',category='warning')
            return render_template('doctor/login.html',form=form,search_form=search_form)
        if not personnel.is_doctor():
            flash('personnel is Not Doctor !!',category='danger')
            return render_template('doctor/login.html',form=form,search_form=search_form)
        if not personnel.check_password(password):
            flash('Not Validate !!',category='danger')
            return render_template('doctor/login.html',form=form,search_form=search_form)
        session['DocName'] = personnel.personnelname
        session['Doc_id'] = personnel.personnelid 
        session['role'] = personnel.role
        flash('Loggedd in success',category='success')
        return redirect(url_for('doctor.index'))

    if session.get('Doc_id') is not None:
        flash('You all ready logged in !!',category='danger')
        return redirect(url_for('doctor.index'))

    return render_template('doctor/login.html',form=form,search_form=search_form)
@doctor.route('/logout')
@doctor_only_view
def logout():
    session.clear()
    flash('You Successfully log out')
    return redirect(url_for('doctor.login'))
@doctor.route('/create/sick/<int:sick_id>',methods=['POST','GET'])
@doctor_only_view
def create_sick(sick_id):
    search_form=SearchForm()
    sick = Sick.query.get_or_404(sick_id)
    form = SickDoctorForm(obj=sick)
    upload = FileUploadForm()

    notes=form.notes.data
    bimaritype=form.bimaritype.data
        
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Not Validate!!',category='warning')
            return render_template('doctor/create_sick.html',sick=sick,form=form,upload=upload,search_form=search_form)
        
        filename = f'{uuid.uuid1()}_{secure_filename(upload.file.data.filename)}'
        new_file = File()
        new_file.filename = filename

        sick.notes=notes
        sick.noskhe= url_for("static",filename="uploads/"+filename,_external=True)
        sick.bimaritype=bimaritype

        try:
            db.session.add(new_file)
            db.session.commit()
            upload.file.data.save(f'static/uploads/{filename}')
            flash(f'File Uploaded on {url_for("static",filename="uploads/"+filename,_external=True)}')
            db.session.commit()
            flash('Sick add !!',category='success')
            return redirect(url_for('doctor.index'))

        except IntegrityError:
            db.session.rollback()
            # breakpoint()
            flash('Slug is Use !!',category='danger')
            return render_template('doctor/create_sick.html',sick=sick,form=form,upload=upload,search_form=search_form)
    return render_template('doctor/create_sick.html',sick=sick,form=form,upload=upload,search_form=search_form)

@doctor.route('/sick/<int:sick_id>')
@doctor_only_view
def sick(sick_id):
    search_form = SearchForm()
    sick = Sick.query.filter(Sick.bimarid == sick_id).first_or_404()
    return render_template('doctor/sick.html',sick=sick,search_form=search_form)

@doctor.route('/upload',methods=['POST','GET'])
@doctor_only_view
def upload_file():
    form = FileUploadForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            # breakpoint()
            return '1'
        filename = f'{uuid.uuid1()}_{secure_filename(form.file.data.filename)}'
        new_file = File()
        new_file.filename = filename
        try:
            db.session.add(new_file)
            db.session.commit()
            form.file.data.save(f'static/uploads/{filename}')
            flash(f'File Uploaded on {url_for("static",filename="uploads/"+filename,_external=True)}')
        except IntegrityError:
            db.session.rollback()
            flash('Upload Failed')
    return render_template('doctor/upload_file.html',form=form)

@doctor.route('/search')
@doctor_only_view
def search_sick():
    search_form = SearchForm()
    search_query = request.args.get('search_query','')
    bimarname_cond = Sick.bimarname.ilike(f'%{search_query}%')
    mellicode_cond = Sick.mellicode.ilike(f'%{search_query}%')
    bimaritype_cond = Sick.bimaritype.ilike(f'%{search_query}%')
    found_sicks = Sick.query.filter(or_(bimarname_cond,
                                        mellicode_cond,
                                        bimaritype_cond)).all()
    return render_template('doctor/index.html',sicks=found_sicks,search_form=search_form)

@doctor.route('/list/sick')
@doctor_only_view
def list_sick():
    search_form = SearchForm()
    sicks = Sick.query.order_by(Sick.bimarid.desc()).all()
    return render_template('doctor/list_sick.html',sicks=sicks,search_form=search_form)

@doctor.route('/delete/sick/<int:sick_id>')
@doctor_only_view   
def delete_sick(sick_id):
    sick = Sick.query.get_or_404(sick_id)
    db.session.delete(sick)
    db.session.commit()
    flash('Delete sick success',category='success')
    return redirect(url_for('doctor.list_sick'))

