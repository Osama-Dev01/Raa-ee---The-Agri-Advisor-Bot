from dotenv import load_dotenv
import json
import requests
import os

# Load environment variables
load_dotenv(override=True)

# Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"



def find_and_print_crop_data(query, knowledge_base):
    """
    Searches for a crop name from the knowledge base within a user's query.

    Args:
        query (str): The English query from the user.
        knowledge_base (dict): The dictionary loaded from the JSON file.
    
    Returns:
        dict or None: Crop data if found, None otherwise
    """
    if not query or not knowledge_base:
        print("Error: Query or knowledge base is empty")
        return None
    
    query_lower = query.lower()
    available_crops = knowledge_base.keys()
    
    print(f"Searching for crops in query: '{query}'")
    print(f"Available crops: {list(available_crops)}")
    
    for crop_name in available_crops:
        if crop_name.lower() in query_lower:
            print(f"✓ Match Found: '{crop_name}' in query")
            crop_data = knowledge_base[crop_name]
            
            print(f"Retrieved data for {crop_name}:")
            print(json.dumps(crop_data, indent=2, ensure_ascii=False))
            
            return crop_data
    
    print("✗ No crop matches found in query")
    return None

def llm_response(query_text: str, crop_kb):
    """
    Sends the user's query and crop knowledge base to Groq LLM.
    Returns Urdu response from 'Raa'ee' bot.

    Args:
        query_text (str): User's query
        crop_kb (dict or str): Crop knowledge base data
    
    Returns:
        str: LLM response in Urdu
    """
    print("\n=== LLM REQUEST STARTED ===")
    
    # Verify API key
    if not GROQ_API_KEY:
        error_msg = "ERROR: GROQ_API_KEY not found in environment variables"
        print(error_msg)
        return "API کلیدیں غائب ہیں۔ براہ کرم سسٹم ایڈمن سے رابطہ کریں۔"
    
    # Prepare knowledge base context
    if isinstance(crop_kb, dict):
        kb_context = json.dumps(crop_kb, ensure_ascii=False, indent=2)
    else:
        kb_context = str(crop_kb)
    
    print(f"Query: {query_text}")
    print(f"Knowledge base context prepared ({len(kb_context)} characters)")

    # Construct LLM messages
    messages = [
    {
        "role": "system",
        "content": """
        آپ راعی ہیں - پاکستانی کسانوں کے لیے زرعی معاون۔

        **آپ کا کردار:** زرعی مشورہ دینا
        **زبان:** سادہ اردو
        **موضوعات:** فصلوں، کیڑوں، بیماریوں، کھاد، پانی

        **جواب دینے کا طریقہ:**
        - زرعی سوال → مکمل جواب
        - غیر زرعی سوال → "میں زراعت کے بارے میں مدد کر سکتا ہوں، کیا آپ کو کسی فصل کے بارے میں کوئی سوال ہے؟"

        **مثالیں:**
        سوال: "گندم کی کھاد" → "گندم میں ڈی اے پی بوائی کے وقت اور یوریا 25-30 دن بعد ڈالیں۔"
        سوال: "موٹرسائیکل" → "میں زراعت کے بارے میں مدد کر سکتا ہوں، کیا آپ کو کسی فصل کے بارے میں کوئی سوال ہے؟"
        """
    },
    {
        "role": "user",
        "content": f"""
        دستیاب زرعی ڈیٹا:
        {kb_context}

        درج ذیل سوال کا جواب دیں:
        "{query_text}"

        جواب سادہ اردو میں ہو اور عملی ہو۔
        """
    }
]

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",  # ✅ FIXED MODEL NAME
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        print("Sending request to Groq API...")
        
        response = requests.post(
            GROQ_API_URL, 
            headers=headers, 
            json=payload, 
            timeout=30
        )
        
        print(f"API Response Status: {response.status_code}")
        
        # Check for HTTP errors
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        
        # Debug: print API response structure
        print("API Response received successfully")
        print(f"Response keys: {data.keys()}")
        
        # Extract the response content
        if "choices" in data and len(data["choices"]) > 0:
            bot_reply = data["choices"][0]["message"]["content"].strip()
            print(f"✓ LLM Response: {bot_reply}")
            return bot_reply
        else:
            error_msg = "No choices in API response"
            print(f"ERROR: {error_msg}")
            return "معذرت، سرور سے مناسب جواب حاصل نہیں ہو سکا۔"
            
    except requests.exceptions.ConnectionError:
        error_msg = "Connection error - Check internet connection"
        print(f"ERROR: {error_msg}")
        return "معذرت، انٹرنیٹ کنکشن میں مسئلہ ہے۔ براہ کرم کنکشن چیک کریں۔"
        
    except requests.exceptions.Timeout:
        error_msg = "Request timeout"
        print(f"ERROR: {error_msg}")
        return "معذرت، سرور کا جواب موصول نہیں ہوا۔ براہ کرم دوبارہ کوشش کریں۔"
        
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP Error: {e.response.status_code} - {e.response.text}"
        print(f"ERROR: {error_msg}")
        
        if e.response.status_code == 401:
            return "API کلیدیں غلط ہیں۔ براہ کرم سسٹم ایڈمن سے رابطہ کریں۔"
        elif e.response.status_code == 429:
            return "سرور مصروف ہے۔ براہ کرم تھوڑی دیر بعد کوشش کریں۔"
        else:
            return "معذرت، سرور سے جواب حاصل کرنے میں مسئلہ پیش آیا۔ براہ کرم دوبارہ کوشش کریں۔"
            
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(f"ERROR: {error_msg}")
        return "معذرت، غیر متوقع مسئلہ پیش آیا۔ براہ کرم دوبارہ کوشش کریں۔"