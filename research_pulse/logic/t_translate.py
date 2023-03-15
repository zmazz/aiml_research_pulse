import pickle
from transformers import MarianMTModel, MarianTokenizer

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
