"""Optimization engine for energy-aware scheduling."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List

from app.models import Appliance, ForecastPoint, HouseholdProfile, OptimizationRecommendation, UsageWindow


def _time_to_hour(value: str) -> int:
    return int(value.split(":")[0])


def _compute_window_score(
    start_hour: int,
    duration_hours: float,
    price_at_start: float,
    forecast_window: List[ForecastPoint],
    appliance: Appliance,
    profile: HouseholdProfile,
) -> Dict[str, float]:
    peak_penalty = 0.0
    cost_score = 0.0

    for point in forecast_window:
        timestamp = datetime.fromisoformat(point.timestamp)
        hour_value = timestamp.hour
        if start_hour <= hour_value < start_hour + max(1, int(duration_hours)):
            cost_score += point.price_cents_kwh * (0.4 + appliance.peak_sensitivity)
            peak_penalty += max(0.0, point.net_demand_kw - 3.5) * 2.0

    comfort_factor = appliance.comfort_impact * (1.0 - profile.comfort_target)
    window_score = cost_score + peak_penalty + (comfort_factor * 180.0)
    return {
        "window_score": window_score,
        "cost_score": cost_score,
        "peak_penalty": peak_penalty,
    }


def optimize_schedule(
    profile: HouseholdProfile,
    appliances: List[Appliance],
    forecast: List[ForecastPoint],
) -> Dict[str, object]:
    recommendations: List[OptimizationRecommendation] = []
    usage_windows: List[UsageWindow] = []
    scheduled_hours = set()
    total_cost_before = 0.0
    total_cost_after = 0.0

    for point in forecast:
        total_cost_before += point.demand_kw * (point.price_cents_kwh / 100.0)

    for index, appliance in enumerate(sorted(appliances, key=lambda item: (-item.priority, item.name))):
        candidate_scores: List[UsageWindow] = []

        duration_hours = max(1, round(appliance.duration_minutes / 60.0))
        for start_hour in range(0, 24):
            end_hour = start_hour + duration_hours
            if end_hour > 24:
                continue

            if appliance.flexible:
                window_points = [
                    point for point in forecast if start_hour <= datetime.fromisoformat(point.timestamp).hour < end_hour
                ]
            else:
                preferred = _time_to_hour(appliance.preferred_window.split("-")[0])
                if abs(start_hour - preferred) > 6:
                    continue
                window_points = [
                    point for point in forecast if start_hour <= datetime.fromisoformat(point.timestamp).hour < end_hour
                ]

            if not window_points:
                continue

            score_metrics = _compute_window_score(
                start_hour=start_hour,
                duration_hours=duration_hours,
                price_at_start=window_points[0].price_cents_kwh,
                forecast_window=window_points,
                appliance=appliance,
                profile=profile,
            )

            price_savings = sum(point.price_cents_kwh for point in window_points) * (0.12 + appliance.priority * 0.04)
            peak_reduction = appliance.power_kw * (0.38 + appliance.peak_sensitivity * 0.25)

            if appliance.flexible:
                score = score_metrics["window_score"] * (0.5 + appliance.priority / 10.0)
            else:
                score = score_metrics["window_score"] * 0.8 + (abs(start_hour - preferred) * 15.0)

            candidate_scores.append(
                UsageWindow(
                    start_hour=start_hour,
                    end_hour=end_hour,
                    score=score,
                    price_savings=price_savings,
                    peak_reduction=peak_reduction,
                )
            )

        if not candidate_scores:
            continue

        best_choice = min(candidate_scores, key=lambda item: item.score)
        usage_windows.append(best_choice)
        scheduled_hours.add(best_choice.start_hour)

        start_local = f"{best_choice.start_hour:02d}:00"
        end_local = f"{best_choice.end_hour:02d}:00"
        expected_savings = best_choice.price_savings * 0.65
        comfort_score = max(0.5, 0.95 - (appliance.comfort_impact * 0.12))

        recommendations.append(
            OptimizationRecommendation(
                appliance_id=appliance.id,
                appliance_name=appliance.name,
                recommended_start=start_local,
                recommended_end=end_local,
                triggered_reason="Minimize tariff + peak-shaving opportunity",
                expected_savings_usd=expected_savings,
                peak_reduction_kw=best_choice.peak_reduction,
                comfort_score=comfort_score,
                sequence_index=index + 1,
            )
        )

        for point in forecast:
            timestamp = datetime.fromisoformat(point.timestamp)
            if best_choice.start_hour <= timestamp.hour < best_choice.end_hour:
                total_cost_after += point.demand_kw * (point.price_cents_kwh / 100.0) * 0.67

    total_savings = total_cost_before - total_cost_after
    peak_reduction_total = sum(item.peak_reduction_kw for item in recommendations)

    summary = {
        "total_cost_before_usd": round(total_cost_before, 2),
        "total_cost_after_usd": round(total_cost_after, 2),
        "estimated_savings_usd": round(total_savings, 2),
        "peak_reduction_kw": round(peak_reduction_total, 2),
        "appliances_scheduled": len(recommendations),
        "scheduled_windows": [item.to_dict() for item in usage_windows],
    }

    return {
        "recommendations": [item.to_dict() for item in recommendations],
        "summary": summary,
    }
