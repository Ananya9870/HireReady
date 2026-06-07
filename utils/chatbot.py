import streamlit as st
from groq import Groq

def get_chatbot_response(messages, resume_text, job_description):
    """
    Handles conversational memory by passing the entire message history.
    """
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    # Latest high-reasoning model
    MODEL = "llama-3.3-70b-versatile" 
    
    # System Instruction: Context fix karne ke liye
    system_prompt = {
        "role": "system",
        "content": f"""You are an Expert Interview Coach. 
        Context provided:
        Resume: {resume_text[:2000]}
        Job Description: {job_description[:2000]}
        
        Instructions:
        - Maintain conversation context.
        - provide specific questions/answers based on the context.
        - Keep the flow natural. If user asks follow-up, answer based on previous messages."""
    }
    
    full_messages = [system_prompt] + messages
    
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=full_messages,
            temperature=0.7,
            max_tokens=1500
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Coach is temporarily unavailable: {str(e)}"