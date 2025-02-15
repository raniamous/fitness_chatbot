import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import httpx

# Initialize the LLM and the prompt template
template = """
Answer the question below.

Here is the conversation history: {history}

Question: {question}

Answer: 
"""
model = OllamaLLM(model="llama3.2")  # Use the correct model name
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Set up the Streamlit interface
def chat_with_bot():
    st.title("Fitness & Well-being Chatbot")
    st.write("Ask me anything! Type 'exit' to quit.")
    
    # Initialize conversation history (this will keep track of the conversation)
    if 'history' not in st.session_state:
        st.session_state.history = ""

    # Text input box for the user to type their message
    user_input = st.text_input("You: ", "")

    # If the user provides input
    if user_input:
        if user_input.lower() == "exit":
            st.write("Goodbye!")
        else:
            # Get chatbot response by passing the input and conversation history
            result = chain.invoke({"history": st.session_state.history, "question": user_input})

            # If result is returned as a dictionary, ensure the answer is extracted properly
            answer = result.get('answer', '') if isinstance(result, dict) else str(result)
            
            st.write(f"Bot: {answer}")

            # Update the conversation history
            st.session_state.history += f"\nUser: {user_input}\nBot: {answer}"

# Function to fetch data from an API (optional)
def get_data_from_api(url):
    try:
        # Create a client with a timeout of 60 seconds
        with httpx.Client(timeout=60.0) as client:
            response = client.get(url)
            response.raise_for_status()  # Raises an error for bad responses (4xx or 5xx)
            return response.json()  # Assuming the response is in JSON format
    except httpx.RequestError as exc:
        st.error(f"An error occurred while requesting {exc.request.url}: {exc}")
    except httpx.HTTPStatusError as exc:
        st.error(f"HTTP error occurred: {exc.response.status_code}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Function to handle the API request (if you want to test an external URL)
def api_example_request():
    url = "https://api.example.com/data"  # Example URL, replace with your real API
    response = get_data_from_api(url)
    if response:
        st.write(response)

# Call the chat function
if __name__ == "__main__":
    chat_with_bot()  # Start the chatbot
