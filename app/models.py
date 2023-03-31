from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Role model
class Role(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50), nullable=False, unique=True)

# Association table for User and Organization many-to-many relationship
user_organization = db.Table(
    'user_organization',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('user.id'), primary_key=True),
    db.Column('organization_id', UUID(as_uuid=True), db.ForeignKey('organization.id'), primary_key=True),
    db.Column('role_id', UUID(as_uuid=True), db.ForeignKey('role.id'), nullable=False),
    db.Column('start_date', db.Date, nullable=False),
    db.Column('end_date', db.Date, nullable=True)
)

class Organization(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    tax_id_number = db.Column(db.String(30), nullable=False)
    owning_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)

    owning_user = db.relationship('User', back_populates='owned_organizations')
    transformations = db.relationship('Transformation', backref='organization', lazy='dynamic')

class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auth0_id = db.Column(db.String(100), nullable=False, unique=True)
    tags = db.Column(db.String(255), nullable=True)

    owned_organizations = db.relationship('Organization', back_populates='owning_user')
    organizations = db.relationship('Organization', secondary=user_organization, backref=db.backref('users', lazy='dynamic'))

class Transformation(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    input_file = db.Column(db.String(255), nullable=False)
    output_file = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), nullable=False)
    organization_id = db.Column(UUID(as_uuid=True), db.ForeignKey('organization.id'), nullable=False)
    owner_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)

    owner = db.relationship('User', backref=db.backref('transformations', lazy='dynamic'))
