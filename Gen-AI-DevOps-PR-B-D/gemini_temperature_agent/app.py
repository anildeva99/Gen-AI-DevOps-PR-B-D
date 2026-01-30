import streamlit as st
import google.generativeai as genai
import os

# --- API Key Setup ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("❌ No API key found. Please set GEMINI_API_KEY environment variable.")
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        st.error(f"⚠️ Gemini configuration failed: {str(e)}")
        model = None

# --- App Title ---
st.title("🌡️ Gemini Temperature Agent")
st.write("This agent only answers questions related to **AI temperature parameter** (LLM concept).")

# --- User Input ---
prompt = st.text_input("Ask about AI temperature parameter:")

if st.button("Send") and prompt:
    if not model:
        st.error("❌ Gemini model is not configured. Check your API key.")
    else:
        if "temperature" not in prompt.lower():
            st.markdown("⚠️ Sorry, I only handle queries related to the *AI temperature parameter*.")
        else:
            system_instruction = (
                "You are an expert AI assistant. Only answer questions "
                "about the 'temperature' parameter used in LLMs. "
                "Do not answer weather-related queries."
            )
            try:
                response = model.generate_content(system_instruction + "\n\nUser: " + prompt)
                st.markdown(f"**🤖 Temperature Agent:** {response.text}")
            except Exception as e:
                st.error(f"⚠️ Gemini API error: {str(e)}")

