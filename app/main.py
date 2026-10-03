"""API routes for the WattWise dashboard."""

from __future__ import annotations

from fastapi import APIRouter

from app.config import SETTINGS
from app.data.sample_data import build_appliances, build_household_profile
from app.models import HouseholdProfile
from app.services.forecast import build_forecast_payload, generate_forecast, summarize_forecast
from app.services.optimizer import optimize_schedule

router = APIRouter(prefix=SETTINGS.api_prefix)


@router.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "app": SETTINGS.app_name,
        "version": SETTINGS.app_version,
        "message": "WattWise energy management service is running.",
    }


@router.get("/overview")
def get_overview() -> dict:
    profile = build_household_profile()
    appliances = build_appliances()
    forecast = generate_forecast(profile, hours=24)
    summary = summarize_forecast(forecast)
    optimization = optimize_schedule(profile, appliances, forecast)

    return {
        "profile": profile.to_dict(),
        "summary": summary.to_dict(),
        "appliances_count": len(appliances),
        "recommendations_count": len(optimization["recommendations"]),
        "estimated_savings_usd": optimization["summary"]["estimated_savings_usd"],
        "peak_reduction_kw": optimization["summary"]["peak_reduction_kw"],
        "status": "healthy",
    }


@router.get("/forecast")
def get_forecast() -> dict:
    profile = build_household_profile()
    payload = build_forecast_payload(profile, hours=24)
    return payload


@router.get("/appliances")
def get_appliances() -> dict:
    appliances = build_appliances()
    return {
        "count": len(appliances),
        "items": [item.to_dict() for item in appliances],
    }


@router.get("/optimization")
def get_optimization() -> dict:
    profile = build_household_profile()
    appliances = build_appliances()
    forecast = generate_forecast(profile, hours=24)
    optimization = optimize_schedule(profile, appliances, forecast)
    return optimization


@router.get("/meta")
def get_meta() -> dict:
    return {
        "app": SETTINGS.app_name,
        "description": SETTINGS.app_description,
        "version": SETTINGS.app_version,
        "routes": [
            "/api/health",
            "/api/overview",
            "/api/forecast",
            "/api/appliances",
            "/api/optimization",
        ],
    }
