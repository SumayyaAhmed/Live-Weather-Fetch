import reflex as rx
import httpx
import asyncio
import logging
from typing import TypedDict, Any


class CurrentWeather(TypedDict):
    temperature_2m: float
    relative_humidity_2m: int
    weather_code: int
    wind_speed_10m: float


class WeatherData(TypedDict):
    city: str
    country: str
    temperature: float
    humidity: int
    weather_code: int
    weather_description: str
    weather_emoji: str
    wind_speed: float


class WeatherState(rx.State):
    is_loading: bool = False
    error_message: str = ""
    weather_data: WeatherData | None = None
    WEATHER_CODES: dict[int, tuple[str, str]] = {
        0: ("Clear sky", "☀️"),
        1: ("Mainly clear", "⛅"),
        2: ("Partly cloudy", "⛅"),
        3: ("Overcast", "☁️"),
        45: ("Fog", "🌫️"),
        48: ("Depositing rime fog", "🌫️"),
        51: ("Light drizzle", "🌦️"),
        53: ("Moderate drizzle", "🌦️"),
        55: ("Dense drizzle", "🌦️"),
        61: ("Slight rain", "🌧️"),
        63: ("Moderate rain", "🌧️"),
        65: ("Heavy rain", "🌧️"),
        71: ("Slight snow fall", "❄️"),
        73: ("Moderate snow fall", "❄️"),
        75: ("Heavy snow fall", "❄️"),
        80: ("Slight rain showers", "🌧️"),
        81: ("Moderate rain showers", "🌧️"),
        82: ("Violent rain showers", "🌧️"),
        95: ("Thunderstorm", "⛈️"),
        96: ("Thunderstorm with slight hail", "⛈️"),
        99: ("Thunderstorm with heavy hail", "⛈️"),
    }

    @rx.event
    async def get_weather(self, form_data: dict):
        city = form_data.get("city", "").strip()
        if not city:
            self.error_message = "City name cannot be empty."
            return
        self.is_loading = True
        self.error_message = ""
        self.weather_data = None
        yield
        try:
            geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
            async with httpx.AsyncClient() as client:
                geocoding_response = await client.get(geocoding_url)
                geocoding_response.raise_for_status()
                geocoding_data = geocoding_response.json()
            if not geocoding_data.get("results"):
                self.error_message = f"Could not find city: {city}"
                self.is_loading = False
                return
            location = geocoding_data["results"][0]
            lat = location["latitude"]
            lon = location["longitude"]
            city_name = location["name"]
            country = location.get("country", "")
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&timezone=auto"
            async with httpx.AsyncClient() as client:
                weather_response = await client.get(weather_url)
                weather_response.raise_for_status()
                api_weather_data = weather_response.json()
            current_weather: CurrentWeather = api_weather_data["current"]
            weather_code = current_weather["weather_code"]
            description, emoji = self.WEATHER_CODES.get(weather_code, ("Unknown", "🤷"))
            self.weather_data = {
                "city": city_name,
                "country": country,
                "temperature": current_weather["temperature_2m"],
                "humidity": current_weather["relative_humidity_2m"],
                "weather_code": weather_code,
                "weather_description": description,
                "weather_emoji": emoji,
                "wind_speed": current_weather["wind_speed_10m"],
            }
        except httpx.HTTPStatusError as e:
            logging.exception(f"API error: {e}")
            self.error_message = f"API error: {e.response.status_code}"
        except httpx.RequestError as e:
            logging.exception(f"Network error: {e}")
            self.error_message = "Network error. Please check your connection."
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
            self.error_message = "An unexpected error occurred."
        finally:
            self.is_loading = False