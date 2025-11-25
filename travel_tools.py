"""
Travel Planner AI Tools
Implements 4 tools: Weather, Attractions, Budget Optimizer, and Flight/Hotel Search
"""
from typing import Dict, List, Any
from langchain.tools import tool
import requests
import json


@tool
def get_weather_forecast(city: str, days: int = 5) -> str:
    """
    Get weather forecast for a city using OpenWeatherMap API (free tier).
    
    Args:
        city: Name of the city
        days: Number of days to forecast (max 5)
    
    Returns:
        Weather forecast information as a string
    """
    try:
        # Using OpenWeatherMap free API
        # Note: In production, use environment variable for API key
        api_key = "demo_key"  # Replace with actual key or use env var
        base_url = "http://api.openweathermap.org/data/2.5/forecast"
        
        # For demo purposes, return mock data
        # In production, uncomment below:
        # response = requests.get(f"{base_url}?q={city}&appid={api_key}&units=metric")
        # data = response.json()
        
        # Mock weather data for demo
        mock_weather = {
            "city": city,
            "forecast": [
                {"day": 1, "temp": "22°C", "condition": "Sunny", "humidity": "65%"},
                {"day": 2, "temp": "24°C", "condition": "Partly Cloudy", "humidity": "70%"},
                {"day": 3, "temp": "21°C", "condition": "Rainy", "humidity": "80%"},
                {"day": 4, "temp": "23°C", "condition": "Sunny", "humidity": "68%"},
                {"day": 5, "temp": "25°C", "condition": "Clear", "humidity": "62%"},
            ]
        }
        
        result = f"Weather forecast for {city}:\n"
        for day in mock_weather["forecast"][:days]:
            result += f"Day {day['day']}: {day['temp']}, {day['condition']}, Humidity: {day['humidity']}\n"
        
        return result
    except Exception as e:
        return f"Error fetching weather: {str(e)}"


@tool
def search_tourist_attractions(city: str, category: str = "all") -> str:
    """
    Search for tourist attractions in a city.
    
    Args:
        city: Name of the city
        category: Type of attraction (museums, parks, landmarks, all)
    
    Returns:
        List of tourist attractions with details
    """
    # Mock attraction database
    attractions_db = {
        "paris": [
            {"name": "Eiffel Tower", "type": "landmark", "rating": 4.8, "price": "€25"},
            {"name": "Louvre Museum", "type": "museum", "rating": 4.9, "price": "€17"},
            {"name": "Notre-Dame Cathedral", "type": "landmark", "rating": 4.7, "price": "Free"},
            {"name": "Champs-Élysées", "type": "landmark", "rating": 4.6, "price": "Free"},
        ],
        "tokyo": [
            {"name": "Tokyo Skytree", "type": "landmark", "rating": 4.7, "price": "¥2,100"},
            {"name": "Senso-ji Temple", "type": "landmark", "rating": 4.6, "price": "Free"},
            {"name": "Shibuya Crossing", "type": "landmark", "rating": 4.5, "price": "Free"},
            {"name": "Tokyo National Museum", "type": "museum", "rating": 4.8, "price": "¥1,000"},
        ],
        "new york": [
            {"name": "Statue of Liberty", "type": "landmark", "rating": 4.7, "price": "$24"},
            {"name": "Central Park", "type": "park", "rating": 4.8, "price": "Free"},
            {"name": "Metropolitan Museum of Art", "type": "museum", "rating": 4.9, "price": "$30"},
            {"name": "Times Square", "type": "landmark", "rating": 4.6, "price": "Free"},
        ],
        "london": [
            {"name": "Big Ben", "type": "landmark", "rating": 4.7, "price": "Free"},
            {"name": "British Museum", "type": "museum", "rating": 4.8, "price": "Free"},
            {"name": "Tower Bridge", "type": "landmark", "rating": 4.6, "price": "£12"},
            {"name": "Hyde Park", "type": "park", "rating": 4.7, "price": "Free"},
        ],
    }
    
    city_lower = city.lower()
    if city_lower not in attractions_db:
        # Default attractions for unknown cities
        attractions = [
            {"name": f"{city} City Center", "type": "landmark", "rating": 4.5, "price": "Free"},
            {"name": f"{city} Museum", "type": "museum", "rating": 4.4, "price": "$15"},
            {"name": f"{city} Park", "type": "park", "rating": 4.3, "price": "Free"},
        ]
    else:
        attractions = attractions_db[city_lower]
    
    # Filter by category if specified
    if category != "all":
        attractions = [a for a in attractions if a["type"] == category]
    
    result = f"Tourist attractions in {city}:\n"
    for i, attr in enumerate(attractions, 1):
        result += f"{i}. {attr['name']} ({attr['type']}) - Rating: {attr['rating']}/5, Price: {attr['price']}\n"
    
    return result


@tool
def optimize_budget(destinations: List[str], total_budget: float, days_per_destination: List[int]) -> str:
    """
    Optimize budget allocation across multiple destinations.
    
    Args:
        destinations: List of destination cities
        total_budget: Total budget in USD
        days_per_destination: Number of days to spend in each destination
    
    Returns:
        Budget breakdown and recommendations
    """
    if len(destinations) != len(days_per_destination):
        return "Error: Number of destinations must match number of days"
    
    total_days = sum(days_per_destination)
    daily_budget = total_budget / total_days
    
    # Cost estimates per day (in USD)
    cost_estimates = {
        "paris": 150,
        "tokyo": 120,
        "new york": 200,
        "london": 180,
    }
    
    result = f"Budget Optimization for {total_budget} USD:\n"
    result += f"Total days: {total_days}\n"
    result += f"Average daily budget: ${daily_budget:.2f}\n\n"
    
    allocated_budget = 0
    for i, (dest, days) in enumerate(zip(destinations, days_per_destination), 1):
        dest_lower = dest.lower()
        estimated_daily = cost_estimates.get(dest_lower, 100)
        allocated = days * estimated_daily
        allocated_budget += allocated
        
        result += f"Destination {i}: {dest} ({days} days)\n"
        result += f"  Estimated cost: ${allocated:.2f} (${estimated_daily}/day)\n"
        result += f"  Recommended budget: ${days * daily_budget:.2f}\n"
        
        if allocated > days * daily_budget * 1.2:
            result += f"  ⚠️ Warning: This destination may exceed budget\n"
        result += "\n"
    
    remaining = total_budget - allocated_budget
    result += f"Remaining budget: ${remaining:.2f}\n"
    
    if remaining < 0:
        result += "⚠️ Budget exceeded! Consider reducing days or choosing cheaper destinations.\n"
    elif remaining > total_budget * 0.2:
        result += "✅ Good budget allocation with buffer for unexpected expenses.\n"
    
    return result


@tool
def search_flights_hotels(origin: str, destination: str, departure_date: str, return_date: str = None) -> str:
    """
    Search for flights and hotels (mock implementation).
    In production, integrate with Amadeus API or similar.
    
    Args:
        origin: Origin city
        destination: Destination city
        departure_date: Departure date (YYYY-MM-DD)
        return_date: Return date (YYYY-MM-DD), optional for one-way
    
    Returns:
        Flight and hotel options with prices
    """
    # Mock flight and hotel data
    mock_flights = [
        {"airline": "Air Travel Co", "price": 450, "duration": "8h 30m", "stops": 1},
        {"airline": "Budget Airlines", "price": 320, "duration": "10h 15m", "stops": 2},
        {"airline": "Premium Airways", "price": 680, "duration": "7h 45m", "stops": 0},
    ]
    
    mock_hotels = [
        {"name": "Grand Hotel", "price_per_night": 120, "rating": 4.5, "location": "City Center"},
        {"name": "Budget Inn", "price_per_night": 60, "rating": 3.8, "location": "Near Airport"},
        {"name": "Luxury Resort", "price_per_night": 250, "rating": 4.9, "location": "Waterfront"},
    ]
    
    result = f"Flight & Hotel Search: {origin} → {destination}\n"
    result += f"Departure: {departure_date}"
    if return_date:
        result += f", Return: {return_date}\n\n"
    else:
        result += " (One-way)\n\n"
    
    result += "FLIGHT OPTIONS:\n"
    for i, flight in enumerate(mock_flights, 1):
        result += f"{i}. {flight['airline']}: ${flight['price']}, Duration: {flight['duration']}, Stops: {flight['stops']}\n"
    
    result += "\nHOTEL OPTIONS:\n"
    for i, hotel in enumerate(mock_hotels, 1):
        result += f"{i}. {hotel['name']} ({hotel['location']}): ${hotel['price_per_night']}/night, Rating: {hotel['rating']}/5\n"
    
    return result


# Export all tools
TRAVEL_TOOLS = [
    get_weather_forecast,
    search_tourist_attractions,
    optimize_budget,
    search_flights_hotels,
]

