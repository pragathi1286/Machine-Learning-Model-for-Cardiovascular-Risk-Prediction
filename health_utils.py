def generate_health_advice(data):
    """
    Generates personalized health recommendations.
    """
    advice = []

    if data.get("currentSmoker", 0) == 1:
        advice.append("🚭 Quit smoking – it reduces heart disease risk by up to 50%.")
    if data.get("BPMeds", 0) == 1:
        advice.append("💊 Continue taking BP medication as prescribed.")
    if data.get("sysBP", 120) > 130 or data.get("diaBP", 80) > 85:
        advice.append("🩸 Monitor your blood pressure regularly and reduce salt intake.")
    if data.get("BMI", 25) > 25:
        advice.append("🥗 Maintain a balanced diet and exercise 30 mins daily.")
    if data.get("diabetes", 0) == 1:
        advice.append("🍎 Manage diabetes carefully with diet and regular check-ups.")
    if data.get("totChol", 180) > 200:
        advice.append("🥑 Reduce saturated fats and increase fiber intake.")
    if data.get("heartRate", 70) > 100:
        advice.append("💓 Practice relaxation or yoga to control heart rate.")

    if not advice:
        advice.append("✅ You’re maintaining a healthy lifestyle – keep it up!")

    return "\n".join(advice)


def calculate_heart_age(age, data):
    """
    Estimates heart age based on major cardiovascular risk factors.
    """
    sysBP = data.get("sysBP", 120)
    diaBP = data.get("diaBP", 80)
    totChol = data.get("totChol", 180)
    BMI = data.get("BMI", 25)
    diabetes = data.get("diabetes", 0)
    smoker = data.get("currentSmoker", 0)

    heart_age = age
    extra = 0

    if sysBP >= 160 or diaBP >= 100:
        extra += 10
    elif sysBP >= 140 or diaBP >= 90:
        extra += 7
    elif sysBP >= 130:
        extra += 4

    if totChol >= 240:
        extra += 5
    if BMI >= 30:
        extra += 5
    if diabetes == 1:
        extra += 8
    if smoker == 1:
        extra += 6

    heart_age = min(age + extra, age + 25)
    return int(heart_age)
        