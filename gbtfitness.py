import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Initialize your chatbot model
template = """
Answer the question below.

Here is the conversation history: {history}

Question: {question}

Answer: 
"""
model = OllamaLLM(model="llama3.2")  # Make sure you are using the correct model name
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Set up the Streamlit interface
def chat_with_bot():
    st.title("Fitness & Well-being Chatbot")
    st.write("Ask me anything! Type 'exit' to quit.")
    
    # Initialize conversation history (this will keep track of the conversation)
    history = ""

    # Text input box for the user to type their message
    user_input = st.text_input("You: ", "")

    # If the user provides input
    if user_input:
        if user_input.lower() == "exit":
            st.write("Goodbye!")
        else:
            # Get chatbot response by passing the input and conversation history
            result = chain.invoke({"history": history, "question": user_input})
            st.write(f"Bot: {result}")
            # Update the conversation history
            history += f"\nUser: {user_input}\nBot: {result}"

if __name__ == "__main__":
    chat_with_bot()
