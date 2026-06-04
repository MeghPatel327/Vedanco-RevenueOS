"use client";

import { useEffect, useState } from "react";
import { api, Lead } from "@/lib/api";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { useRouter } from "next/navigation";

export default function LeadsPage() {
  const router = useRouter();
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");

  useEffect(() => {
    const fetchLeads = async () => {
      try {
        const data = await api.getLeads();
        setLeads(data);
      } catch (err) {
        console.error("Failed to fetch leads", err);
      } finally {
        setLoading(false);
      }
    };
    fetchLeads();
  }, []);

  const getStatusColor = (status: string | null) => {
    switch (status) {
      case "New Lead": return "default";
      case "Qualified": return "success";
      case "Appointment Booked": return "warning";
      case "Not Interested": return "destructive";
      default: return "secondary";
    }
  };

  const filteredLeads = leads.filter(lead => {
    const matchesSearch = 
      (lead.name?.toLowerCase().includes(search.toLowerCase()) || "") ||
      (lead.email?.toLowerCase().includes(search.toLowerCase()) || "");
    const matchesStatus = statusFilter === "ALL" || lead.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Leads</h2>
      </div>

      <div className="flex items-center space-x-4">
        <div className="w-1/3">
          <Input 
            placeholder="Search leads by name or email..." 
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <Select value={statusFilter} onValueChange={(value) => setStatusFilter(value || "ALL")}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Filter by status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="ALL">All Statuses</SelectItem>
            <SelectItem value="New Lead">New Lead</SelectItem>
            <SelectItem value="Qualified">Qualified</SelectItem>
            <SelectItem value="Appointment Booked">Appointment Booked</SelectItem>
            <SelectItem value="Not Interested">Not Interested</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="rounded-md border bg-card">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Company</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Created At</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={5} className="h-24 text-center">Loading...</TableCell>
              </TableRow>
            ) : filteredLeads.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} className="h-24 text-center">No leads found.</TableCell>
              </TableRow>
            ) : (
              filteredLeads.map((lead) => (
                <TableRow 
                  key={lead.id} 
                  className="cursor-pointer hover:bg-muted/50"
                  onClick={() => router.push(`/leads/${lead.id}`)}
                >
                  <TableCell className="font-medium">{lead.name}</TableCell>
                  <TableCell>{lead.email}</TableCell>
                  <TableCell>{lead.company || "-"}</TableCell>
                  <TableCell>
                    {lead.status && (
                      <Badge variant={getStatusColor(lead.status) as any}>
                        {lead.status}
                      </Badge>
                    )}
                  </TableCell>
                  <TableCell className="text-right">{lead.created_at}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
