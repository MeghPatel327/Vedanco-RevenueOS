"use client";

import { useEffect, useState } from "react";
import { api, Appointment } from "@/lib/api";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { Trash2 } from "lucide-react";

export default function AppointmentsPage() {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = async () => {
    try {
      const data = await api.getAppointments();
      setAppointments(data);
    } catch (err: any) {
      toast.error("Failed to fetch appointments: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = async (id: number) => {
    if (!confirm("Are you sure you want to cancel this appointment?")) return;
    
    try {
      await api.deleteAppointment(id);
      toast.success("Appointment cancelled successfully.");
      fetchAppointments();
    } catch (err: any) {
      toast.error("Failed to cancel appointment: " + err.message);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Appointments</h2>
      </div>

      <div className="rounded-md border bg-card">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Lead</TableHead>
              <TableHead>Date</TableHead>
              <TableHead>Time</TableHead>
              <TableHead>Booked On</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={5} className="h-24 text-center">Loading...</TableCell>
              </TableRow>
            ) : appointments.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} className="h-24 text-center">No appointments found.</TableCell>
              </TableRow>
            ) : (
              appointments.map((appt) => (
                <TableRow key={appt.id}>
                  <TableCell className="font-medium">
                    {appt.lead && appt.lead.length > 0 ? appt.lead[0].value : "Unknown Lead"}
                  </TableCell>
                  <TableCell>{appt.appointment_date}</TableCell>
                  <TableCell>{appt.appointment_time}</TableCell>
                  <TableCell>{appt.created_at}</TableCell>
                  <TableCell className="text-right">
                    <Button 
                      variant="destructive" 
                      size="sm"
                      onClick={() => handleCancel(appt.id)}
                    >
                      <Trash2 className="h-4 w-4 mr-2" /> Cancel
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
