from pydantic import BaseModel, field_validator

class GenerateRequest(BaseModel):
    destination: str
    duration: int
    groupSize: int = 1
    budgetAmount: float = 0
    budgetCurrency: str = "USD"
    interests: list[str] = []
    mustSee: str = ""
    customRequest: str = ""
    fromDate: str = ""
    activities: list[str] = []

    @field_validator('destination', 'budgetCurrency')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()