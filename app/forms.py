from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional


class AQIPredictionForm(FlaskForm):
    """
    Form for AQI prediction inputs
    """

    # Pollutants
    pm25 = FloatField(
        "PM2.5",
        validators=[DataRequired(), NumberRange(min=0, message="Must be >= 0")]
    )

    pm10 = FloatField(
        "PM10",
        validators=[DataRequired(), NumberRange(min=0)]
    )

    no2 = FloatField(
        "NO2",
        validators=[Optional(), NumberRange(min=0)]
    )

    so2 = FloatField(
        "SO2",
        validators=[Optional(), NumberRange(min=0)]
    )

    co = FloatField(
        "CO",
        validators=[Optional(), NumberRange(min=0)]
    )

    o3 = FloatField(
        "O3",
        validators=[Optional(), NumberRange(min=0)]
    )

    # Time-based inputs (optional but useful)
    month = FloatField(
        "Month (1-12)",
        validators=[Optional(), NumberRange(min=1, max=12)]
    )

    dayofweek = FloatField(
        "Day of Week (0=Mon, 6=Sun)",
        validators=[Optional(), NumberRange(min=0, max=6)]
    )

    # Submit button
    submit = SubmitField("Predict AQI")
