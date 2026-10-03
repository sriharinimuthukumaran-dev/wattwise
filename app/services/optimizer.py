"""Demand and price forecasting services for WattWise."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List

from app.models import EnergySummary, ForecastPoint, HouseholdProfile


def _hourly_timestamp(base_time: datetime, hour_index: int) -> str:
    return (base_time + timedelta(hours=hour_index)).strftime("%Y-%m-%dT%H:00:00")


def _hourly_price(hour: int, tariff_profile: Dict[str, float]) -> float:
    hour_key = f"{hour:02d}:00"
    if hour_key in tariff_profile:
        return tariff_profile[hour_key]
    return 0.21


def generate_forecast(profile: HouseholdProfile, hours: int = 24) -> List[ForecastPoint]:
    """Generate a 24-hour or multi-hour forecast using a simple but effective heuristic model."""
    base_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    results: List[ForecastPoint] = []

    for hour_index in range(hours):
        current_hour = (base_time + timedelta(hours=hour_index)).hour
        occupancy = profile.occupancy_pattern.get(f"{current_hour:02d}:00", 0.5)
        price = _hourly_price(current_hour, profile.tariff_schedule)

        weather_correction = profile.weather_factor * (1.0 if current_hour >= 15 else 0.4)
        solar_generation = profile.solar_capacity_kw * max(0.0, (1.0 - abs(current_hour - 13) / 11.0))
        solar_generation *= 0.7

        if current_hour >= 6 and current_hour <= 17:
            solar_generation *= 1.2
        elif current_hour > 17 or current_hour < 6:
            solar_generation *= 0.15

        demand = profile.baseline_load_kw
        demand += profile.occupants * 0.26 * occupancy
        demand += weather_correction * 1.7
        demand += 0.6 if current_hour in (7, 8, 17, 18, 19, 20) else 0.0
        demand += 0.4 if current_hour in (9, 10, 11, 12, 13) else 0.0

        if current_hour >= 21 or current_hour <= 5:
            demand *= 0.9

        net_demand = max(0.0, demand - solar_generation)
        temperature = 18.5 + 11.0 * (0.5 + 0.5 * __import__('math').sin((hour_index - 5) / 3.0))

        results.append(
            ForecastPoint(
                timestamp=_hourly_timestamp(base_time, hour_index),
                demand_kw=round(demand, 2),
                solar_kw=round(solar_generation, 2),
                price_cents_kwh=round(price * 100.0, 2),
                temperature_c=round(temperature, 2),
                occupancy_index=round(occupancy, 2),
                net_demand_kw=round(net_demand, 2),
            )
        )

    return results


def summarize_forecast(points: List[ForecastPoint]) -> EnergySummary:
    total_usage_kwh = sum(point.net_demand_kw for point in points) * 1.0
    peak_demand_kw = max(point.net_demand_kw for point in points) if points else 0.0
    average_price = sum(point.price_cents_kwh for point in points) / len(points) if points else 0.0
    estimated_cost_usd = total_usage_kwh * (average_price / 100.0) * 1.1
    renewable_share = (
        sum(point.solar_kw for point in points) / max(sum(point.demand_kw for point in points), 1.0)
    ) * 100.0

    demand_response_score = min(98.0, 65.0 + (peak_demand_kw / max(3.5, peak_demand_kw)) * 22.0)

    return EnergySummary(
        total_daily_usage_kwh=round(total_usage_kwh, 2),
        peak_demand_kw=round(peak_demand_kw, 2),
        average_price_cents_kwh=round(average_price, 2),
        estimated_cost_usd=round(estimated_cost_usd, 2),
        renewable_share_pct=round(renewable_share, 2),
        demand_response_score=round(demand_response_score, 2),
    )


def build_forecast_payload(profile: HouseholdProfile, hours: int = 24) -> Dict[str, object]:
    points = generate_forecast(profile, hours)
    summary = summarize_forecast(points)
    return {
        "points": [point.to_dict() for point in points],
        "summary": summary.to_dict(),
    }
