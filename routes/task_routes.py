from flask import Blueprint, request, redirect, render_template, session
from models import db, Task, Project, User, ProjectMember
from datetime import datetime

task = Blueprint('task', __name__)

def require_login():
    user = User.query.get(session.get('user_id'))
    if not user:
        return None, redirect('/')
    return user, None

@task.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    # Guard: only logged-in user can see their own dashboard
    logged_in = User.query.get(session.get('user_id'))
    if not logged_in:
        return redirect('/')

    user     = User.query.get_or_404(user_id)
    tasks    = Task.query.filter_by(assigned_to=user_id).all()
    projects = Project.query.all()
    users    = User.query.all()
    now      = datetime.utcnow()

    # Mark overdue: pending tasks whose due_date has passed
    overdue_ids = {
        t.id for t in tasks
        if t.status == 'pending' and t.due_date and t.due_date < now
    }

    # Build project members map: { project_id: [User, ...] }
    memberships   = ProjectMember.query.all()
    project_members = {}
    for m in memberships:
        project_members.setdefault(m.project_id, []).append(User.query.get(m.user_id))

    return render_template(
        "dashboard.html",
        tasks=tasks,
        projects=projects,
        users=users,
        user=user,
        overdue_ids=overdue_ids,
        project_members=project_members,
        now=now
    )

@task.route('/create_task', methods=['POST'])
def create_task():
    user, err = require_login(), None
    user = User.query.get(session.get('user_id'))
    if not user or user.role != 'admin':
        return "Not allowed"

    data  = request.form
    title = data.get('title', '').strip()
    if not title:
        return redirect(f"/dashboard/{user.id}")

    due_date = None
    raw_due  = data.get('due_date', '').strip()
    if raw_due:
        try:
            due_date = datetime.strptime(raw_due, '%Y-%m-%d')
        except ValueError:
            pass

    new_task = Task(
        title       = title,
        project_id  = int(data['project_id']),
        assigned_to = int(data['assigned_to']),
        due_date    = due_date
    )
    db.session.add(new_task)
    db.session.commit()
    return redirect(f"/dashboard/{user.id}")

@task.route('/update_task/<int:id>')
def update_task(id):
    user = User.query.get(session.get('user_id'))
    if not user:
        return redirect('/')

    t = Task.query.get_or_404(id)

    # Only admin or the assigned user can mark done
    if user.role != 'admin' and t.assigned_to != user.id:
        return "Not allowed"

    t.status = 'done'
    db.session.commit()
    return redirect(f"/dashboard/{session['user_id']}")
