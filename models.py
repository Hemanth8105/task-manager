from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Association table for Project <-> Member (team management)
class ProjectMember(db.Model):
    __tablename__ = 'project_members'
    id         = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'), nullable=False)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id',    ondelete='CASCADE'), nullable=False)
    __table_args__ = (db.UniqueConstraint('project_id', 'user_id', name='uq_project_member'),)

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role     = db.Column(db.String(20),  nullable=False, default='member')

    # relationships
    tasks    = db.relationship('Task',          backref='assignee',  lazy=True, foreign_keys='Task.assigned_to')
    projects = db.relationship('ProjectMember', backref='member',    lazy=True)

class Project(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    tasks   = db.relationship('Task',          backref='project', lazy=True, cascade='all, delete-orphan')
    members = db.relationship('ProjectMember', backref='project', lazy=True, cascade='all, delete-orphan')

class Task(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    status      = db.Column(db.String(20),  nullable=False, default='pending')
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    due_date    = db.Column(db.DateTime, nullable=True)
    project_id  = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id',    ondelete='CASCADE'), nullable=False)
