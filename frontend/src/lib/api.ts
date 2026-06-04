import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

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
  lead?: any[];
}

export interface Activity {
  id: number;
  activity_type?: string;
  description?: string;
  timestamp: string;
  lead?: any[];
}

export interface QualificationResponse {
  message: string;
  new_status: string;
  reason: string;
  lead: Lead;
}

export const api = {
  getDashboardMetrics: async (): Promise<DashboardMetrics> => {
    const { data } = await apiClient.get('/dashboard');
    return data;
  },
  
  getLeads: async (): Promise<Lead[]> => {
    const { data } = await apiClient.get('/leads');
    return data;
  },
  
  getLeadById: async (id: number): Promise<Lead> => {
    const { data } = await apiClient.get(`/lead/${id}`);
    return data;
  },
  
  createLead: async (leadData: Partial<Lead>): Promise<Lead> => {
    const { data } = await apiClient.post('/lead', leadData);
    return data;
  },

  updateLead: async (id: number, leadData: Partial<Lead>): Promise<Lead> => {
    const { data } = await apiClient.put(`/lead/${id}`, leadData);
    return data;
  },

  deleteLead: async (id: number): Promise<void> => {
    await apiClient.delete(`/lead/${id}`);
  },
  
  qualifyLead: async (id: number): Promise<QualificationResponse> => {
    const { data } = await apiClient.post(`/qualify/${id}`);
    return data;
  },
  
  getAppointments: async (): Promise<Appointment[]> => {
    const { data } = await apiClient.get('/appointments');
    return data;
  },
    
  bookAppointment: async (apptData: { lead_id: number; appointment_date: string; appointment_time: string }): Promise<Appointment> => {
    const { data } = await apiClient.post('/appointment', apptData);
    return data;
  },

  updateAppointment: async (id: number, apptData: Partial<Appointment>): Promise<Appointment> => {
    const { data } = await apiClient.put(`/appointment/${id}`, apptData);
    return data;
  },

  deleteAppointment: async (id: number): Promise<void> => {
    await apiClient.delete(`/appointment/${id}`);
  },

  getActivities: async (leadId: number): Promise<Activity[]> => {
    const { data } = await apiClient.get(`/activities/${leadId}`);
    return data;
  }
};
