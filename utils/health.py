def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

def get_ideal_bmi_range(age, gender):
    gender = gender.lower()
    if gender == "female":
        if age < 25:
            return (18.5, 23.5)
        elif age < 40:
            return (19.0, 24.0)
        elif age < 60:
            return (20.0, 25.0)
        else:
            return (21.0, 26.0)
    else:  
        if age < 25:
            return (19.0, 24.0)
        elif age < 40:
            return (20.0, 25.0)
        elif age < 60:
            return (21.0, 26.0)
        else:
            return (22.0, 27.0)

def bmi_score_by_age_gender(bmi, age, gender):
    lower, upper = get_ideal_bmi_range(age, gender)
    if lower <= bmi <= upper:
        return 34
    elif lower - 1 <= bmi < lower or upper < bmi <= upper + 1:
        return 17
    else:
        return 8

def calculate_health_score(sleep_hours, exercise_minutes, weight_kg, height_cm, age, gender):
   
    if 7 <= sleep_hours <= 9:
        sleep_score = 33
    elif 6 <= sleep_hours < 7 or 9 < sleep_hours <= 10:
        sleep_score = 22
    else:
        sleep_score = 11

    
    if exercise_minutes >= 30:
        exercise_score = 33
    elif exercise_minutes >= 15:
        exercise_score = 22
    else:
        exercise_score = 11

    bmi = calculate_bmi(weight_kg, height_cm)
    bmi_score = bmi_score_by_age_gender(bmi, age, gender)

    final_score = sleep_score + exercise_score + bmi_score
    return final_score
