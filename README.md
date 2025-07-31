# ItinerAIry

An AI-powered travel itinerary generator that creates personalized travel plans based on user preferences, budget, and interests.

## Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
  - [Backend Architecture](#backend-architecture)
  - [Frontend Architecture](#frontend-architecture)
- [Core Functionality](#core-functionality)
  - [Backend Components](#backend-components)
  - [Frontend Components](#frontend-components)
- [Data Flow](#data-flow)
- [Technology Stack](#technology-stack)
- [Key Features](#key-features)
- [Setup and Running Instructions](#setup-and-running-instructions)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [Running the Application](#running-the-application)
- [API Specification](#api-specification)
- [Current Limitations](#current-limitations)
- [Potential Improvements](#potential-improvements)
- [Project Status](#project-status)

## Project Overview

ItinerAIry is a full-stack web application that leverages artificial intelligence to generate personalized travel itineraries. Users can input their destination, travel duration, group size, budget, interests, and other preferences to receive a comprehensive travel plan including daily activities, meal suggestions, and a packing list. The application also provides cost estimates and budget tracking to help users plan their trips effectively.

## Architecture

### Backend Architecture

The backend is built using FastAPI, a modern, fast web framework for building APIs with Python. It follows a modular architecture with clear separation of concerns:

- **Main Application**: [`app/main.py`](backend/app/main.py) - Entry point with CORS configuration and exception handling
- **Routes**: [`app/routes/generate.py`](backend/app/routes/generate.py) - API endpoint for itinerary generation
- **Schemas**: [`app/schemas/generate_schema.py`](backend/app/schemas/generate_schema.py) - Data validation models
- **Utilities**:
  - [`app/utils/llm.py`](backend/app/utils/llm.py) - LLM API integration with fallback mechanism
  - [`app/utils/prompt.py`](backend/app/utils/prompt.py) - Prompt building logic
  - [`app/utils/validation.py`](backend/app/utils/validation.py) - Request and response validation
  - [`app/utils/cost.py`](backend/app/utils/cost.py) - Cost estimation and budget tracking

### Frontend Architecture

The frontend is a React-based single-page application built with Vite:

- **Main Application**: [`src/main.tsx`](frontend/src/main.tsx) - Entry point with routing configuration
- **Components**: 
  - [`src/pages/ItineraryForm.tsx`](frontend/src/pages/ItineraryForm.tsx) - Main form component for trip planning
  - [`src/App.tsx`](frontend/src/App.tsx) - Root component (currently contains default Vite+React template)
- **Styling**: Basic CSS styling with responsive design

## Core Functionality

### Backend Components

1. **API Endpoint (`/generate`)**:
   - Accepts travel preferences via POST request
   - Validates input data using Pydantic models
   - Constructs prompts for AI models
   - Calls LLM APIs with fallback mechanism
   - Processes and validates AI responses
   - Adds cost estimates to activities
   - Generates budget summaries

2. **LLM Integration**:
   - Primary integration with Groq API using Llama 3.1 8B Instant model
   - Fallback to OpenRouter API using z-ai/glm-4.5-air:free model
   - Structured JSON responses with consistent schema

3. **Data Processing**:
   - Request validation for required fields
   - Response structure validation
   - Cost estimation for activities based on keywords
   - Budget comparison and tracking

### Frontend Components

1. **Trip Planning Form**:
   - Input fields for destination, duration, group size
   - Budget configuration with currency support
   - Interests and activities selection
   - Must-see places and custom requests
   - Date picker for trip start date

2. **Results Display**:
   - Day-by-day itinerary with activities and timings
   - Cost estimates for each activity
   - Packing list suggestions
   - Budget summary with within-budget indicator

## Data Flow

1. **User Input**:
   - User fills out the trip planning form in the frontend
   - Form data is validated and submitted to the backend

2. **Backend Processing**:
   - Request is validated using Pydantic schemas
   - Prompt is constructed based on user preferences
   - LLM API is called (Groq with OpenRouter fallback)
   - Response is validated and processed
   - Cost estimates are added to activities
   - Budget summary is generated

3. **Response Delivery**:
   - Processed data is returned to the frontend
   - Results are displayed in a user-friendly format
   - Itinerary, packing list, and cost summary are presented

## Technology Stack

### Backend
- **Framework**: FastAPI 0.116.1
- **Language**: Python 3.x
- **LLM Integration**: 
  - Groq API (Llama 3.1 8B Instant)
  - OpenRouter API (z-ai/glm-4.5-air:free)
- **Data Validation**: Pydantic 2.11.7
- **HTTP Client**: httpx 0.28.1
- **Environment Management**: python-dotenv 1.1.1
- **Server**: Uvicorn 0.35.0

### Frontend
- **Framework**: React 19.1.0
- **Language**: TypeScript
- **Build Tool**: Vite 7.0.4
- **HTTP Client**: Axios 1.11.0
- **Routing**: React Router DOM 7.7.1
- **Development**: ESLint, TypeScript

## Key Features

1. **AI-Powered Itinerary Generation**: Leverages advanced language models to create personalized travel plans
2. **Multi-LLM Support**: Fallback mechanism between Groq and OpenRouter APIs for reliability
3. **Budget Tracking**: Real-time cost estimation and budget comparison
4. **Flexible Input Options**: Comprehensive form with various travel preferences
5. **Structured Output**: Consistent JSON response format with detailed daily plans
6. **Packing List Generation**: AI-suggested packing items based on destination and activities
7. **Responsive Design**: Mobile-friendly interface for trip planning on any device

## Setup and Running Instructions

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn package manager
- API keys for Groq and OpenRouter (stored in `.env` file)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your API keys:
     ```
     GROQ_API_KEY=your_groq_api_key
     OPENROUTER_API_KEY=your_openrouter_api_key
     ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Running the Application

1. Start the backend server:
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```
   The backend will be available at `http://localhost:8000`

2. Start the frontend development server:
   ```bash
   cd frontend
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

3. Access the application:
   - Open `http://localhost:5173` in your browser
   - Navigate to `http://localhost:5173/itineraryForm` to use the trip planning form

## API Specification

### POST /generate

Generates a travel itinerary based on user preferences.

**Request Body:**
```json
{
  "destination": "string",
  "duration": "integer",
  "groupSize": "integer",
  "budgetAmount": "number",
  "budgetCurrency": "string",
  "interests": ["string"],
  "mustSee": "string",
  "customRequest": "string",
  "fromDate": "string",
  "activities": ["string"]
}
```

**Response Body:**
```json
{
  "itinerary": [
    {
      "day": "integer",
      "date": "string",
      "summary": "string",
      "meals": ["string"],
      "activities": [
        {
          "time": "string",
          "description": "string",
          "estimated_cost": "number"
        }
      ]
    }
  ],
  "packingList": ["string"],
  "costSummary": {
    "estimated_total": "number",
    "budget": "number",
    "packing_list_cost": "number",
    "within_budget": "boolean",
    "currency": "string"
  },
  "groupSize": "integer"
}
```

**Response Codes:**
- 200: Success
- 500: Internal server error or invalid AI response

## Current Limitations

1. **Cost Estimation**: Uses a naive keyword-based approach for cost estimation, which may not be accurate for all locations or activities
2. **LLM Dependency**: Relies on external AI services, which may have rate limits or downtime
3. **Limited Personalization**: Does not account for user's travel history or preferences beyond the current form inputs
4. **No User Authentication**: No user accounts or trip saving functionality
5. **Basic UI**: Current interface is functional but lacks advanced UI/UX features
6. **No Real-time Data**: Does not integrate with real-time data sources for weather, events, or pricing
7. **Limited Error Handling**: Basic error handling without detailed user feedback

## Potential Improvements

1. **Enhanced Cost Estimation**:
   - Integration with real pricing APIs
   - Location-specific cost databases
   - Dynamic pricing based on seasonality

2. **User Features**:
   - User authentication and profiles
   - Trip saving and sharing
   - Travel history and preferences learning

3. **UI/UX Enhancements**:
   - Interactive maps for itinerary visualization
   - Image uploads for destinations
   - Mobile app development
   - Dark mode and accessibility features

4. **Data Integration**:
   - Weather API integration
   - Real-time event and attraction data
   - Flight and hotel booking integration
   - Local transportation options

5. **AI Improvements**:
   - Fine-tuned models for travel planning
   - Multi-language support
   - Voice input capabilities
   - Image recognition for destination suggestions

6. **Performance & Scalability**:
   - Caching mechanisms
   - Database integration for storing trips
   - API rate limiting and optimization
   - Containerization with Docker

## Project Status

ItinerAIry is currently in active development with core functionality implemented. The application successfully generates travel itineraries using AI models and provides a functional user interface for trip planning. The project demonstrates a working full-stack architecture with proper separation of concerns and modern development practices.

The current version (1.0.0) includes:
- ✅ Basic itinerary generation
- ✅ Cost estimation and budget tracking
- ✅ Multi-LLM support with fallback
- ✅ Responsive web interface
- ✅ API documentation through FastAPI
- ✅ Data validation and error handling

Future development will focus on the improvements outlined above, with priority given to user experience enhancements and data integration features.