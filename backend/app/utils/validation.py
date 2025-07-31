def validate_response(data: dict) -> bool:
    """
    Validates the AI response structure.

    Expected structure:
    {
        "itinerary": [ { "day": int, "date": str, ... }, ... ],
        "packing_list": [ "Item 1", "Item 2", ... ]
    }
    """

    if not isinstance(data, dict):
        return False

    # Top-level keys
    if "itinerary" not in data or "packing_list" not in data:
        return False

    itinerary = data["itinerary"]
    packing_list = data["packing_list"]

    # Validate itinerary
    if not isinstance(itinerary, list) or not itinerary:
        return False
    for day in itinerary:
        if not isinstance(day, dict):
            return False
        required_day_fields = {"day", "date", "summary", "meals", "activities"}
        if not required_day_fields.issubset(day):
            return False
        if not isinstance(day["activities"], list):
            return False

    # Validate packing_list
    if not isinstance(packing_list, list):
        return False
    if not all(isinstance(item, str) for item in packing_list):
        return False

    return True

from app.schemas.generate_schema import GenerateRequest

def validate_request(data: GenerateRequest) -> bool:
    """
    Optional: additional checks not covered by Pydantic.
    Currently just ensures required fields are non-empty.
    """
    if not data.destination.strip():
        return False
    if data.duration <= 0:
        return False
    if data.groupSize <= 0:
        return False
    if data.budgetAmount < 0:
        return False
    if not data.budgetCurrency.strip():
        return False

    return True