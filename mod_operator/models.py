from app import db
from sqlalchemy import DateTime,Column,Text,Integer,String,Table,ForeignKey
import datetime as dt
from werkzeug.security import generate_password_hash,check_password_hash

sicks_personnels = Table('sicks_personnels',db.metadata,
        Column('sicks_id',Integer,ForeignKey('sicks.bimarid',ondelete='cascade')),
        Column('personnels_id',Integer,ForeignKey('personnels.personnelid',ondelete='cascade'))
)

class Sick(db.Model):
        __tablename__ = 'sicks'
        bimarid=Column(Integer,primary_key=True)
        bimarname=Column(String(128),nullable=True , unique=False )
        datesabt=Column(DateTime(),nullable=False , unique=False ,default=dt.datetime.utcnow )
        bimehcode=Column(Text,nullable=False , unique=False )
        telph=Column(Text,nullable=False , unique=False )
        mobile=Column(Text,nullable=False , unique=False )
        mellicode=Column(Text,nullable=False , unique=False )
        address=Column(Text,nullable=False , unique=False )
        notes=Column(Text,nullable=True , unique=False )

        bimaritype=Column(Text,nullable=False , unique=False,default='None' )
        bimetypeid=Column(Integer,nullable=False , unique=False ,default='0' )
        haghalzahmehid=Column(Integer,nullable=False , unique=False )
        resnoskheid=Column(Integer,nullable=True , unique=False,default='2')

        noskhe=Column(String(128),nullable=False , unique=False ,default='None')

        personnels = db.relationship('Personnel',secondary=sicks_personnels,back_populates='sicks')

class Personnel(db.Model):
        __tablename__ = 'personnels'
        personnelid=Column(Integer,primary_key=True) 
        personnelname=Column(String(128),nullable=False , unique=True )
        madraktype=Column(String(128),nullable=True , unique=False )
        phone=Column(Text,nullable=False , unique=False )
        mobile=Column(Text,nullable=True , unique=True ) 
        mellicode=Column(Text,nullable=False , unique=False ) 
        dateestekhdam=Column(DateTime(),nullable=False , unique=False,default=dt.datetime.utcnow )
        address=Column(Text,nullable=True , unique=False ) 
        role=Column(Integer,nullable= False, default = 0)
        password=Column(String(128),nullable= False , unique=False) 
        sicks = db.relationship('Sick',secondary=sicks_personnels,back_populates='personnels')
        def set_password(self,password):
                self.password = generate_password_hash(password)
        def check_password(self,password):
                return check_password_hash(self.password,password)
        def is_doctor(self):
                return self.role == 1
        def is_nurse(self):
                return self.role == 2
        def is_operator(self):
                return self.role == 3


        
