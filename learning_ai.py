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
                              system_instruction=f"""请用{language}语言来回答所有问题。
                              完成以下任务：
 1. 语法与拼写检查：
     - 分析用户输入的文本，并标记所有语法、拼写和标点错误。
     - 尝试纠正这些错误，并提供修改后的文本。
     - 为文本的语法和拼写质量评分，评分范围为 0 到 10 分。
 2. 结构和逻辑建议：
     - 分析用户输入的文本的结构和逻辑流。
     - 提供建议以帮助用户改善段落结构和逻辑流，让写作更连贯。
     - 为文本的结构和逻辑质量评分，评分范围为 0 到 10 分。
     提供优化和修改后的完整文本：""",
                              )



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
                "content": "Hello! I'm here to enhance your writing with grammar, spelling, and structure tips. Ask me anything!"
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
        
        
        # 将所有历史信息拼接起来
        full_query = "\n".join([message["content"] for message in st.session_state.messages])
        full_query += f"\n{query}"
        llm_function(full_query)

        # llm_function(query)

        

if __name__ == "__main__":
    main()
