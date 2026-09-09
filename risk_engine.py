def calculate_risk(game_results):
    """
    Prototype wellbeing risk engine.

    This does NOT diagnose depression, anxiety, or any
    mental-health condition.

    It identifies patterns that may indicate a need
    for a wellbeing check-in.
    """

    if not game_results:
        return {
            "risk_score": 0,
            "risk_level": "low",
            "signals": [],
            "message": "Not enough activity data yet."
        }

    risk_score = 0
    signals = []

    # -------------------------------------------------
    # 1. Look at recent results
    # -------------------------------------------------

    recent_results = game_results[-5:]

    scores = [
        r.score
        for r in recent_results
        if r.score is not None
    ]

    # -------------------------------------------------
    # 2. Low game performance signal
    # -------------------------------------------------

    if scores:
        average_score = sum(scores) / len(scores)

        if average_score < 40:
            risk_score += 30
            signals.append("Consistently low activity performance")

        elif average_score < 60:
            risk_score += 15
            signals.append("Lower-than-usual activity performance")

    # -------------------------------------------------
    # 3. Reaction / response time signal
    # -------------------------------------------------

    response_times = []

    for result in recent_results:
        if result.time_taken is not None:
            response_times.append(result.time_taken)

    if response_times:
        average_time = sum(response_times) / len(response_times)

        if average_time > 10:
            risk_score += 15
            signals.append("Slower response pattern")

    # -------------------------------------------------
    # 4. Accuracy signal
    # -------------------------------------------------

    accuracies = [
        r.accuracy
        for r in recent_results
        if r.accuracy is not None
    ]

    if accuracies:
        average_accuracy = sum(accuracies) / len(accuracies)

        if average_accuracy < 50:
            risk_score += 25
            signals.append("Lower accuracy pattern")

        elif average_accuracy < 70:
            risk_score += 10
            signals.append("Moderate accuracy pattern")

    # -------------------------------------------------
    # 5. Convert score into risk level
    # -------------------------------------------------

    risk_score = min(risk_score, 100)

    if risk_score >= 75:
        risk_level = "critical"

    elif risk_score >= 50:
        risk_level = "high"

    elif risk_score >= 25:
        risk_level = "elevated"

    else:
        risk_level = "low"

    # -------------------------------------------------
    # 6. Final message
    # -------------------------------------------------

    if risk_level == "low":
        message = "Current activity pattern looks stable."

    elif risk_level == "elevated":
        message = "Some changes in activity patterns may be worth checking in on."

    elif risk_level == "high":
        message = "Multiple wellbeing signals detected. A human check-in may be appropriate."

    else:
        message = "Significant wellbeing signals detected. Follow the safety escalation process."

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "signals": signals,
        "message": message
    }