# Smart Study Tracker

A web-based task management system designed to help students organise their study workload.

## Features
- Add, edit, delete tasks
- Mark tasks as complete
- Filter by module and date
- Persistent storage using SQLite database
- REST API built with Flask

## Project Structure
- frontend/ → user interface
- backend/ → Flask API + database
- docs/ → reports and evidence

## How to Run

1. Install dependencies:
pip install flask

2. Run backend:
python backend/app.py

3. Open frontend:
Open frontend/index.html in browser

## API Endpoints
- GET /tasks
- POST /tasks
- PUT /tasks/<id>
- DELETE /tasks/<id>
