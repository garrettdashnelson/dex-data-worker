#!/usr/bin/env python3
"""Fetch weekly menu data from Nutrislice API."""

import requests
from datetime import date, timedelta

schools = [
    {
        "name": "franklin-ecc",
        "meal": "breakfast",
    },
    {
        "name": "horace-mann",
        "meal": "breakfast",
    }
]


def get_target_monday() -> date:
    """
    Get the target Monday date based on current day:
    - Mon-Fri: return the current or most recent Monday
    - Sat-Sun: return the next Monday
    """
    today = date.today()
    weekday = today.weekday()  # Monday=0, Sunday=6
    
    if weekday <= 4:  # Monday through Friday
        # Go back to this week's Monday
        return today - timedelta(days=weekday)
    else:  # Saturday (5) or Sunday (6)
        # Go forward to next Monday
        days_until_monday = 7 - weekday
        return today + timedelta(days=days_until_monday)


def fetch_menu(school_name: str, meal: str) -> list[dict]:
    """
    Fetch weekly menu data from Nutrislice API and extract menu info.
    
    Args:
        school_name: The school identifier (e.g., 'melrose-high-school')
        meal: The meal/menu type (e.g., 'lunch', 'breakfast')
    
    Returns:
        List of dicts with 'date' and 'food_name' for days with menu items
    """
    monday = get_target_monday()
    
    url = (
        f"https://melroseschools.api.nutrislice.com/menu/api/weeks/"
        f"school/{school_name}/menu-type/{meal}/"
        f"{monday.year}/{monday.month}/{monday.day}/?format=json"
    )
    
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    
    result = []
    for day in data.get("days", []):
        menu_items = day.get("menu_items", [])
        if len(menu_items) > 0:
            # Find the first menu_item where food is not null
            food_name = None
            for item in menu_items:
                if item.get("food") is not None:
                    food_name = item["food"].get("name")
                    break
            
            result.append({
                "date": day.get("date"),
                "food_name": food_name,
            })
    
    return result





if __name__ == "__main__":
    import json
    from pathlib import Path
    
    output_path = Path(__file__).parent.parent / "data-exports" / "menus.json"
    
    all_menus = {}
    for school in schools:
        menu_data = fetch_menu(school["name"], school["meal"])
        all_menus[school["name"]] = menu_data
    
    with open(output_path, "w") as f:
        json.dump(all_menus, f, indent=2)

