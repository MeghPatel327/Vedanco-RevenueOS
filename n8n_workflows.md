# n8n Workflow Architecture for Vedanco RevenueOS

These n8n workflows act as the central orchestration engine connecting Baserow (database events) with your FastAPI backend.

> [!NOTE]  
> To use these workflows, simply copy the JSON blocks and paste them directly onto your n8n workflow canvas. n8n will automatically parse the JSON and visually construct the nodes.

---

## Workflow 1: Lead Created Orchestration

**Trigger**: A new lead is added to Baserow.  
**Steps**:
1. **Trigger**: Catches the Webhook from Baserow when a row is inserted in the `Leads` table.
2. **Create Activity**: Uses the Baserow API to add a "Lead Created" record to the `Activities` table.
3. **Trigger AI Qualification**: Sends a POST request to your FastAPI backend (`/qualify/{lead_id}`).
4. **Update Lead Status**: (Optional via n8n) The FastAPI backend natively handles the status update internally during qualification, but n8n logs the final success status.

### JSON Definition

```json
{
  "name": "RevenueOS: Lead Created",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "vedanco-new-lead",
        "options": {}
      },
      "id": "e1a90c12-3b2d-4f8a-9a1b-cdef12345678",
      "name": "Baserow Webhook (New Lead)",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [ 200, 300 ]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://api.baserow.io/api/database/rows/table/1009954/?user_field_names=true",
        "authentication": "headerAuth",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            { "name": "activity_type", "value": "Lead Created" },
            { "name": "description", "value": "Lead entered the system via n8n integration." },
            { "name": "lead", "value": "={{ $json.body.row_id }}" }
          ]
        },
        "options": {}
      },
      "id": "a2b90c12-3b2d-4f8a-9a1b-cdef12345679",
      "name": "Create Activity",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [ 450, 300 ],
      "credentials": { "httpHeaderAuth": { "id": "baserow_token", "name": "Baserow API Token" } }
    },
    {
      "parameters": {
        "method": "POST",
        "url": "http://host.docker.internal:8000/qualify/{{ $('Baserow Webhook (New Lead)').item.json.body.row_id }}",
        "sendBody": false,
        "options": {}
      },
      "id": "b3c90c12-3b2d-4f8a-9a1b-cdef12345680",
      "name": "Trigger AI Qualification (FastAPI)",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [ 700, 300 ]
    }
  ],
  "connections": {
    "Baserow Webhook (New Lead)": {
      "main": [
        [ { "node": "Create Activity", "type": "main", "index": 0 } ]
      ]
    },
    "Create Activity": {
      "main": [
        [ { "node": "Trigger AI Qualification (FastAPI)", "type": "main", "index": 0 } ]
      ]
    }
  }
}
```

---

## Workflow 2: Appointment Booked

**Trigger**: A new appointment is scheduled (either via the frontend triggering a webhook or Baserow Row created).  
**Steps**:
1. **Trigger**: Catches the event payload containing `lead_id` and appointment details.
2. **Update Lead Status**: Calls Baserow to update the specific Lead's status to "Appointment Booked".
3. **Create Activity**: Logs the appointment in the `Activities` table.
4. **Log Event**: Sends a notification (e.g., to Slack/Discord or a local log file).

### JSON Definition

```json
{
  "name": "RevenueOS: Appointment Booked",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "vedanco-appointment",
        "options": {}
      },
      "id": "c4d90c12-3b2d-4f8a-9a1b-cdef12345681",
      "name": "Appointment Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [ 200, 500 ]
    },
    {
      "parameters": {
        "method": "PATCH",
        "url": "https://api.baserow.io/api/database/rows/table/1009952/{{ $json.body.lead_id }}/?user_field_names=true",
        "authentication": "headerAuth",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            { "name": "status", "value": "Appointment Booked" }
          ]
        },
        "options": {}
      },
      "id": "d5e90c12-3b2d-4f8a-9a1b-cdef12345682",
      "name": "Update Lead Status",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [ 450, 500 ],
      "credentials": { "httpHeaderAuth": { "id": "baserow_token", "name": "Baserow API Token" } }
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://api.baserow.io/api/database/rows/table/1009954/?user_field_names=true",
        "authentication": "headerAuth",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            { "name": "activity_type", "value": "Appointment Booked" },
            { "name": "description", "value": "An appointment was successfully scheduled." },
            { "name": "lead", "value": "={{ $('Appointment Webhook').item.json.body.lead_id }}" }
          ]
        },
        "options": {}
      },
      "id": "e6f90c12-3b2d-4f8a-9a1b-cdef12345683",
      "name": "Create Activity",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [ 700, 500 ],
      "credentials": { "httpHeaderAuth": { "id": "baserow_token", "name": "Baserow API Token" } }
    },
    {
      "parameters": {
        "options": {}
      },
      "id": "f7g90c12-3b2d-4f8a-9a1b-cdef12345684",
      "name": "Log Event (NoOp)",
      "type": "n8n-nodes-base.noOp",
      "typeVersion": 1,
      "position": [ 950, 500 ],
      "notes": "Replace this with Slack, Email, or Logger node"
    }
  ],
  "connections": {
    "Appointment Webhook": {
      "main": [
        [ { "node": "Update Lead Status", "type": "main", "index": 0 } ]
      ]
    },
    "Update Lead Status": {
      "main": [
        [ { "node": "Create Activity", "type": "main", "index": 0 } ]
      ]
    },
    "Create Activity": {
      "main": [
        [ { "node": "Log Event (NoOp)", "type": "main", "index": 0 } ]
      ]
    }
  }
}
```

## Security Best Practices
- **Authentication**: The HTTP nodes reaching out to Baserow use a predefined `headerAuth` credential type in n8n. Make sure you set up a Header Auth credential in n8n where `Name` is `Authorization` and `Value` is `Token YOUR_BASEROW_TOKEN`.
- **FastAPI Environment**: In the "Trigger AI Qualification" node, ensure the `url` matches your FastAPI backend's accessibility from n8n (e.g., using `http://host.docker.internal:8000` if running n8n locally via Docker).
