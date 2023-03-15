import pickle
from transformers import MarianMTModel, MarianTokenizer


def marian_model():
    """
    Import MarianMTModel and MarianTokenizer
    """
    model_name = "Helsinki-NLP/opus-mt-en-roa"
    marian_tokenizer = MarianTokenizer.from_pretrained(model_name)
    marian_model = MarianMTModel.from_pretrained(model_name)

    return marian_tokenizer, marian_model


def translate_fr(query_id,df,tokenizer, model):
    text='Title: ' + df.loc[df['id']==query_id]['title'].values[0] + ' -- Abstract:' + df.loc[df['id']==query_id]['abstract'].values[0]
    src_text= ">>fra<< " + text
    translated = model.generate(**tokenizer(src_text, return_tensors="pt", padding=True))
    return {'original text': text,
            'translated text': [tokenizer.decode(t, skip_special_tokens=True) for t in translated][0] }
