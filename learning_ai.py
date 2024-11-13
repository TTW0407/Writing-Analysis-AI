import google.generativeai as genai
import os
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

# Title
st.title("📑 Writing Analysis AI")

#Language Select
language = st.selectbox("Select Response Language🌐", ["English", "Chinese", "Malay"])

#Temperature
temperature = st.slider("Creative Range💡", min_value=0.1, max_value=2.0, value=1.0, step=0.1)



# Config API Key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])



#Create Model
model = genai.GenerativeModel("gemini-1.5-flash",
    system_instruction=f"""Please communicate with users in {language}.

    Task guidelines:
    1. Determine the user's intent based on their input:
       - If the input is a greeting, simple question, or does not require analysis, respond in a friendly and concise manner.
       - If the input appears to be a text for analysis, proceed with a structured response as described below.

    Main tasks when analyzing text:
    1. **Grammar and Spelling Check**:
       - Identify grammatical, spelling, and punctuation errors.
       - Provide a corrected version of the text and rate the grammar/spelling quality (0-10 scale).

    2. **Structure and Logic Suggestions**:
       - Evaluate the text's structure and logical flow.
       - Suggest improvements for paragraph structure and flow, and rate structure/logic quality (0-10 scale).

    3. **Final Optimized Text**:
       - Provide the fully optimized and revised text, preserving the original tone and style for comparison.

    Always begin responses by briefly introducing yourself and your capabilities, especially if the user hasn't yet provided text for analysis."""
)


# page_bg_img = f"""
# <style>
# [data-testid="stAppViewContainer"] > .main {{
# background-image: url("https://i.postimg.cc/d34QXdDD/application-pc-and-smartphone-with-business-vector-29570430.jpg");
# background-size: cover;
# background-position: center center;
# background-repeat: no-repeat;
# background-attachment: local;
# }}
# [data-testid="stHeader"] {{
# background: rgba(0,0,0,0);
# }}
# </style>
# """

# st.markdown(page_bg_img, unsafe_allow_html=True)

def main():
    

    # Content Generate
    def generate_content(query, temperature, language):
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=8192,
            top_p=0.95,
            top_k=40,
        )
        
        response = model.generate_content(
            query,
            generation_config=generation_config
        )
        
        return response.text if hasattr(response, 'text') else "No response generated."



    # Initialize History
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "**Hello!** I'm here to **Enhance** your **Writing** with:\n- **Grammar Tips**\n- **Spelling Tips**\n- **Structure Tips**\n\nAsk me anything!"
            }
        ]



    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])



    # Process and store Query and Response
    def llm_function(query):
        response = generate_content(query, temperature, language)

        
        # Displaying the Assistant Message
        with st.chat_message("assistant"):
            st.markdown(response)


        # Storing the User Message
        st.session_state.messages.append(
            {
                "role":"user",
                "content": query
            }
        )


        # Storing the Assistant Message
        st.session_state.messages.append(
            {
                "role":"assistant",
                "content": response
            }
        )

    


    # User Input
    query = st.chat_input("How may I help you?")
     


    # Process User Input
    # Calling the Function when Input is Provided
    if query:
        # Displaying the User Message
        with st.chat_message("user"):
            st.markdown(query)
        
        
        # Stitching Historical Information
        full_query = "\n".join([message["content"] for message in st.session_state.messages])
        full_query += f"\n{query}"
        llm_function(full_query)

        # llm_function(query)

        

if __name__ == "__main__":
    main()
