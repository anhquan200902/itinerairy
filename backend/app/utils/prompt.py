def build_prompt(
    destination: str,
    duration: int,
    groupSize: str,
    budget: str,
    currency: str,
    interests: list[str],
    must_see: str,
    custom: str,
    from_date: str,
    activities: list[str]
) -> str:
    prompt_parts = [
        f"Plan a {duration}-day trip to {destination} for a group of {groupSize} people.",
        f"The total budget is approximately {budget} {currency}.",
    ]

    if interests:
        prompt_parts.append(f"The group is interested in: {', '.join(interests)}.")
    if activities:
        prompt_parts.append(f"Preferred activities include: {', '.join(activities)}.")
    if must_see:
        prompt_parts.append(f"Must-see places: {must_see}.")
    if custom:
        prompt_parts.append(f"Additional request: {custom}")
    if from_date:
        prompt_parts.append(f"The trip should start on or after {from_date}.")

    prompt_parts.append(
        "\nReturn a JSON object with the following exact structure:\n"
        "```\n"
        "{\n"
        '  "itinerary": [\n'
        "    {\n"
        '      "day": 1,\n'
        '      "date": "YYYY-MM-DD",\n'
        '      "summary": "Brief day overview",\n'
        '      "meals": ["Breakfast", "Lunch", "Dinner"],\n'
        '      "activities": [\n'
        '        { "time": "HH:MM", "description": "activity" },\n'
        "        ...\n"
        "      ]\n"
        "    },\n"
        "    ...\n"
        "  ],\n"
        '  "packing_list": [\n'
        '    "Item 1", "Item 2", ...\n'
        "  ]\n"
        "}\n"
        "```"
    )

    return " ".join(prompt_parts)
