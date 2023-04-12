import streamlit as st
import torch

from transformers import AutoTokenizer, DALLEForConditionalGeneration

tokenizer = AutoTokenizer.from_pretrained("borisdayma/dalle-mini")
model = DALLEForConditionalGeneration.from_pretrained("borisdayma/dalle-mini")


def generate_images(prompt, max_length=32, temperature=0.7):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(torch.device("cuda:0" if torch.cuda.is_available() else "cpu"))
    output_ids = model.generate(input_ids, max_length=max_length, temperature=temperature)
    output_image = output_ids[0].cpu().detach().numpy()
    return output_image

st.title("DALL·E Mini Model Card")
prompt = st.text_input("Enter your text prompt:")
if prompt:
    output_image = generate_images(prompt)
    st.image(output_image, width=512)
