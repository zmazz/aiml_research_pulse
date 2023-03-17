import numpy as np
import pandas as pd
import streamlit as st
from transformers import BartForConditionalGeneration, BartTokenizer, BartConfig

# def chunk_paragraph(paragraph):
#     sub_paragraphs = []
#     current_sub_paragraph = ""
#     for sentence in paragraph.split(". "):
#         sentence += ". "
#         if len(current_sub_paragraph) + len(sentence) <= 500:
#             current_sub_paragraph += sentence
#         else:
#             sub_paragraphs.append(current_sub_paragraph)
#             current_sub_paragraph = sentence
#     if current_sub_paragraph:
#         sub_paragraphs.append(current_sub_paragraph)
#     return sub_paragraphs

# Loading the model and tokenizer for bart-large-cnn
def bart_model():
    #Code BartConfig
    config = BartConfig.from_pretrained('facebook/bart-large-cnn', output_hidden_states=True)
    #Code BARTConfig and set vocab size to 50265
    config.vocab_size = 50265
    bart_tokenizer=BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    bart_model=BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    return bart_tokenizer,bart_model

#Use pretrained model and tonekizer to produce summary tokens and then decode thise summarized tokens
def summarizer(query_id, df, bart_tokenizer, bart_model):
    text=df.loc[df['id']==query_id]['abstract'].values[0]
    inputs = bart_tokenizer.batch_encode_plus(text,return_tensors='pt')
    summary_ids = bart_model.generate(inputs['input_ids'], early_stopping=True)
    bart_summary = bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True, max_length=130, min_length=30, do_sample=False)
    return {'original_text': text,
            'summarized_text': bart_summary[0] }
