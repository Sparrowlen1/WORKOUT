
from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():
    db.drop_all()
    db.create_all()

    e1 = Exercise(name="Push-up", category="Strength", equipment_needed=False)
    e2 = Exercise(name="Squat", category="Strength", equipment_needed=False)
    e3 = Exercise(name="Running", category="Cardio", equipment_needed=False)
    e4 = Exercise(name="Plank", category="Flexibility", equipment_needed=False)
    db.session.add_all([e1, e2, e3, e4])
    db.session.commit()

    w1 = Workout(date=date(2026, 7, 20), duration_minutes=30, notes="Morning workout")
    w2 = Workout(date=date(2026, 7, 21), duration_minutes=45, notes="Evening cardio")
    db.session.add_all([w1, w2])
    db.session.commit()

    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=e1.id, reps=15, sets=3)
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=e2.id, reps=20, sets=4)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=e3.id, duration_seconds=1800)
    we4 = WorkoutExercise(workout_id=w2.id, exercise_id=e4.id, reps=3, sets=1, duration_seconds=60)
    db.session.add_all([we1, we2, we3, we4])
    db.session.commit()

    print("Database seeded successfully.")