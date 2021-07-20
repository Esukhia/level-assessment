import html
import streamlit as st

from annotated_text import annotation
from botok import WordTokenizer
from htbuilder import H, HtmlElement

"""
# Word Level Assessment Tool For Tibetan Language


"""
div = H.div
wt = WordTokenizer()

level_dict = {
    'བཀྲ་ཤིས་': 'l2',
    'བདེ་ལེགས་': 'l3',
    'ང་': 'l1',
    'བོད་': 'l2',
    'ནས་': 'l1',
    'ཡིན་': 'l1',
    'སེམས་པ་':'l2',
    'ཐམས་ཅད་': 'l3'
}

level_code_lookup = {
    'l1': '#8ef',
    'l2': '#afa',
    'l3': '#faa'
}

def get_tokens(text):
    tokens = wt.tokenize(text, split_affixes=False)
    return tokens


def check_level(word):
    level = level_dict.get(word, '')
    level_code = ''
    if level:
        level_code = level_code_lookup.get(level, '')
    return level, level_code

    
def assess_level(input_text):
    tokens = get_tokens(input_text)
    level_annotated = []
    for token in tokens:
        token_text = token.text
        level, level_code = check_level(token_text)
        if level:
            level_annotated.append((token_text, level, level_code))
        else:
            level_annotated.append(token_text)
    return level_annotated

level_assessment = []
user_input = st.text_area("Enter text here", "")
level_assessment = assess_level(user_input)

if st.button('Assess Level'):
    out = div()

    for word in level_assessment:
        if isinstance(word, str):
            out(html.escape(word))

        elif isinstance(word, HtmlElement):
            out(word)

        elif isinstance(word, tuple):
            out(annotation(*word))

        else:
            raise Exception("Oh noes!")

    st.markdown(str(out), unsafe_allow_html=True)


# ང་བོད་ལ་འགྲོ་ནས་སླེད་པ་ཡིན་ སེམས་ཅན་ཐམས་ཅད་ལ་བཀྲ་ཤིས་བདེ་ལེགས་ཞུས་རྒྱུ་ཡིན་ སེམས་པ་སྐྱིད་པོ་འདུག།