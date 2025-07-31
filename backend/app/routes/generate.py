from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.schemas.generate_schema import GenerateRequest
from pydantic import BaseModel, field_validator
import json

from app.utils.llm import call_api_with_fallback
from app.utils.prompt import build_prompt
from app.utils.validation import validate_request, validate_response
from app.utils.cost import add_cost_to_itinerary, generate_cost_summary

router = APIRouter()

class GenerateResponse(BaseModel):
    itinerary: list
    packingList: list
    costSummary: dict
    groupSize: int

@router.post('')
async def generate_itinerary(req: Request):
    try:
        body = await req.json()
        data = GenerateRequest(**body)

        # Build prompt
        prompt = build_prompt(
            destination=data.destination,
            duration=data.duration,
            groupSize=str(data.groupSize),
            budget=str(data.budgetAmount),
            currency=data.budgetCurrency,
            interests=data.interests,
            must_see=data.mustSee,
            custom=data.customRequest,
            from_date=data.fromDate,
            activities=data.activities,
        )

        # Call LLM
        raw = await call_api_with_fallback(prompt)
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            return JSONResponse(
                status_code=500,
                content={'message': 'Malformed response from AI'},
            )
        
        if not validate_response(parsed):
            return JSONResponse(
                status_code=500,
                content={'message': 'Invalid response structure from AI'},
            )
        
        # Post-process response
        itinerary = add_cost_to_itinerary(parsed['itinerary'])
        cost_summary = generate_cost_summary(parsed, itinerary, data.budgetAmount, data.budgetCurrency)

        return JSONResponse(
            content={
                'itinerary': itinerary,
                'packingList': parsed['packing_list'],
                'costSummary': cost_summary,
                'groupSize': data.groupSize
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={'message': 'Internal server error', 'details': str(e)},
        )