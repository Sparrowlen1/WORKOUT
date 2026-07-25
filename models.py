from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint, CheckConstraint
from sqlalchemy.orm import validates
from datetime import datetime

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='exercise',
        cascade='all, delete-orphan'
    )
    workouts = db.relationship(
        'Workout',
        secondary='workout_exercises',
        back_populates='exercises',
        viewonly=True
    )

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 2:
            raise ValueError("Exercise name must be at least 2 characters.")
        return name

    @validates('category')
    def validate_category(self, key, category):
        allowed = ['Cardio', 'Strength', 'Flexibility', 'Other']
        if category not in allowed:
            raise ValueError(f"Category must be one of {allowed}")
        return category

    def __repr__(self):
        return f'<Exercise {self.name}>'


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='workout',
        cascade='all, delete-orphan'
    )

    exercises = db.relationship(
        'Exercise',
        secondary='workout_exercises',
        back_populates='workouts',
        viewonly=True #setting ikuwe many to many readonly
    )

    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
    )

    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration <= 0:
            raise ValueError("Duration must be positive.")
        return duration

    @validates('date')
    def validate_date(self, key, date):
        if date > datetime.now().date():
            raise ValueError("Date cannot be in the future.")
        return date

    def __repr__(self):
        return f'<Workout {self.date}>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    __table_args__ = (
        UniqueConstraint('workout_id', 'exercise_id', name='unique_workout_exercise'),
        CheckConstraint('reps IS NULL OR reps > 0', name='check_reps_positive'),
        CheckConstraint('sets IS NULL OR sets > 0', name='check_sets_positive'),
        CheckConstraint('duration_seconds IS NULL OR duration_seconds > 0', name='check_duration_positive'),
    )

    @validates('reps')
    def validate_reps(self, key, reps):
        if reps is not None and reps <= 0:
            raise ValueError("Reps must be positive or None.")
        return reps

    @validates('sets')
    def validate_sets(self, key, sets):
        if sets is not None and sets <= 0:
            raise ValueError("Sets must be positive or None.")
        return sets

    @validates('duration_seconds')
    def validate_duration_seconds(self, key, duration):
        if duration is not None and duration <= 0:
            raise ValueError("Duration seconds must be positive or None.")
        return duration

    def __repr__(self):
        return f'<WorkoutExercise workout={self.workout_id} exercise={self.exercise_id}>'