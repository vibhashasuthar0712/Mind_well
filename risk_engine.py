def calculate_risk(game_results):
    """
    MindWell Prototype Risk Engine

    This engine does NOT diagnose any mental-health condition.

    It identifies changes in activity patterns that may indicate
    that a wellbeing check-in could be useful.
    """

    # -------------------------------------------------
    # 0. Not enough data
    # -------------------------------------------------

    if not game_results:
        return {
            "risk_score": 0,
            "risk_level": "low",
            "signals": [],
            "message": "Not enough activity data yet."
        }

    # -------------------------------------------------
    # 1. Need enough history for baseline comparison
    # -------------------------------------------------

    if len(game_results) < 3:
        return {
            "risk_score": 0,
            "risk_level": "low",
            "signals": [],
            "message": "More activity data is needed to establish a personal baseline."
        }

    # -------------------------------------------------
    # 2. Split historical and recent activity
    # -------------------------------------------------

    scores = [
        r.score
        for r in game_results
        if r.score is not None
    ]

    accuracies = [
        r.accuracy
        for r in game_results
        if r.accuracy is not None
    ]

    response_times = [
        r.time_taken
        for r in game_results
        if r.time_taken is not None
    ]

    risk_score = 0
    signals = []

    # -------------------------------------------------
    # 3. PERSONAL BASELINE
    # -------------------------------------------------

    # Use older activity as baseline
    if len(scores) >= 4:

        baseline_scores = scores[:-3]
        recent_scores = scores[-3:]

        baseline_average = (
            sum(baseline_scores) / len(baseline_scores)
        )

        recent_average = (
            sum(recent_scores) / len(recent_scores)
        )

        score_change = baseline_average - recent_average

        # Significant decline
        if score_change >= 30:
            risk_score += 30
            signals.append(
                "Significant decline from personal activity baseline"
            )

        elif score_change >= 15:
            risk_score += 15
            signals.append(
                "Recent activity performance is below personal baseline"
            )

    # -------------------------------------------------
    # 4. REPEATED LOW PERFORMANCE
    # -------------------------------------------------

    recent_scores = scores[-5:]

    if len(recent_scores) >= 3:

        low_score_count = sum(
            1 for score in recent_scores
            if score < 50
        )

        if low_score_count >= 4:
            risk_score += 20
            signals.append(
                "Repeated lower activity performance"
            )

        elif low_score_count >= 3:
            risk_score += 10
            signals.append(
                "Several recent activities show lower performance"
            )

    # -------------------------------------------------
    # 5. RESPONSE TIME CHANGE
    # -------------------------------------------------

    if len(response_times) >= 4:

        baseline_times = response_times[:-3]
        recent_times = response_times[-3:]

        baseline_time = (
            sum(baseline_times) / len(baseline_times)
        )

        recent_time = (
            sum(recent_times) / len(recent_times)
        )

        if baseline_time > 0:

            time_increase = (
                (recent_time - baseline_time)
                / baseline_time
            ) * 100

            if time_increase >= 40:
                risk_score += 20
                signals.append(
                    "Response time has increased significantly from baseline"
                )

            elif time_increase >= 20:
                risk_score += 10
                signals.append(
                    "Recent response time is slower than usual"
                )

    # -------------------------------------------------
    # 6. ACCURACY DECLINE
    # -------------------------------------------------

    if len(accuracies) >= 4:

        baseline_accuracy = accuracies[:-3]
        recent_accuracy = accuracies[-3:]

        baseline_avg = (
            sum(baseline_accuracy)
            / len(baseline_accuracy)
        )

        recent_avg = (
            sum(recent_accuracy)
            / len(recent_accuracy)
        )

        accuracy_change = baseline_avg - recent_avg

        if accuracy_change >= 30:
            risk_score += 20
            signals.append(
                "Significant decline in activity accuracy"
            )

        elif accuracy_change >= 15:
            risk_score += 10
            signals.append(
                "Recent accuracy is below personal baseline"
            )

    # -------------------------------------------------
    # 7. CURRENT LOW ACCURACY
    # -------------------------------------------------

    if accuracies:

        recent_accuracy = accuracies[-3:]

        average_recent_accuracy = (
            sum(recent_accuracy)
            / len(recent_accuracy)
        )

        if average_recent_accuracy < 50:
            risk_score += 15
            signals.append(
                "Consistently low recent accuracy"
            )

    # -------------------------------------------------
    # 8. COMBINATION SIGNAL
    # -------------------------------------------------

    # Multiple different signals together are more
    # meaningful than a single isolated signal.

    if len(signals) >= 3:
        risk_score += 10
        signals.append(
            "Multiple activity pattern changes detected"
        )

    # -------------------------------------------------
    # 9. Keep score between 0 and 100
    # -------------------------------------------------

    risk_score = min(risk_score, 100)

    # -------------------------------------------------
    # 10. Convert score to risk level
    # -------------------------------------------------

    if risk_score >= 75:

        risk_level = "critical"

    elif risk_score >= 50:

        risk_level = "high"

    elif risk_score >= 25:

        risk_level = "elevated"

    else:

        risk_level = "low"

    # -------------------------------------------------
    # 11. User-friendly message
    # -------------------------------------------------

    if risk_level == "low":

        message = (
            "Current activity pattern looks relatively stable."
        )

    elif risk_level == "elevated":

        message = (
            "Some changes in activity patterns may be worth "
            "checking in on."
        )

    elif risk_level == "high":

        message = (
            "Multiple wellbeing signals detected. "
            "A human check-in may be appropriate."
        )

    else:

        message = (
            "Significant wellbeing signals detected. "
            "Follow the safety escalation process."
        )

    # -------------------------------------------------
    # 12. Final result
    # -------------------------------------------------

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "signals": signals,
        "message": message
    }