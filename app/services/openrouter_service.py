import json
import requests
from app.config import settings
from app.prompts.qualification import QUALIFICATION_SYSTEM_PROMPT, build_lead_prompt
from app.utils.logger import logger

def qualify_lead(lead_data: dict) -> dict:
    """
    Evaluates the lead using OpenRouter and returns the status and reason.
    Returns a dict with 'status' ("Qualified" or "Not Interested") and 'reason'.
    """
    logger.info(f"Qualifying lead ID: {lead_data.get('id')}")
    user_prompt = build_lead_prompt(lead_data)
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": settings.ai_model,
        "messages": [
            {"role": "system", "content": QUALIFICATION_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "response_format": { "type": "json_object" },
        "temperature": settings.ai_temperature,
        "max_tokens": settings.ai_max_tokens
    }
    
    try:
        logger.debug(f"Calling OpenRouter API with model {settings.ai_model}")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        response_data = response.json()
        result_text = response_data["choices"][0]["message"]["content"]
        
        result = json.loads(result_text)
        # Ensure status is one of the expected values
        if result.get("status") not in ["Qualified", "Not Interested"]:
            result["status"] = "Not Interested"
            
        logger.info(f"Lead qualified as: {result.get('status')}")
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"OpenRouter API error: {str(e)}")
        return {
            "status": "Not Interested",
            "reason": f"OpenRouter API error: {str(e)}"
        }
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        logger.error(f"Failed to parse AI response: {str(e)}")
        return {
            "status": "Not Interested",
            "reason": f"Failed to parse AI response: {str(e)}"
        }
