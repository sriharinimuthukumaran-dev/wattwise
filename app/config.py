"""Application configuration settings for WattWise."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class AppSettings:
    app_name: str = "WattWise"
    app_version: str = "1.0.0"
    app_description: str = "AI-Driven Home Energy Management and Appliance-Level Optimization"
    api_prefix: str = "/api"
    default_timezone: str = "UTC"
    max_forecast_hours: int = 48
    default_peak_threshold_kw: float = 6.0
    default_price_floor: float = 0.12
    default_price_ceiling: float = 0.42

    def to_dict(self) -> Dict[str, object]:
        return {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "app_description": self.app_description,
            "api_prefix": self.api_prefix,
            "default_timezone": self.default_timezone,
            "max_forecast_hours": self.max_forecast_hours,
            "default_peak_threshold_kw": self.default_peak_threshold_kw,
            "default_price_floor": self.default_price_floor,
            "default_price_ceiling": self.default_price_ceiling,
        }


SETTINGS = AppSettings()


def get_default_appliance_categories() -> List[str]:
    return [
        "HVAC",
        "Water Heating",
        "Laundry",
        "Kitchen",
        "EV Charging",
        "Thermal Storage",
        "Pool",
        "General",
    ]
