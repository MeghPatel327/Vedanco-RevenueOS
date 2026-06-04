import json
import requests
from app.config import settings
from app.prompts.qualification import QUALIFICATION_SYSTEM_PROMPT, build_lead_prompt

def qualify_lead(lead_data: dict) -> dict:
    """
    Evaluates the lead using OpenRouter and returns the status and reason.
    Returns a dict with 'status' ("Qualified" or "Not Interested") and 'reason'.
    """
    user_prompt = build_lead_prompt(lead_data)
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": settings.openrouter_model,
        "messages": [
            {"role": "system", "content": QUALIFICATION_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "response_format": { "type": "json_object" },
        "temperature": 0.2
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        response_data = response.json()
        result_text = response_data["choices"][0]["message"]["content"]
        
        result = json.loads(result_text)
        # Ensure status is one of the expected values
        if result.get("status") not in ["Qualified", "Not Interested"]:
            result["status"] = "Not Interested"
        return result
    except requests.exceptions.RequestException as e:
        return {
            "status": "Not Interested",
            "reason": f"OpenRouter API error: {str(e)}"
        }
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return {
            "status": "Not Interested",
            "reason": f"Failed to parse AI response: {str(e)}"
        }
