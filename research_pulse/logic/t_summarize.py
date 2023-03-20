import numpy as np
import pandas as pd
from transformers import BartForConditionalGeneration, BartTokenizer, BartConfig
import torch
import json
import sentencepiece as spm
import research_pulse.logic.data_loader as dl
import os
import sys

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

def load_bart_model():
    # #Code BartConfig
    bart_config = BartConfig.from_pretrained('facebook/bart-large-cnn', output_hidden_states=True)
    # #Code BARTConfig and set vocab size to 50265
    bart_config.vocab_size = 50265
    bart_tokenizer=BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    bart_model=BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

    # bart_tokenizer= BartTokenizer.from_pretrained('/Users/ziadmazzawi/deepdipper/training_outputs/bart_tokenizer')
    # bart_model = BartForConditionalGeneration.from_pretrained('/Users/ziadmazzawi/deepdipper/training_outputs/bart_model')
    # bart_config = BartConfig.from_pretrained('/Users/ziadmazzawi/deepdipper/training_outputs/bart_config')


    # bart_tokenizer= BartTokenizer.from_pretrained(os.path.join(sys.path[0], 'bart_tokenizer'))
    # bart_model = BartForConditionalGeneration.from_pretrained(os.path.join(sys.path[0], 'bart_model'))
    # bart_config = BartConfig.from_pretrained(os.path.join(sys.path[0], "bart_config"))


    # from gcsfs import GCSFileSystem
    # gcs = GCSFileSystem(token=None)
    # path_tokenizer = 'gs://deepdipper_data/training_outputs/bart_tokenizer'
    # bart_tokenizer = BartTokenizer.from_pretrained(path_tokenizer, fs=gcs)
    # path_model = 'gs://deepdipper_data/training_outputs/bart_model'
    # bart_model=BartForConditionalGeneration.from_pretrained(path_model, fs=gcs)
    # path_config='gs://deepdipper_data/training_outputs/bart_config'
    # bart_config = BartConfig.from_pretrained(path_config, fs=gcs)
#

    # import gcsfs

    # fs = gcsfs.GCSFileSystem(project='deepdipper')
    # with fs.open('deepdipper_data/training_outputs/bart_model/config.json', 'rb') as f:
    #     config = json.load(f)
    # with fs.open('deepdipper_data/training_outputs/bart_model/pytorch_model.bin', 'rb') as f:
    #     model_state_dict = torch.load(f)
    # bart_model = BartForConditionalGeneration.from_pretrained(pretrained_model_name_or_path=None,
    #                                                         config=config,
    #                                                         state_dict=model_state_dict)

    # with fs.open('deepdipper_data/training_outputs/bart_tokenizer/tokenizer_config.json', 'rb') as f:
    #     tokenizer_config = json.load(f)
    # with fs.open('deepdipper_data/training_outputs/bart_tokenizer/vocab.json', 'r') as f:
    #     vocab = json.load(f)
    # with fs.open('deepdipper_data/training_outputs/bart_tokenizer/source.spm', 'rb') as f:
    #     source_model = f.read()
    # with fs.open('deepdipper_data/training_outputs/bart_tokenizer/special_tokens_map.json', 'r') as f:
    #     special_tokens_map = json.load(f)

    # source_spm = spm.SentencePieceProcessor()
    # source_spm.LoadFromSerializedProto(source_model)

    # bart_tokenizer = BartTokenizer.from_pretrained(pretrained_model_name_or_path=None,
    #                                         tokenizer_file=None,
    #                                         tokenizer_config=tokenizer_config,
    #                                         vocab_files={'input_ids': vocab, 'attention_mask': vocab, 'decoder_input_ids': vocab, 'decoder_attention_mask': vocab},
    #                                         merges_file=None,
    #                                         add_prefix_space=False,
    #                                         source_vocab=source_spm,
    #                                         target_vocab=None,
    #                                         special_tokens_map=special_tokens_map)

    return bart_tokenizer,bart_model,bart_config

#Use pretrained model and tonekizer to produce summary tokens and then decode thise summarized tokens
def summarizer(query_id, df, bart_tokenizer, bart_model,bart_config):

    bart_config.vocab_size = 50265

    text=df.loc[df['id']==query_id]['abstract'].values[0]
    input_ids = bart_tokenizer.encode(text, return_tensors='pt')

    # Generate a 2-3 sentence summary
    summary_ids = bart_model.generate(input_ids, num_beams=4, max_length=120, early_stopping=True)
    summary = bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)

    # summary_ids = bart_model.generate(inputs['input_ids'], early_stopping=True)
    # bart_summary = bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True, max_length=130, min_length=30)
    return {'original': text,
            'summary': summary}

if __name__ =='__main__':
    data,cit=dl.load_data()
    bart_tokenizer,bart_model,bart_config = load_bart_model()
    summarizer(query_id=input('Enter your query: '), df=data, bart_tokenizer=bart_tokenizer, bart_model=bart_model,bart_config=bart_config)
