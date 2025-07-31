import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import ItineraryForm from './pages/ItineraryForm'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<div>Welcome to ItinerAIry</div>} />
        <Route path="/itineraryForm" element={<ItineraryForm />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
)
