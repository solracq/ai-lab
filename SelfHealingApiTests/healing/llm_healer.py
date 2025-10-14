import os
import json
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_failure_with_llm(endpoint, response_test, error_message):
    """
    Use LLM (GPT-5) to explain and propose fixes for test failures
    :param endpoint: service endpoint
    :param response_test: response of test
    :param error_message: error message
    :return: suggested fix
    """
    prompt = f"""
    The REST API test for endpoint '{endpoint}' failed with error:
    {error_message}
    
    Response body:
    {response_test[:800]}
    
    Analyze what likely changed in the API and suggested how the test should adapt.
    Return JSON with keys: "explanation" and "suggested_fix". 
    """
    response = openai.ChatCompletion.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}]
    )

    msg = response.choices[0].message["content"]
    try:
        return json.loads(msg)
    except json.JSONDecodeError:
        return {"explanation": msg, "suggested_fix": None}


