import numpy as np
import pandas as pd
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
    # #Code BartConfig
    # config = BartConfig.from_pretrained('facebook/bart-large-cnn', output_hidden_states=True)
    # # #Code BARTConfig and set vocab size to 50265
    # config.vocab_size = 50265
    # bart_tokenizer=BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    # bart_model=BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

    # bart_tokenizer= BartTokenizer.from_pretrained('/Users/ziadmazzawi/deepdipper/training_outputs/bart_tokenizer')
    # bart_model = BartForConditionalGeneration.from_pretrained('/Users/ziadmazzawi/deepdipper/training_outputs/bart_model')
    # bart_config = BartConfig.from_pretrained('/Users/ziadmazzawi/deepdipper/training_outputs/bart_config')

    import gcsfs
    fs = gcsfs.GCSFileSystem(project='deepdipper')
    with fs.open('deepdipper_data/training_outputs/bart_tokenizer') as g:
        bart_tokenizer = BartTokenizer.from_pretrained(g)
    with fs.open('deepdipper_data/training_outputs/bart_model') as f:
        bart_model = BartForConditionalGeneration.from_pretrained(f)
    with fs.open('deepdipper_data/training_outputs/bart_config') as h:
        bart_config = BartConfig.from_pretrained(h)

    return bart_tokenizer,bart_model,bart_config

#Use pretrained model and tonekizer to produce summary tokens and then decode thise summarized tokens
def summarizer(query_id, df, bart_tokenizer, bart_model,bart_config):

    bart_config.vocab_size = 50265

    text=df.loc[df['id']==query_id]['abstract'].values[0]
    input_ids = bart_tokenizer.encode(text, return_tensors='pt')

    # Generate a 2-sentence summary
    summary_ids = bart_model.generate(input_ids, num_beams=4, max_length=120, early_stopping=True)
    summary = bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)

    # Print the summary
    print(summary)

    # summary_ids = bart_model.generate(inputs['input_ids'], early_stopping=True)
    # bart_summary = bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True, max_length=130, min_length=30)
    return {'original': text,
            'summary': summary}
