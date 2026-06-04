"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { api, Lead } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { ArrowLeft, Sparkles, Calendar, Mail, Phone, Building, Briefcase } from "lucide-react";

export default function LeadDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const id = Number(params.id);

  const [lead, setLead] = useState<Lead | null>(null);
  const [loading, setLoading] = useState(true);
  const [qualifying, setQualifying] = useState(false);
  const [booking, setBooking] = useState(false);
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    fetchLead();
  }, [id]);

  const fetchLead = async () => {
    try {
      const data = await api.getLeadById(id);
      setLead(data);
    } catch (err: any) {
      toast.error("Failed to fetch lead: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleQualify = async () => {
    setQualifying(true);
    toast.info("Running AI qualification...");
    try {
      const result = await api.qualifyLead(id);
      toast.success(result.message);
      fetchLead(); // Refresh data
    } catch (err: any) {
      toast.error("Qualification failed: " + err.message);
    } finally {
      setQualifying(false);
    }
  };

  const handleBookAppointment = async (e: React.FormEvent) => {
    e.preventDefault();
    setBooking(true);
    try {
      await api.bookAppointment({
        lead_id: id,
        appointment_date: date,
        appointment_time: time,
      });
      toast.success("Appointment booked successfully!");
      setDialogOpen(false);
      fetchLead(); // Refresh data
    } catch (err: any) {
      toast.error("Failed to book appointment: " + err.message);
    } finally {
      setBooking(false);
    }
  };

  if (loading) {
    return <div className="animate-pulse">Loading lead details...</div>;
  }

  if (!lead) {
    return <div>Lead not found.</div>;
  }

  return (
    <div className="space-y-6 max-w-4xl">
      <Button variant="ghost" onClick={() => router.push("/leads")} className="mb-4">
        <ArrowLeft className="mr-2 h-4 w-4" /> Back to Leads
      </Button>

      <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">{lead.name}</h2>
          <div className="mt-2 flex items-center gap-2">
            <Badge variant="outline">{lead.status || "Unknown Status"}</Badge>
            <span className="text-sm text-muted-foreground">Added on {lead.created_at}</span>
          </div>
        </div>
        
        <div className="flex gap-2">
          <Button onClick={handleQualify} disabled={qualifying}>
            <Sparkles className="mr-2 h-4 w-4" />
            {qualifying ? "Qualifying..." : "Run AI Qualification"}
          </Button>

          <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
            <DialogTrigger render={<Button variant="secondary" />}>
              <Calendar className="mr-2 h-4 w-4" /> Book Appointment
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Book Appointment for {lead.name}</DialogTitle>
              </DialogHeader>
              <form onSubmit={handleBookAppointment} className="space-y-4 pt-4">
                <div className="space-y-2">
                  <Label htmlFor="date">Date</Label>
                  <Input 
                    id="date" 
                    type="date" 
                    required 
                    value={date} 
                    onChange={e => setDate(e.target.value)} 
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="time">Time</Label>
                  <Input 
                    id="time" 
                    type="time" 
                    required 
                    value={time} 
                    onChange={e => setTime(e.target.value)} 
                  />
                </div>
                <Button type="submit" className="w-full" disabled={booking}>
                  {booking ? "Booking..." : "Confirm Booking"}
                </Button>
              </form>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Contact Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-3 text-sm">
              <Mail className="h-4 w-4 text-muted-foreground" />
              <span>{lead.email}</span>
            </div>
            {lead.phone && (
              <div className="flex items-center gap-3 text-sm">
                <Phone className="h-4 w-4 text-muted-foreground" />
                <span>{lead.phone}</span>
              </div>
            )}
            {lead.company && (
              <div className="flex items-center gap-3 text-sm">
                <Building className="h-4 w-4 text-muted-foreground" />
                <span>{lead.company}</span>
              </div>
            )}
            {lead.service && (
              <div className="flex items-center gap-3 text-sm">
                <Briefcase className="h-4 w-4 text-muted-foreground" />
                <span>{lead.service}</span>
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Additional Details</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <span className="text-sm font-medium text-muted-foreground block mb-1">Source</span>
              <p className="text-sm">{lead.source || "N/A"}</p>
            </div>
            <div>
              <span className="text-sm font-medium text-muted-foreground block mb-1">Notes</span>
              <p className="text-sm whitespace-pre-wrap">{lead.notes || "No notes available."}</p>
            </div>
          </CardContent>
        </Card>
      </div>

    </div>
  );
}
