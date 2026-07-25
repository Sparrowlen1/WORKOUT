from marshmallow import Schema, fields, validate, ValidationError, post_load

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, error="Name must be at least 2 characters"))
    category = fields.Str(required=True, validate=validate.OneOf(['Cardio', 'Strength', 'Flexibility', 'Other'], error="Invalid category"))
    equipment_needed = fields.Bool()

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True, format='%Y-%m-%d')
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, error="Duration must be positive"))
    notes = fields.Str(allow_none=True)

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1, error="Reps must be positive"))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1, error="Sets must be positive"))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=1, error="Duration seconds must be positive"))

    @post_load
    def validate_at_least_one(self, data, **kwargs):
        reps = data.get('reps')
        sets = data.get('sets')
        duration = data.get('duration_seconds')
        if reps is None and sets is None and duration is None:
            raise ValidationError("At least one of reps, sets, or duration_seconds must be provided.")
        return data


class WorkoutWithExercisesSchema(WorkoutSchema):
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)
    exercises = fields.Nested(ExerciseSchema, many=True, dump_only=True)

class ExerciseWithWorkoutsSchema(ExerciseSchema):
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)