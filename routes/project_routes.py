from flask import Blueprint, request, redirect, session, jsonify
from models import db, Project, User, ProjectMember

project = Blueprint('project', __name__)

def require_admin():
    user = User.query.get(session.get('user_id'))
    if not user or user.role != 'admin':
        return None, "Not allowed"
    return user, None

@project.route('/create_project', methods=['POST'])
def create_project():
    user, err = require_admin()
    if err:
        return err

    name = request.form.get('name', '').strip()
    if not name:
        return redirect(f"/dashboard/{user.id}")

    new_project = Project(name=name)
    db.session.add(new_project)
    db.session.commit()
    return redirect(f"/dashboard/{user.id}")

@project.route('/add_member', methods=['POST'])
def add_member():
    user, err = require_admin()
    if err:
        return err

    project_id = request.form.get('project_id')
    user_id    = request.form.get('user_id')

    if not project_id or not user_id:
        return redirect(f"/dashboard/{user.id}")

    # Check project and user exist
    proj = Project.query.get(project_id)
    target = User.query.get(user_id)
    if not proj or not target:
        return redirect(f"/dashboard/{user.id}")

    # Avoid duplicate membership
    exists = ProjectMember.query.filter_by(project_id=project_id, user_id=user_id).first()
    if not exists:
        db.session.add(ProjectMember(project_id=int(project_id), user_id=int(user_id)))
        db.session.commit()

    return redirect(f"/dashboard/{user.id}")

@project.route('/remove_member', methods=['POST'])
def remove_member():
    user, err = require_admin()
    if err:
        return err

    project_id = request.form.get('project_id')
    user_id    = request.form.get('user_id')

    membership = ProjectMember.query.filter_by(project_id=project_id, user_id=user_id).first()
    if membership:
        db.session.delete(membership)
        db.session.commit()

    return redirect(f"/dashboard/{user.id}")
