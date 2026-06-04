export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface DashboardMetrics {
  total_leads: number;
  qualified_leads: number;
  appointment_booked_leads: number;
  conversion_rate: number;
}

export interface Lead {
  id: number;
  name: string;
  email: string;
  phone?: string | null;
  company?: string | null;
  source?: string | null;
  service?: string | null;
  notes?: string | null;
  status?: string | null;
  created_at?: string | null;
}

export interface Appointment {
  id: number;
  appointment_date: string;
  appointment_time: string;
  created_at: string;
}

export interface QualificationResponse {
  message: string;
  new_status: string;
  reason: string;
  lead: Lead;
}

// Helper to handle API responses
async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const url = `${API_URL}${endpoint}`;
  
  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  const response = await fetch(url, { ...options, headers });
  
  if (!response.ok) {
    let errorMessage = "An error occurred while fetching data.";
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch (e) {}
    throw new Error(errorMessage);
  }

  return response.json();
}

export const api = {
  getDashboardMetrics: (): Promise<DashboardMetrics> => fetchAPI("/dashboard"),
  
  getLeads: (): Promise<Lead[]> => fetchAPI("/leads"),
  
  getLeadById: (id: number): Promise<Lead> => fetchAPI(`/lead/${id}`),
  
  qualifyLead: (id: number): Promise<QualificationResponse> => 
    fetchAPI(`/qualify/${id}`, { method: "POST" }),
    
  bookAppointment: (data: { lead_id: number; appointment_date: string; appointment_time: string }): Promise<Appointment> => 
    fetchAPI("/appointment", { 
      method: "POST", 
      body: JSON.stringify(data)
    })
};
