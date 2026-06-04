# Vedanco RevenueOS

FastAPI backend for Vedanco RevenueOS with Baserow and OpenAI integration.

## API Routes

Below is a list of all available API routes in the application:

### General
- `GET /` - Root endpoint to verify API is running.
- `GET /health` - Health check endpoint for monitoring.

### Leads
- `POST /lead` - Create a new lead.
- `GET /leads` - Get all leads.
- `GET /lead/{id}` - Get a specific lead by ID.
- `PUT /lead/{id}` - Update a specific lead by ID.
- `DELETE /lead/{id}` - Delete a specific lead by ID.

### Appointments
- `POST /appointment` - Create a new appointment.
- `GET /appointments` - Get a list of appointments.
- `PUT /appointment/{id}` - Update a specific appointment by ID.
- `DELETE /appointment/{id}` - Delete a specific appointment by ID.

### Qualification
- `POST /qualify/{lead_id}` - Qualify a specific lead.

### Dashboard
- `GET /dashboard` - Get dashboard metrics.

### Activities
- `GET /activities/{lead_id}` - Get activities for a specific lead.
