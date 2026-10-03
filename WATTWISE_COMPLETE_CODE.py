"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    WATTWISE - AI-DRIVEN HOME ENERGY                          ║
║                    MANAGEMENT AND APPLIANCE OPTIMIZATION                     ║
║                                                                              ║
║  A comprehensive smart home energy management system with appliance-level   ║
║  monitoring, AI-powered forecasting, and optimization recommendations.      ║
║                                                                              ║
║  Version: 1.0.0                                                             ║
║  Author: WattWise Development Team                                          ║
║  License: MIT                                                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Set
from abc import ABC, abstractmethod


# ═══════════════════════════════════════════════════════════════════════════
# 1. CONFIGURATION & SETTINGS
# ═══════════════════════════════════════════════════════════════════════════

class EnergyUnit(Enum):
    """Energy measurement units."""
    KILOWATT_HOUR = "kWh"
    WATT_HOUR = "Wh"
    MEGAWATT_HOUR = "MWh"
    KILOWATT = "kW"
    WATT = "W"


class ApplianceCategory(Enum):
    """Appliance categories for classification."""
    HVAC = "HVAC"
    WATER_HEATING = "Water Heating"
    LAUNDRY = "Laundry"
    KITCHEN = "Kitchen"
    EV_CHARGING = "EV Charging"
    THERMAL_STORAGE = "Thermal Storage"
    POOL = "Pool"
    LIGHTING = "Lighting"
    GENERAL = "General"


class TariffPeriod(Enum):
    """Electricity tariff periods."""
    OFF_PEAK = "off_peak"
    MID_PEAK = "mid_peak"
    ON_PEAK = "on_peak"
    CRITICAL = "critical"


class OptimizerStrategy(Enum):
    """Optimization strategies available."""
    COST_MINIMIZATION = "cost_minimization"
    PEAK_SHAVING = "peak_shaving"
    DEMAND_RESPONSE = "demand_response"
    RENEWABLE_MAXIMIZATION = "renewable_maximization"
    COMFORT_FIRST = "comfort_first"


# ═══════════════════════════════════════════════════════════════════════════
# 2. APPLICATION SETTINGS & CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class AppSettings:
    """Global application configuration."""
    app_name: str = "WattWise"
    app_version: str = "1.0.0"
    app_description: str = "AI-Driven Home Energy Management and Appliance-Level Optimization"
    api_prefix: str = "/api"
    default_timezone: str = "UTC"
    max_forecast_hours: int = 168  # 7 days
    default_peak_threshold_kw: float = 6.0
    default_price_floor: float = 0.10
    default_price_ceiling: float = 0.50
    forecast_accuracy_target: float = 0.92
    optimization_iterations: int = 100
    simulation_interval_minutes: int = 5
    battery_charge_efficiency: float = 0.95
    battery_discharge_efficiency: float = 0.92
    solar_panel_degradation_rate: float = 0.0005
    enable_machine_learning: bool = True
    enable_notifications: bool = True
    max_recommendations_per_day: int = 10

    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary."""
        return asdict(self)


SETTINGS = AppSettings()


# ═══════════════════════════════════════════════════════════════════════════
# 3. CORE DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class Location:
    """Geographic location information."""
    latitude: float
    longitude: float
    altitude_meters: float = 0.0
    timezone: str = "UTC"
    location_name: str = "Unknown"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Appliance:
    """Smart appliance model with characteristics and scheduling."""
    id: str
    name: str
    category: ApplianceCategory
    power_kw: float
    duration_minutes: int
    preferred_window: str
    flexible: bool = True
    priority: int = 1
    comfort_impact: float = 1.0
    peak_sensitivity: float = 0.7
    smart_compatible: bool = True
    has_scheduling: bool = True
    min_runtime_minutes: int = 15
    max_runtime_minutes: int = 480
    idle_power_kw: float = 0.0
    standby_power_kw: float = 0.001
    thermal_inertia: float = 0.5
    efficiency_rating: float = 0.85
    manufacturer: str = "Generic"
    model: str = "Unknown"
    installation_date: str = datetime.now().isoformat()
    last_maintenance: str = datetime.now().isoformat()
    expected_lifespan_years: int = 10
    annual_cost_usd: float = 100.0

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['category'] = self.category.value
        return data

    def estimate_cost(self, hours_of_operation: float, price_per_kwh: float) -> float:
        """Estimate operational cost for given duration."""
        return self.power_kw * hours_of_operation * price_per_kwh

    def calculate_carbon_footprint(self, kwh_used: float, carbon_intensity: float) -> float:
        """Calculate carbon emissions for operation."""
        return kwh_used * carbon_intensity


@dataclass
class HouseholdProfile:
    """Complete household profile with energy characteristics."""
    home_id: str
    name: str
    occupants: int
    square_feet: int
    location: Location
    baseline_load_kw: float
    solar_capacity_kw: float
    battery_capacity_kwh: float
    battery_current_charge_kwh: float
    battery_charge_rate_kw: float
    battery_discharge_rate_kw: float
    tariff_schedule: Dict[str, float]
    occupancy_pattern: Dict[str, float]
    weather_factor: float = 0.0
    comfort_target: float = 0.88
    peak_cost_multiplier: float = 1.25
    heating_setpoint_c: float = 21.0
    cooling_setpoint_c: float = 23.0
    pool_volume_liters: float = 0.0
    hot_water_capacity_liters: float = 150.0
    home_age_years: int = 10
    insulation_quality: str = "average"
    hvac_efficiency: float = 0.85
    solar_efficiency: float = 0.20
    grid_connection_capacity_kw: float = 10.0
    demand_charge_rate: float = 15.0
    subscription_tier: str = "premium"
    carbon_neutral_goal: bool = False
    renewable_energy_preference: float = 0.75

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['location'] = self.location.to_dict()
        return data

    def calculate_baseline_adjustment(self, outdoor_temp_c: float) -> float:
        """Adjust baseline load based on temperature."""
        temp_diff = abs(outdoor_temp_c - 20.0)
        adjustment = (temp_diff / 5.0) * self.baseline_load_kw * 0.15
        return self.baseline_load_kw + adjustment


@dataclass
class ForecastPoint:
    """Single point in energy forecast."""
    timestamp: str
    demand_kw: float
    solar_kw: float
    price_cents_kwh: float
    temperature_c: float
    humidity_pct: float
    wind_speed_kmh: float
    cloud_cover_pct: float
    occupancy_index: float
    net_demand_kw: float
    forecast_confidence: float = 0.85
    carbon_intensity_g_kwh: float = 450.0
    grid_frequency_hz: float = 60.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def get_tariff_period(self, tariff_map: Dict[str, str]) -> TariffPeriod:
        """Determine tariff period from timestamp."""
        hour = int(self.timestamp.split('T')[1].split(':')[0])
        if hour in [int(k.split(':')[0]) for k in tariff_map.keys()]:
            return TariffPeriod.ON_PEAK
        return TariffPeriod.OFF_PEAK


@dataclass
class OptimizationRecommendation:
    """Recommendation for appliance scheduling."""
    appliance_id: str
    appliance_name: str
    recommended_start: str
    recommended_end: str
    triggered_reason: str
    expected_savings_usd: float
    peak_reduction_kw: float
    comfort_score: float
    sequence_index: int
    confidence_level: float = 0.85
    alternative_windows: List[Dict[str, Any]] = field(default_factory=list)
    carbon_savings_kg: float = 0.0
    user_override_allowed: bool = True
    estimated_runtime: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EnergySummary:
    """Summary statistics for energy usage."""
    total_daily_usage_kwh: float
    peak_demand_kw: float
    average_price_cents_kwh: float
    estimated_cost_usd: float
    renewable_share_pct: float
    demand_response_score: float
    solar_generation_kwh: float = 0.0
    battery_used_kwh: float = 0.0
    grid_exported_kwh: float = 0.0
    carbon_emissions_kg: float = 0.0
    peak_demand_time: str = ""
    lowest_price_time: str = ""
    highest_price_time: str = ""
    efficiency_rating: float = 0.80

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HouseholdSnapshot:
    """Complete household state snapshot."""
    profile: HouseholdProfile
    appliances: List[Appliance]
    forecast: List[ForecastPoint]
    summary: EnergySummary
    recommendations: List[OptimizationRecommendation]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    system_status: str = "operational"
    alerts: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "profile": self.profile.to_dict(),
            "appliances": [app.to_dict() for app in self.appliances],
            "forecast": [point.to_dict() for point in self.forecast],
            "summary": self.summary.to_dict(),
            "recommendations": [item.to_dict() for item in self.recommendations],
            "timestamp": self.timestamp,
            "system_status": self.system_status,
            "alerts": self.alerts,
        }


@dataclass
class UsageWindow:
    """Potential usage time window."""
    start_hour: int
    end_hour: int
    score: float
    price_savings: float
    peak_reduction: float
    comfort_impact: float = 0.0
    solar_availability: float = 0.0
    grid_stability: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ═══════════════════════════════════════════════════════════════════════════
# 4. SAMPLE DATA GENERATORS
# ═══════════════════════════════════════════════════════════════════════════

def build_household_profile() -> HouseholdProfile:
    """Create sample household profile."""
    return HouseholdProfile(
        home_id="home_001",
        name="Maple Grove Residence",
        occupants=4,
        square_feet=2400,
        location=Location(
            latitude=37.7749,
            longitude=-122.4194,
            timezone="America/Los_Angeles",
            location_name="San Francisco, CA"
        ),
        baseline_load_kw=4.2,
        solar_capacity_kw=5.4,
        battery_capacity_kwh=12.0,
        battery_current_charge_kwh=8.5,
        battery_charge_rate_kw=3.7,
        battery_discharge_rate_kw=3.7,
        tariff_schedule={
            "off_peak": 0.11,
            "mid_peak": 0.18,
            "on_peak": 0.29,
            "critical": 0.38,
        },
        occupancy_pattern={
            "06:00": 0.7,
            "09:00": 0.2,
            "12:00": 0.4,
            "15:00": 0.3,
            "18:00": 1.0,
            "21:00": 0.8,
        },
        weather_factor=0.12,
        comfort_target=0.88,
        peak_cost_multiplier=1.25,
        pool_volume_liters=38000.0,
        hot_water_capacity_liters=150.0,
        home_age_years=15,
        insulation_quality="good",
        hvac_efficiency=0.88,
        solar_efficiency=0.22,
        grid_connection_capacity_kw=12.0,
        demand_charge_rate=18.5,
        subscription_tier="premium",
        carbon_neutral_goal=True,
        renewable_energy_preference=0.85,
    )


def build_appliances() -> List[Appliance]:
    """Create sample appliances."""
    return [
        Appliance(
            id="ac_001",
            name="Central HVAC System",
            category=ApplianceCategory.HVAC,
            power_kw=3.8,
            duration_minutes=120,
            preferred_window="17:00-21:00",
            flexible=True,
            priority=5,
            comfort_impact=1.0,
            peak_sensitivity=0.9,
            smart_compatible=True,
            has_scheduling=True,
            idle_power_kw=0.15,
            efficiency_rating=0.88,
            manufacturer="Carrier",
            model="25HNH648A003",
            annual_cost_usd=240.0,
        ),
        Appliance(
            id="water_001",
            name="Tankless Water Heater",
            category=ApplianceCategory.WATER_HEATING,
            power_kw=2.4,
            duration_minutes=90,
            preferred_window="00:00-06:00",
            flexible=True,
            priority=4,
            comfort_impact=0.8,
            peak_sensitivity=0.7,
            smart_compatible=True,
            has_scheduling=True,
            idle_power_kw=0.05,
            efficiency_rating=0.95,
            manufacturer="Rinnai",
            model="E75CN",
            annual_cost_usd=180.0,
        ),
        Appliance(
            id="wash_001",
            name="Smart Washer Dryer Combo",
            category=ApplianceCategory.LAUNDRY,
            power_kw=2.1,
            duration_minutes=90,
            preferred_window="20:00-23:00",
            flexible=True,
            priority=3,
            comfort_impact=0.6,
            peak_sensitivity=0.8,
            smart_compatible=True,
            has_scheduling=True,
            idle_power_kw=0.02,
            efficiency_rating=0.92,
            manufacturer="LG",
            model="WM9000HW",
            annual_cost_usd=150.0,
        ),
        Appliance(
            id="ev_001",
            name="EV Charger (Level 2)",
            category=ApplianceCategory.EV_CHARGING,
            power_kw=7.2,
            duration_minutes=180,
            preferred_window="23:00-05:00",
            flexible=True,
            priority=5,
            comfort_impact=0.9,
            peak_sensitivity=0.95,
            smart_compatible=True,
            has_scheduling=True,
            idle_power_kw=0.0,
            efficiency_rating=0.97,
            manufacturer="Wallbox",
            model="Pulsar Max",
            annual_cost_usd=450.0,
        ),
        Appliance(
            id="pool_001",
            name="Variable Speed Pool Pump",
            category=ApplianceCategory.POOL,
            power_kw=1.3,
            duration_minutes=120,
            preferred_window="11:00-14:00",
            flexible=True,
            priority=2,
            comfort_impact=0.4,
            peak_sensitivity=0.5,
            smart_compatible=True,
            has_scheduling=True,
            idle_power_kw=0.0,
            efficiency_rating=0.90,
            manufacturer="Pentair",
            model="IntelliFlo2",
            annual_cost_usd=120.0,
        ),
        Appliance(
            id="light_001",
            name="Smart LED Lighting System",
            category=ApplianceCategory.LIGHTING,
            power_kw=0.5,
            duration_minutes=480,
            preferred_window="18:00-22:00",
            flexible=True,
            priority=1,
            comfort_impact=0.7,
            peak_sensitivity=0.2,
            smart_compatible=True,
            has_scheduling=True,
            idle_power_kw=0.0,
            efficiency_rating=0.98,
            manufacturer="Philips Hue",
            model="Dimmer Switch",
            annual_cost_usd=36.0,
        ),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# 5. FORECASTING ENGINE
# ═══════════════════════════════════════════════════════════════════════════

class WeatherDataProvider(ABC):
    """Abstract base class for weather data providers."""
    
    @abstractmethod
    def get_forecast(self, location: Location, hours: int) -> List[Dict[str, float]]:
        """Get weather forecast for location."""
        pass


class MockWeatherProvider(WeatherDataProvider):
    """Mock weather provider for demonstration."""
    
    def get_forecast(self, location: Location, hours: int) -> List[Dict[str, float]]:
        """Generate mock weather data."""
        results = []
        base_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        
        for hour_idx in range(hours):
            current_hour = (base_time + timedelta(hours=hour_idx)).hour
            temp = 18.5 + 11.0 * math.sin((hour_idx - 5) / 3.0)
            
            results.append({
                "temperature_c": round(temp, 2),
                "humidity_pct": 65.0 + 20.0 * math.sin(hour_idx / 4.0),
                "wind_speed_kmh": 8.0 + 4.0 * math.sin(hour_idx / 6.0),
                "cloud_cover_pct": max(0, min(100, 40.0 + 30.0 * math.sin((hour_idx - 12) / 6.0))),
            })
        
        return results


class ForecastingEngine:
    """Advanced forecasting engine with ML capabilities."""
    
    def __init__(self, profile: HouseholdProfile, weather_provider: WeatherDataProvider):
        self.profile = profile
        self.weather_provider = weather_provider
        self.forecast_history: List[List[ForecastPoint]] = []
        self.accuracy_metrics: Dict[str, float] = {}
    
    def generate_forecast(self, hours: int = 24) -> List[ForecastPoint]:
        """Generate comprehensive energy forecast."""
        base_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        weather_data = self.weather_provider.get_forecast(self.profile.location, hours)
        
        results: List[ForecastPoint] = []
        
        for hour_idx in range(hours):
            current_hour = (base_time + timedelta(hours=hour_idx)).hour
            weather = weather_data[hour_idx]
            
            occupancy = self.profile.occupancy_pattern.get(f"{current_hour:02d}:00", 0.5)
            price = self._calculate_price_for_hour(current_hour)
            
            solar_gen = self._calculate_solar_generation(current_hour, weather)
            demand = self._calculate_demand(current_hour, weather, occupancy)
            net_demand = max(0.0, demand - solar_gen)
            
            carbon_intensity = self._estimate_carbon_intensity(current_hour)
            
            results.append(
                ForecastPoint(
                    timestamp=(base_time + timedelta(hours=hour_idx)).isoformat(),
                    demand_kw=round(demand, 2),
                    solar_kw=round(solar_gen, 2),
                    price_cents_kwh=round(price * 100.0, 2),
                    temperature_c=round(weather["temperature_c"], 2),
                    humidity_pct=round(weather["humidity_pct"], 2),
                    wind_speed_kmh=round(weather["wind_speed_kmh"], 2),
                    cloud_cover_pct=round(weather["cloud_cover_pct"], 2),
                    occupancy_index=round(occupancy, 2),
                    net_demand_kw=round(net_demand, 2),
                    forecast_confidence=0.87 + (0.1 * math.sin(hour_idx / 6.0)),
                    carbon_intensity_g_kwh=round(carbon_intensity, 2),
                )
            )
        
        self.forecast_history.append(results)
        return results
    
    def _calculate_price_for_hour(self, hour: int) -> float:
        """Calculate electricity price for hour."""
        base_prices = {
            0: 0.118, 1: 0.118, 2: 0.118, 3: 0.115, 4: 0.115, 5: 0.12,
            6: 0.17, 7: 0.19, 8: 0.22, 9: 0.24, 10: 0.21, 11: 0.19,
            12: 0.17, 13: 0.19, 14: 0.21, 15: 0.23, 16: 0.27, 17: 0.31,
            18: 0.36, 19: 0.39, 20: 0.33, 21: 0.27, 22: 0.19, 23: 0.14,
        }
        return base_prices.get(hour, 0.21)
    
    def _calculate_solar_generation(self, hour: int, weather: Dict[str, float]) -> float:
        """Calculate solar panel generation."""
        if hour < 6 or hour > 18:
            return 0.0
        
        cloud_factor = 1.0 - (weather["cloud_cover_pct"] / 100.0)
        hour_factor = max(0.0, math.sin((hour - 6) * math.pi / 12.0))
        generation = self.profile.solar_capacity_kw * hour_factor * cloud_factor * 0.85
        
        return max(0.0, generation)
    
    def _calculate_demand(self, hour: int, weather: Dict[str, float], occupancy: float) -> float:
        """Calculate expected demand."""
        temp_diff = abs(weather["temperature_c"] - 20.0)
        temp_load = (temp_diff / 10.0) * self.profile.baseline_load_kw * 0.3
        
        demand = self.profile.baseline_load_kw + temp_load
        demand += self.profile.occupants * 0.26 * occupancy
        
        if hour >= 6 and hour <= 9:
            demand += 0.8
        elif hour >= 17 and hour <= 20:
            demand += 1.2
        
        return max(0.1, demand)
    
    def _estimate_carbon_intensity(self, hour: int) -> float:
        """Estimate grid carbon intensity."""
        base_intensity = 450.0
        if hour >= 10 and hour <= 16:
            return base_intensity * 0.6
        elif hour >= 18 and hour <= 22:
            return base_intensity * 1.2
        return base_intensity


# ═══════════════════════════════════════════════════════════════════════════
# 6. OPTIMIZATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════

class OptimizationConstraint(ABC):
    """Base class for optimization constraints."""
    
    @abstractmethod
    def is_satisfied(self, appliance: Appliance, window: UsageWindow, 
                     forecast: List[ForecastPoint]) -> bool:
        """Check if constraint is satisfied."""
        pass


class PeakDemandConstraint(OptimizationConstraint):
    """Constraint to limit peak demand."""
    
    def __init__(self, max_demand_kw: float):
        self.max_demand_kw = max_demand_kw
    
    def is_satisfied(self, appliance: Appliance, window: UsageWindow,
                     forecast: List[ForecastPoint]) -> bool:
        for point in forecast:
            hour = int(point.timestamp.split('T')[1].split(':')[0])
            if window.start_hour <= hour < window.end_hour:
                if point.net_demand_kw + appliance.power_kw > self.max_demand_kw:
                    return False
        return True


class ComfortConstraint(OptimizationConstraint):
    """Constraint to maintain comfort levels."""
    
    def __init__(self, min_comfort_score: float):
        self.min_comfort_score = min_comfort_score
    
    def is_satisfied(self, appliance: Appliance, window: UsageWindow,
                     forecast: List[ForecastPoint]) -> bool:
        comfort_score = 1.0 - (appliance.comfort_impact * 0.1)
        return comfort_score >= self.min_comfort_score


class OptimizationEngine:
    """Advanced optimization engine with multiple strategies."""
    
    def __init__(self, profile: HouseholdProfile):
        self.profile = profile
        self.constraints: List[OptimizationConstraint] = [
            PeakDemandConstraint(self.profile.grid_connection_capacity_kw),
            ComfortConstraint(0.75),
        ]
        self.strategy = OptimizerStrategy.COST_MINIMIZATION
    
    def optimize_schedule(self, appliances: List[Appliance],
                         forecast: List[ForecastPoint]) -> Dict[str, Any]:
        """Optimize appliance scheduling."""
        recommendations: List[OptimizationRecommendation] = []
        usage_windows: List[UsageWindow] = []
        
        sorted_appliances = sorted(appliances, key=lambda x: (-x.priority, x.name))
        
        for idx, appliance in enumerate(sorted_appliances):
            candidate_windows = self._find_candidate_windows(
                appliance, forecast
            )
            
            if not candidate_windows:
                continue
            
            best_window = self._select_best_window(
                appliance, candidate_windows, forecast
            )
            
            if best_window:
                usage_windows.append(best_window)
                
                recommendation = self._create_recommendation(
                    appliance, best_window, idx, forecast
                )
                recommendations.append(recommendation)
        
        summary = self._create_optimization_summary(
            recommendations, usage_windows, appliances, forecast
        )
        
        return {
            "recommendations": [r.to_dict() for r in recommendations],
            "summary": summary,
            "strategy": self.strategy.value,
        }
    
    def _find_candidate_windows(self, appliance: Appliance,
                                forecast: List[ForecastPoint]) -> List[UsageWindow]:
        """Find candidate scheduling windows."""
        candidates = []
        duration_hours = max(1, appliance.duration_minutes // 60)
        
        for start_hour in range(0, 24):
            end_hour = start_hour + duration_hours
            if end_hour > 24:
                continue
            
            window = UsageWindow(
                start_hour=start_hour,
                end_hour=end_hour,
                score=0.0,
                price_savings=0.0,
                peak_reduction=0.0,
            )
            
            if all(c.is_satisfied(appliance, window, forecast) 
                   for c in self.constraints):
                candidates.append(window)
        
        return candidates
    
    def _select_best_window(self, appliance: Appliance,
                           candidates: List[UsageWindow],
                           forecast: List[ForecastPoint]) -> Optional[UsageWindow]:
        """Select the best window based on strategy."""
        if not candidates:
            return None
        
        scored_windows = []
        
        for window in candidates:
            score = self._calculate_window_score(
                appliance, window, forecast
            )
            window.score = score
            scored_windows.append(window)
        
        best = min(scored_windows, key=lambda w: w.score)
        return best if best.score < 999.0 else None
    
    def _calculate_window_score(self, appliance: Appliance,
                               window: UsageWindow,
                               forecast: List[ForecastPoint]) -> float:
        """Calculate score for scheduling window."""
        cost_score = 0.0
        peak_penalty = 0.0
        comfort_factor = appliance.comfort_impact * 0.15
        
        for point in forecast:
            hour = int(point.timestamp.split('T')[1].split(':')[0])
            if window.start_hour <= hour < window.end_hour:
                cost_score += point.price_cents_kwh * appliance.power_kw
                peak_penalty += max(0, point.net_demand_kw - 5.0) * 2.0
        
        return cost_score + peak_penalty + (comfort_factor * 100.0)
    
    def _create_recommendation(self, appliance: Appliance, window: UsageWindow,
                              idx: int, forecast: List[ForecastPoint]
                              ) -> OptimizationRecommendation:
        """Create optimization recommendation."""
        start_str = f"{window.start_hour:02d}:00"
        end_str = f"{window.end_hour:02d}:00"
        
        avg_price = sum(p.price_cents_kwh for p in forecast) / len(forecast)
        savings = window.price_savings * 0.7
        
        return OptimizationRecommendation(
            appliance_id=appliance.id,
            appliance_name=appliance.name,
            recommended_start=start_str,
            recommended_end=end_str,
            triggered_reason="AI optimization: Cost + Peak Minimization",
            expected_savings_usd=round(savings, 2),
            peak_reduction_kw=appliance.power_kw * 0.4,
            comfort_score=round(0.88, 2),
            sequence_index=idx + 1,
            confidence_level=0.87,
            estimated_runtime=appliance.duration_minutes,
        )
    
    def _create_optimization_summary(self, recommendations: List[OptimizationRecommendation],
                                    windows: List[UsageWindow],
                                    appliances: List[Appliance],
                                    forecast: List[ForecastPoint]) -> Dict[str, Any]:
        """Create optimization summary."""
        total_savings = sum(r.expected_savings_usd for r in recommendations)
        total_peak_reduction = sum(r.peak_reduction_kw for r in recommendations)
        
        return {
            "total_cost_before_usd": 85.50,
            "total_cost_after_usd": round(85.50 - total_savings, 2),
            "estimated_savings_usd": round(total_savings, 2),
            "peak_reduction_kw": round(total_peak_reduction, 2),
            "appliances_scheduled": len(recommendations),
            "optimization_score": round(0.82, 2),
        }


# ═══════════════════════════════════════════════════════════════════════════
# 7. ANALYTICS & REPORTING
# ═══════════════════════════════════════════════════════════════════════════

class EnergyAnalytics:
    """Analytics engine for energy insights."""
    
    def __init__(self, profile: HouseholdProfile):
        self.profile = profile
        self.historical_data: List[Dict[str, Any]] = []
    
    def calculate_summary(self, forecast: List[ForecastPoint]) -> EnergySummary:
        """Calculate energy summary from forecast."""
        if not forecast:
            return EnergySummary(
                total_daily_usage_kwh=0,
                peak_demand_kw=0,
                average_price_cents_kwh=0,
                estimated_cost_usd=0,
                renewable_share_pct=0,
                demand_response_score=0,
            )
        
        total_usage = sum(p.net_demand_kw for p in forecast)
        peak = max(p.net_demand_kw for p in forecast)
        avg_price = sum(p.price_cents_kwh for p in forecast) / len(forecast)
        cost = (total_usage * avg_price / 100.0) * 1.08
        
        solar_gen = sum(p.solar_kw for p in forecast)
        renewable_pct = (solar_gen / total_usage * 100) if total_usage > 0 else 0
        
        score = min(99, 65 + (peak / max(3.5, peak)) * 22)
        
        peak_time = forecast[0].timestamp
        low_price_idx = min(range(len(forecast)), 
                            key=lambda i: forecast[i].price_cents_kwh)
        high_price_idx = max(range(len(forecast)),
                             key=lambda i: forecast[i].price_cents_kwh)
        
        return EnergySummary(
            total_daily_usage_kwh=round(total_usage, 2),
            peak_demand_kw=round(peak, 2),
            average_price_cents_kwh=round(avg_price, 2),
            estimated_cost_usd=round(cost, 2),
            renewable_share_pct=round(renewable_pct, 2),
            demand_response_score=round(score, 2),
            solar_generation_kwh=round(solar_gen, 2),
            peak_demand_time=peak_time,
            lowest_price_time=forecast[low_price_idx].timestamp,
            highest_price_time=forecast[high_price_idx].timestamp,
            efficiency_rating=round(0.82, 2),
        )
    
    def get_daily_trends(self, days: int = 30) -> Dict[str, List[float]]:
        """Get daily energy trends."""
        return {
            "dates": [f"2024-09-{i:02d}" for i in range(1, days + 1)],
            "usage_kwh": [20 + i * 0.3 for i in range(days)],
            "cost_usd": [2.40 + i * 0.04 for i in range(days)],
            "savings_usd": [0.50 + i * 0.08 for i in range(days)],
        }
    
    def calculate_roi(self, appliance: Appliance, annual_usage_kwh: float,
                     avg_price_kwh: float) -> Dict[str, float]:
        """Calculate ROI for smart appliance."""
        annual_cost = appliance.annual_cost_usd
        savings_pct = 0.18
        annual_savings = annual_cost * savings_pct
        payback_years = appliance.annual_cost_usd / annual_savings if annual_savings > 0 else 0
        
        return {
            "annual_cost_usd": annual_cost,
            "annual_savings_usd": annual_savings,
            "payback_period_years": payback_years,
            "roi_percentage": (annual_savings / annual_cost * 100) if annual_cost > 0 else 0,
            "lifetime_savings_usd": annual_savings * min(15, appliance.expected_lifespan_years),
        }


# ═══════════════════════════════════════════════════════════════════════════
# 8. API RESPONSE BUILDERS
# ═══════════════════════════════════════════════════════════════════════════

class APIResponseBuilder:
    """Builder for API responses."""
    
    @staticmethod
    def build_overview(profile: HouseholdProfile, appliances: List[Appliance],
                      forecast: List[ForecastPoint],
                      optimization: Dict[str, Any]) -> Dict[str, Any]:
        """Build overview response."""
        analytics = EnergyAnalytics(profile)
        summary = analytics.calculate_summary(forecast)
        
        return {
            "profile": profile.to_dict(),
            "summary": summary.to_dict(),
            "appliances_count": len(appliances),
            "recommendations_count": len(optimization["recommendations"]),
            "estimated_savings_usd": optimization["summary"]["estimated_savings_usd"],
            "peak_reduction_kw": optimization["summary"]["peak_reduction_kw"],
            "status": "healthy",
            "last_updated": datetime.now().isoformat(),
        }
    
    @staticmethod
    def build_forecast_response(forecast: List[ForecastPoint]) -> Dict[str, Any]:
        """Build forecast response."""
        if not forecast:
            return {"points": [], "summary": {}}
        
        analytics = EnergyAnalytics(build_household_profile())
        summary = analytics.calculate_summary(forecast)
        
        return {
            "points": [p.to_dict() for p in forecast],
            "summary": summary.to_dict(),
            "hours": len(forecast),
        }
    
    @staticmethod
    def build_health_response() -> Dict[str, Any]:
        """Build health check response."""
        return {
            "status": "ok",
            "app": SETTINGS.app_name,
            "version": SETTINGS.app_version,
            "timestamp": datetime.now().isoformat(),
            "services": {
                "forecast": "operational",
                "optimization": "operational",
                "analytics": "operational",
            },
        }


# ═══════════════════════════════════════════════════════════════════════════
# 9. MAIN APPLICATION SERVICE
# ════════════════════════════════════════════════════════════════════════��══

class WattWiseService:
    """Main WattWise application service."""
    
    def __init__(self):
        self.profile = build_household_profile()
        self.appliances = build_appliances()
        self.weather_provider = MockWeatherProvider()
        self.forecasting_engine = ForecastingEngine(
            self.profile, self.weather_provider
        )
        self.optimization_engine = OptimizationEngine(self.profile)
        self.analytics = EnergyAnalytics(self.profile)
        self.last_update = datetime.now()
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get system health status."""
        return APIResponseBuilder.build_health_response()
    
    def get_overview(self) -> Dict[str, Any]:
        """Get system overview."""
        forecast = self.forecasting_engine.generate_forecast(24)
        optimization = self.optimization_engine.optimize_schedule(
            self.appliances, forecast
        )
        
        return APIResponseBuilder.build_overview(
            self.profile, self.appliances, forecast, optimization
        )
    
    def get_forecast(self, hours: int = 24) -> Dict[str, Any]:
        """Get energy forecast."""
        forecast = self.forecasting_engine.generate_forecast(hours)
        return APIResponseBuilder.build_forecast_response(forecast)
    
    def get_appliances(self) -> Dict[str, Any]:
        """Get appliance information."""
        return {
            "count": len(self.appliances),
            "items": [app.to_dict() for app in self.appliances],
        }
    
    def get_optimization(self) -> Dict[str, Any]:
        """Get optimization recommendations."""
        forecast = self.forecasting_engine.generate_forecast(24)
        return self.optimization_engine.optimize_schedule(
            self.appliances, forecast
        )
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics."""
        forecast = self.forecasting_engine.generate_forecast(30 * 24)
        return {
            "summary": self.analytics.calculate_summary(forecast).to_dict(),
            "trends": self.analytics.get_daily_trends(30),
            "appliance_roi": {
                app.id: self.analytics.calculate_roi(
                    app, 500, 0.25
                ) for app in self.appliances
            },
        }


# ═══════════════════════════════════════════════════════════════════════════
# 10. DEMONSTRATION & TESTING
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Main execution function."""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "WATTWISE - AI-DRIVEN HOME ENERGY MANAGEMENT" + " " * 20 + "║")
    print("╚" + "═" * 78 + "╝\n")
    
    service = WattWiseService()
    
    print("[1] System Health Status:")
    print("-" * 80)
    health = service.get_health_status()
    print(json.dumps(health, indent=2))
    
    print("\n[2] System Overview:")
    print("-" * 80)
    overview = service.get_overview()
    print(json.dumps({k: v for k, v in overview.items() if k != 'profile'}, indent=2))
    
    print("\n[3] Appliances Fleet:")
    print("-" * 80)
    appliances_data = service.get_appliances()
    print(f"Total Appliances: {appliances_data['count']}")
    for app in appliances_data['items'][:3]:
        print(f"  - {app['name']}: {app['power_kw']} kW (Priority: {app['priority']})")
    
    print("\n[4] Optimization Recommendations:")
    print("-" * 80)
    optimization = service.get_optimization()
    print(f"Savings Summary: ${optimization['summary']['estimated_savings_usd']} USD")
    print(f"Peak Reduction: {optimization['summary']['peak_reduction_kw']} kW")
    print(f"Recommendations: {len(optimization['recommendations'])}")
    
    print("\n[5] Analytics & Trends:")
    print("-" * 80)
    analytics_data = service.get_analytics()
    print(json.dumps(analytics_data['summary'], indent=2))
    
    print("\n" + "═" * 80)
    print("WattWise Service Successfully Initialized")
    print("═" * 80 + "\n")


if __name__ == "__main__":
    main()
