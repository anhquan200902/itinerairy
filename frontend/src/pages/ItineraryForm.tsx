import React, { useState } from "react";
import axios from "axios";

type RequestData = {
  destination: string;
  duration: number;
  groupSize: number;
  budgetAmount: number;
  budgetCurrency: string;
  interests: string[];
  mustSee: string;
  customRequest: string;
  fromDate: string;
  activities: string[];
};

type ResponseData = {
  itinerary: any[];
  packingList: string[];
  costSummary: {
    estimated_total: number;
    budget: number;
    packing_list_cost: number;
    within_budget: boolean;
    currency: string;
  };
  groupSize: number;
};

export default function ItineraryForm() {
  const [form, setForm] = useState<RequestData>({
    destination: "",
    duration: 1,
    groupSize: 1,
    budgetAmount: 0,
    budgetCurrency: "USD",
    interests: [],
    mustSee: "",
    customRequest: "",
    fromDate: "",
    activities: [],
  });

  const [response, setResponse] = useState<ResponseData | null>(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);

    try {
      const res = await axios.post("http://localhost:8000/generate", {
        ...form,
        interests: form.interests.length ? form.interests : [],
        activities: form.activities.length ? form.activities : [],
      });
      setResponse(res.data);
    } catch (err) {
      console.error("API error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Plan Your Trip</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input name="destination" onChange={handleChange} value={form.destination} placeholder="Destination" className="w-full p-2 border" />
        <input name="duration" type="number" onChange={handleChange} value={form.duration} placeholder="Duration (days)" className="w-full p-2 border" />
        <input name="groupSize" type="number" onChange={handleChange} value={form.groupSize} placeholder="Group size" className="w-full p-2 border" />
        <input name="budgetAmount" type="number" onChange={handleChange} value={form.budgetAmount} placeholder="Budget" className="w-full p-2 border" />
        <input name="budgetCurrency" onChange={handleChange} value={form.budgetCurrency} placeholder="Currency" className="w-full p-2 border" />
        <input name="interests" onChange={(e) => setForm((f) => ({ ...f, interests: e.target.value.split(",") }))} placeholder="Interests (comma separated)" className="w-full p-2 border" />
        <input name="activities" onChange={(e) => setForm((f) => ({ ...f, activities: e.target.value.split(",") }))} placeholder="Activities (comma separated)" className="w-full p-2 border" />
        <textarea name="mustSee" onChange={handleChange} value={form.mustSee} placeholder="Must see" className="w-full p-2 border" />
        <textarea name="customRequest" onChange={handleChange} value={form.customRequest} placeholder="Custom request" className="w-full p-2 border" />
        <input name="fromDate" type="date" onChange={handleChange} value={form.fromDate} className="w-full p-2 border" />
        <button type="submit" disabled={loading} className="bg-blue-600 text-white px-4 py-2 rounded">
          {loading ? "Generating..." : "Generate Itinerary"}
        </button>
      </form>

      {response && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold">Itinerary</h2>
          {response.itinerary.map((day, i) => (
            <div key={i} className="border p-2 my-2">
              <strong>Day {day.day}:</strong> {day.summary}
              <ul className="ml-4 list-disc">
                {day.activities.map((act: any, j: number) => (
                  <li key={j}>
                    {act.time} – {act.description} (${act.estimated_cost || 0})
                  </li>
                ))}
              </ul>
            </div>
          ))}

          <h2 className="text-xl font-semibold mt-4">Packing List</h2>
          <ul className="ml-4 list-disc">
            {response.packingList.map((item, i) => <li key={i}>{item}</li>)}
          </ul>

          <h2 className="text-xl font-semibold mt-4">Cost Summary</h2>
          <p>Total: {response.costSummary.estimated_total} {response.costSummary.currency}</p>
          <p>Budget: {response.costSummary.budget} {response.costSummary.currency}</p>
          <p>Within Budget: {response.costSummary.within_budget ? "✅ Yes" : "❌ No"}</p>
        </div>
      )}
    </div>
  );
}
