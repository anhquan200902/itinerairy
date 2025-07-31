def add_cost_to_itinerary(itinerary: list[dict]) -> list[dict]:
    """
    Add rough per-activity cost estimates (very naive).
    """
    for day in itinerary:
        for activity in day.get("activities", []):
            desc = activity.get("description", "").lower()
            cost = 0

            if any(keyword in desc for keyword in ["museum", "gallery", "temple", "tour"]):
                cost = 10
            elif any(keyword in desc for keyword in ["hiking", "beach", "market", "walk"]):
                cost = 0
            elif any(keyword in desc for keyword in ["dinner", "lunch", "restaurant", "meal"]):
                cost = 15
            elif "hotel" in desc or "accommodation" in desc:
                cost = 60
            else:
                cost = 5  # default

            activity["estimated_cost"] = cost

    return itinerary


def generate_cost_summary(
    parsed: dict,
    itinerary: list[dict],
    budget_amount: float,
    currency: str
) -> dict:
    """
    Sum up estimated costs and compare to budget.
    """
    total = 0
    for day in itinerary:
        for activity in day.get("activities", []):
            total += activity.get("estimated_cost", 0)

    packing_list_cost = len(parsed.get("packing_list", [])) * 2  # estimate $2 per item
    total += packing_list_cost

    return {
        "estimated_total": round(total, 2),
        "budget": round(budget_amount, 2),
        "packing_list_cost": packing_list_cost,
        "within_budget": total <= budget_amount,
        "currency": currency
    }
