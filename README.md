# Workout Application Backend

## Description
A Flask‑SQLAlchemy API for personal trainers to manage workouts and exercises.  
It supports creation, listing, and deletion of workouts/exercises, and the ability to add exercises to a workout with sets, reps, or duration.

## Installation
1. Clone the repository:  
   `git clone <repo-url>`
2. Install dependencies with Pipenv:  
   `pipenv install`
3. Activate the virtual environment:  
   `pipenv shell`
4. Set up the database:  
   `flask db upgrade head`
5. (Optional) Seed the database:  
   `python seed.py`

## Run Instructions
Start the Flask development server:  
`flask run`  
or  
`python app.py`  
The API will be available at `http://localhost:5555`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/exercises` | List all exercises. |
| GET | `/exercises/<id>` | Get a single exercise with its associated workouts. |
| POST | `/exercises` | Create a new exercise (requires `name`, `category`, `equipment_needed`). |
| DELETE | `/exercises/<id>` | Delete an exercise (cascade deletes its associations). |
| GET | `/workouts` | List all workouts. |
| GET | `/workouts/<id>` | Get a single workout with its exercises and details (reps/sets/duration). |
| POST | `/workouts` | Create a new workout (requires `date`, `duration_minutes`, `notes` optional). |
| DELETE | `/workouts/<id>` | Delete a workout (cascade deletes its associations). |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout. Provide JSON with `reps`, `sets`, and/or `duration_seconds` (at least one required). |

## Technologies
- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 3.1.0
- Marshmallow 3.20.1
- SQLite
- Python 3.8+