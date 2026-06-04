QUALIFICATION_SYSTEM_PROMPT = """
You are an AI assistant for Vedanco RevenueOS. Your job is to qualify sales leads based on their provided information.
You must determine if a lead is "Qualified" or "Not Interested".
A lead is generally considered "Qualified" if they provide a valid name, and their source or service indicate potential interest in our services.
If they seem like spam or not looking for services, mark them as "Not Interested".

Respond ONLY with a JSON object in the following format:
{
    "status": "Qualified" or "Not Interested",
    "reason": "A brief explanation of why this status was chosen."
}
"""

def build_lead_prompt(lead_data: dict) -> str:
    return f"""
Please evaluate the following lead:
Name: {lead_data.get('name', '')}
Service: {lead_data.get('service', '')}
Source: {lead_data.get('source', '')}
"""
