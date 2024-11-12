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
                              system_instruction=f"""Please communicate with users in {language}, 
                                
                              Complete the following tasks:
 1. Grammar and spelling check:
     - Analyze the user input text and identify all grammatical, spelling, and punctuation errors.
     - Try to correct these errors and provide the revised text.
     - Rate the grammar and spelling quality of the text on a scale of 0 to 10.
 2. Structure and logic suggestions:
     - Analyze the structure and logical flow of the user input text.
     - Provide suggestions to help the user improve the paragraph structure and logical flow to make writing more coherent.
     - Rate the structure and logic quality of the text on a scale of 0 to 10.
 3. Final text:
    - Provide the fully optimized and revised text in a new paragraph, preserving the tone and style of the original for comparison.""",
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
