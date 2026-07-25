from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    ExerciseSchema,
    WorkoutSchema,
    WorkoutExerciseSchema,
    WorkoutWithExercisesSchema,
    ExerciseWithWorkoutsSchema
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    schema = ExerciseSchema(many=True)
    return jsonify(schema.dump(exercises)), 200

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    schema = ExerciseWithWorkoutsSchema()
    return jsonify(schema.dump(exercise)), 200

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    schema = ExerciseSchema()
    errors = schema.validate(data)
    if errors:
        return make_response(jsonify(errors), 400)
    exercise = Exercise(**data)
    db.session.add(exercise)
    db.session.commit()
    return jsonify(schema.dump(exercise)), 201

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise) 
    db.session.commit()
    return make_response('', 204)


@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    schema = WorkoutSchema(many=True)
    return jsonify(schema.dump(workouts)), 200

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    schema = WorkoutWithExercisesSchema()
    return jsonify(schema.dump(workout)), 200

@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    schema = WorkoutSchema()
    errors = schema.validate(data)
    if errors:
        return make_response(jsonify(errors), 400)
    workout = Workout(**data)
    db.session.add(workout)
    db.session.commit()
    return jsonify(schema.dump(workout)), 201

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout) 
    db.session.commit()
    return make_response('', 204)

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get_or_404(workout_id)
    exercise = Exercise.query.get_or_404(exercise_id)

    data = request.get_json()
    schema = WorkoutExerciseSchema()
    errors = schema.validate(data)
    if errors:
        return make_response(jsonify(errors), 400)

    existing = WorkoutExercise.query.filter_by(workout_id=workout_id, exercise_id=exercise_id).first()
    if existing:
        return make_response(jsonify({"error": "Exercise already in workout"}), 409)

    we = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        reps=data.get('reps'),
        sets=data.get('sets'),
        duration_seconds=data.get('duration_seconds')
    )
    db.session.add(we)
    db.session.commit()
    return jsonify(schema.dump(we)), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)