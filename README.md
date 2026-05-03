# TaskFlow — Team Task Manager

A full-stack web application for managing projects, assigning tasks, and tracking progress with **role-based access control (Admin / Member)**.

---


---

## 🚀 Features

### Authentication
- Signup with username, password, and role selection
- Login with hashed password verification (Werkzeug)
- Forgot password / reset password flow
- Session-based authentication
- Duplicate username validation and minimum password length enforcement

### Role-Based Access Control
| Action | Admin | Member |
|---|---|---|
| Create projects | ✅ | ❌ |
| Create & assign tasks | ✅ | ❌ |
| Add / remove team members | ✅ | ❌ |
| View dashboard | ✅ | ✅ |
| Mark tasks as done | ✅ | ✅ (own tasks only) |

### Project & Team Management
- Admins can create projects
- Admins can add or remove members from specific projects
- Each project displays its assigned team members

### Task Management
- Create tasks with a title, project, assigned user, and due date
- Tasks display status: **Pending**, **Done**, or **Overdue**
- Overdue tasks (pending + past due date) are highlighted in red
- Members can mark their own tasks as done

### Dashboard
- Stat cards: Total Tasks, Completed, Pending, Overdue
- Date filter bar: Today, This Week, This Month, This Quarter, or custom range
- Separate views for Dashboard Overview, My Tasks, and Projects (no page reload)
- Topbar updates dynamically based on the active view

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite (via SQLAlchemy ORM) |
| Auth | Flask Sessions, Werkzeug password hashing |
| Frontend | HTML, CSS, Vanilla JS (Jinja2 templates) |
| Deployment | Railway |

---

## 📁 Project Structure

```
taskflow/
│
├── app.py                  # App factory, blueprint registration
├── models.py               # SQLAlchemy models (User, Project, Task, ProjectMember)
│
├── routes/
│   ├── auth_routes.py      # Signup, login, logout, forgot password
│   ├── project_routes.py   # Create project, add/remove members
│   └── task_routes.py      # Dashboard, create task, update task
│
└── templates/
    ├── login.html          # Login + signup (tabbed)
    ├── forgot.html         # Reset password
    └── dashboard.html      # Main app dashboard
```

---

## ⚙️ Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/taskflow.git
cd taskflow
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install flask flask-sqlalchemy werkzeug
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
```
http://127.0.0.1:5000
```

The database (`db.sqlite3`) is created automatically on first run.

---

## 🗄️ Database Models

### User
| Field | Type | Constraints |
|---|---|---|
| id | Integer | Primary Key |
| username | String(100) | Unique, Not Null |
| password | String(200) | Not Null (hashed) |
| role | String(20) | Not Null (`admin` / `member`) |

### Project
| Field | Type | Constraints |
|---|---|---|
| id | Integer | Primary Key |
| name | String(100) | Not Null |
| created_at | DateTime | Default: now |

### Task
| Field | Type | Constraints |
|---|---|---|
| id | Integer | Primary Key |
| title | String(200) | Not Null |
| status | String(20) | Default: `pending` |
| created_at | DateTime | Default: now |
| due_date | DateTime | Nullable |
| project_id | Integer | ForeignKey → Project |
| assigned_to | Integer | ForeignKey → User |

### ProjectMember
| Field | Type | Constraints |
|---|---|---|
| id | Integer | Primary Key |
| project_id | Integer | ForeignKey → Project |
| user_id | Integer | ForeignKey → User |

---

## 🌐 API Routes

### Auth
| Method | Route | Description |
|---|---|---|
| GET | `/` | Login page |
| POST | `/signup` | Create new account |
| POST | `/login` | Login |
| GET | `/logout` | Logout |
| GET/POST | `/forgot` | Reset password |

### Dashboard & Tasks
| Method | Route | Description |
|---|---|---|
| GET | `/dashboard/<user_id>` | User dashboard |
| POST | `/create_task` | Create a task (admin only) |
| GET | `/update_task/<id>` | Mark task as done |

### Projects
| Method | Route | Description |
|---|---|---|
| POST | `/create_project` | Create a project (admin only) |
| POST | `/add_member` | Add user to project (admin only) |
| POST | `/remove_member` | Remove user from project (admin only) |

---

## 🚢 Deployment (Railway)

1. Push your code to a GitHub repository
2. Go to [railway.app](https://railway.app) and create a new project
3. Select **Deploy from GitHub repo** and choose your repository
4. Add the following environment variable in Railway settings:
   ```
   SECRET_KEY=your_secret_key_here
   ```
5. Railway will auto-detect Python and deploy — your live URL will appear in the dashboard

> **Note:** Update `app.secret_key` in `app.py` to read from environment variable before deploying:
> ```python
> import os
> app.secret_key = os.environ.get("SECRET_KEY", "fallback_secret")
> ```

---

## 👤 Author

- **Name:** _Your Name_
- **Email:** _your@email.com_
- **GitHub:** _github.com/your-username_
