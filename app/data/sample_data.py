"""Core data models for WattWise."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Appliance:
    id: str
    name: str
    category: str
    power_kw: float
    duration_minutes: int
    preferred_window: str
    flexible: bool = True
    priority: int = 1
    comfort_impact: float = 1.0
    peak_sensitivity: float = 0.7
    smart_compatible: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "power_kw": self.power_kw,
            "duration_minutes": self.duration_minutes,
            "preferred_window": self.preferred_window,
            "flexible": self.flexible,
            "priority": self.priority,
            "comfort_impact": self.comfort_impact,
            "peak_sensitivity": self.peak_sensitivity,
            "smart_compatible": self.smart_compatible,
        }


@dataclass
class HouseholdProfile:
    home_id: str
    name: str
    occupants: int
    square_feet: int
    baseline_load_kw: float
    solar_capacity_kw: float
    battery_capacity_kwh: float
    tariff_schedule: Dict[str, float]
    occupancy_pattern: Dict[str, float]
    weather_factor: float = 0.0
    comfort_target: float = 0.88
    peak_cost_multiplier: float = 1.25

    def to_dict(self) -> Dict[str, Any]:
        return {
            "home_id": self.home_id,
            "name": self.name,
            "occupants": self.occupants,
            "square_feet": self.square_feet,
            "baseline_load_kw": self.baseline_load_kw,
            "solar_capacity_kw": self.solar_capacity_kw,
            "battery_capacity_kwh": self.battery_capacity_kwh,
            "tariff_schedule": self.tariff_schedule,
            "occupancy_pattern": self.occupancy_pattern,
            "weather_factor": self.weather_factor,
            "comfort_target": self.comfort_target,
            "peak_cost_multiplier": self.peak_cost_multiplier,
        }


@dataclass
class ForecastPoint:
    timestamp: str
    demand_kw: float
    solar_kw: float
    price_cents_kwh: float
    temperature_c: float
    occupancy_index: float
    net_demand_kw: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "demand_kw": round(self.demand_kw, 2),
            "solar_kw": round(self.solar_kw, 2),
            "price_cents_kwh": round(self.price_cents_kwh, 2),
            "temperature_c": round(self.temperature_c, 2),
            "occupancy_index": round(self.occupancy_index, 2),
            "net_demand_kw": round(self.net_demand_kw, 2),
        }


@dataclass
class OptimizationRecommendation:
    appliance_id: str
    appliance_name: str
    recommended_start: str
    recommended_end: str
    triggered_reason: str
    expected_savings_usd: float
    peak_reduction_kw: float
    comfort_score: float
    sequence_index: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "appliance_id": self.appliance_id,
            "appliance_name": self.appliance_name,
            "recommended_start": self.recommended_start,
            "recommended_end": self.recommended_end,
            "triggered_reason": self.triggered_reason,
            "expected_savings_usd": round(self.expected_savings_usd, 2),
            "peak_reduction_kw": round(self.peak_reduction_kw, 2),
            "comfort_score": round(self.comfort_score, 2),
            "sequence_index": self.sequence_index,
        }


@dataclass
class EnergySummary:
    total_daily_usage_kwh: float
    peak_demand_kw: float
    average_price_cents_kwh: float
    estimated_cost_usd: float
    renewable_share_pct: float
    demand_response_score: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_daily_usage_kwh": round(self.total_daily_usage_kwh, 2),
            "peak_demand_kw": round(self.peak_demand_kw, 2),
            "average_price_cents_kwh": round(self.average_price_cents_kwh, 2),
            "estimated_cost_usd": round(self.estimated_cost_usd, 2),
            "renewable_share_pct": round(self.renewable_share_pct, 2),
            "demand_response_score": round(self.demand_response_score, 2),
        }


@dataclass
class HouseholdSnapshot:
    profile: HouseholdProfile
    appliances: List[Appliance]
    forecast: List[ForecastPoint]
    summary: EnergySummary
    recommendations: List[OptimizationRecommendation]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "profile": self.profile.to_dict(),
            "appliances": [app.to_dict() for app in self.appliances],
            "forecast": [point.to_dict() for point in self.forecast],
            "summary": self.summary.to_dict(),
            "recommendations": [item.to_dict() for item in self.recommendations],
        }


@dataclass
class UsageWindow:
    start_hour: int
    end_hour: int
    score: float
    price_savings: float
    peak_reduction: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "start_hour": self.start_hour,
            "end_hour": self.end_hour,
            "score": round(self.score, 2),
            "price_savings": round(self.price_savings, 2),
            "peak_reduction": round(self.peak_reduction, 2),
        }
