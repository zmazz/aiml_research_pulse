import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
# simple chatbot using Hugging Face's GPT-2 model, potentially a good starting point for a more complex chatbot for pdfs or other documents

st.title("Dolly Chat App")

conversation_history = []

user_input = st.text_input("Your message:", key="user_input")

if st.button("Send"):
    conversation_history.append(f'User: {user_input}')

    # Concatenate conversation history
    instruction = ' '.join(conversation_history)

    input_ids = tokenizer.encode(instruction, return_tensors="pt")
    generated_output = model.generate(
        input_ids,
        max_length=len(instruction.split()) + 50,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        top_k=50,
        top_p=0.95,
        temperature=0.8,
    )
    dolly_response = tokenizer.decode(generated_output[0], skip_special_tokens=True)

    # Remove the user input from Dolly's response
    dolly_response = dolly_response[len(instruction):].strip()

    # Add Dolly's response to the conversation history
    conversation_history.append(f'Dolly: {dolly_response}')

# Display conversation history
for message in conversation_history:
    st.write(message)
