from transformers import MarianMTModel, MarianTokenizer
import json
import torch

def chunk_paragraph(paragraph):
    sub_paragraphs = []
    current_sub_paragraph = ""
    for sentence in paragraph.split(". "):
        sentence += ". "
        if len(current_sub_paragraph) + len(sentence) <= 500:
            current_sub_paragraph += sentence
        else:
            sub_paragraphs.append(current_sub_paragraph)
            current_sub_paragraph = sentence
    if current_sub_paragraph:
        sub_paragraphs.append(current_sub_paragraph)
    return sub_paragraphs

def marian_model():
    """
    Import MarianMTModel and MarianTokenizer
    """
    model_name = "Helsinki-NLP/opus-mt-en-roa"
    marian_tokenizer = MarianTokenizer.from_pretrained(model_name)
    marian_model = MarianMTModel.from_pretrained(model_name)


    # marian_model = MarianMTModel.from_pretrained("/Users/ziadmazzawi/deepdipper/training_outputs/marian_model")
    # marian_tokenizer = MarianTokenizer.from_pretrained("/Users/ziadmazzawi/deepdipper/training_outputs/marian_tokenizer")


    # from gcsfs import GCSFileSystem
    # gcs = GCSFileSystem(token=None)
    # path_tokenizer = 'gs://deepdipper_data/training_outputs/marian_tokenizer'
    # marian_tokenizer = MarianTokenizer.from_pretrained(path_tokenizer, fs=gcs)
    # path_model = 'gs://deepdipper_data/training_outputs/marian_model'
    # marian_model = MarianMTModel.from_pretrained(path_model, fs=gcs)


    # import gcsfs
    # fs = gcsfs.GCSFileSystem(project='deepdipper')

    # # Load tokenizer
    # with fs.open('deepdipper_data/training_outputs/marian_tokenizer/tokenizer_config.json', 'r') as f:
    #     tokenizer_config = f.read()
    # with fs.open('deepdipper_data/training_outputs/marian_tokenizer/vocab.json', 'r') as f:
    #     vocab = f.read()
    # with fs.open('deepdipper_data/training_outputs/marian_tokenizer/source.spm', 'rb') as f:
    #     source_model = f.read()
    # with fs.open('deepdipper_data/training_outputs/marian_tokenizer/target.spm', 'rb') as f:
    #     target_model = f.read()
    # with fs.open('deepdipper_data/training_outputs/marian_tokenizer/special_tokens_map.json', 'r') as f:
    #     special_tokens_map = json.load(f)

    # tokenizer = MarianTokenizer.from_pretrained(pretrained_model_name_or_path=None,
    #                                             tokenizer_file=None,
    #                                             tokenizer_config=tokenizer_config,
    #                                             vocab_files={'source': vocab, 'target': vocab},
    #                                             source_vocab=None,
    #                                             target_vocab=None,
    #                                             special_tokens_map=special_tokens_map)

    # tokenizer.source_spm.LoadFromSerializedProto(source_model)
    # tokenizer.target_spm.LoadFromSerializedProto(target_model)

    # # Load model
    # with fs.open('deepdipper_data/training_outputs/marian_model/config.json', 'r') as f:
    #     config = f.read()
    # with fs.open('deepdipper_data/training_outputs/marian_model/pytorch_model.bin', 'rb') as f:
    #     model_state_dict = torch.load(f)

    # model = MarianMTModel.from_pretrained(pretrained_model_name_or_path=None,
    #                                     config=config,
    #                                     state_dict=model_state_dict,
    #                                     tokenizer=tokenizer)

    # # Set model and tokenizer to device
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # model.to(device)
    # tokenizer.model_max_length = model.config.max_length

    # marian_tokenizer=tokenizer
    # marian_model=model
    return marian_tokenizer, marian_model

def translate_fra(query_id,df,tokenizer, model):
    text='TITLE: ' + df.loc[df['id']==query_id]['title'].values[0] + ' \n -- AUTHORS:' + df.loc[df['id']==query_id]['authors'].values[0] + ' \n -- ABSTRACT:' + df.loc[df['id']==query_id]['abstract'].values[0]
    sub_texts=chunk_paragraph(text)
    sub_texts_translated=[]
    for sub_text in sub_texts:
        src_text= ">>fra<< " + sub_text
        translated = model.generate(**tokenizer(src_text, return_tensors="pt", padding=True))
        sub_texts_translated.append([tokenizer.decode(t, skip_special_tokens=True) for t in translated][0])
    translation=' '.join(sub_texts_translated)
    return {'original_text': text,
            'translated_text': translation }

def translate_esp(query_id,df,tokenizer, model):
    text='TITLE: ' + df.loc[df['id']==query_id]['title'].values[0] + ' \n -- AUTHORS:' + df.loc[df['id']==query_id]['authors'].values[0] + ' \n -- ABSTRACT:' + df.loc[df['id']==query_id]['abstract'].values[0]
    sub_texts=chunk_paragraph(text)
    sub_texts_translated=[]
    for sub_text in sub_texts:
        src_text= ">>esp<< " + sub_text
        translated = model.generate(**tokenizer(src_text, return_tensors="pt", padding=True))
        sub_texts_translated.append([tokenizer.decode(t, skip_special_tokens=True) for t in translated][0])
    translation=' '.join(sub_texts_translated)
    return {'original_text': text,
            'translated_text': translation }

def translate_por(query_id,df,tokenizer, model):
    text='TITLE: ' + df.loc[df['id']==query_id]['title'].values[0] + ' \n -- AUTHORS:' + df.loc[df['id']==query_id]['authors'].values[0] + ' \n -- ABSTRACT:' + df.loc[df['id']==query_id]['abstract'].values[0]
    sub_texts=chunk_paragraph(text)
    sub_texts_translated=[]
    for sub_text in sub_texts:
        src_text= ">>por<< " + sub_text
        translated = model.generate(**tokenizer(src_text, return_tensors="pt", padding=True))
        sub_texts_translated.append([tokenizer.decode(t, skip_special_tokens=True) for t in translated][0])
    translation=' '.join(sub_texts_translated)
    return {'original_text': text,
            'translated_text': translation }
