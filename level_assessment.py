import html
import streamlit as st

from annotated_text import annotation
from botok import WordTokenizer
from htbuilder import H, HtmlElement

st.set_page_config(layout='wide')
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

pos_ann = {
    'VERB': '#8ef',
    'NOUN': '#afa',
    'PART': '#faa'
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

    
def annotate_level(tokens):
    level_annotations = []
    for token in tokens:
        token_text = token.text
        level, level_code = check_level(token_text)
        if level:
            level_annotations.append((token_text, level, level_code))
        else:
            level_annotations.append(token_text)
    return level_annotations

def annotate_segmentations(tokens):
    segmentation_annotations = []
    for token in tokens:
        token_text = token.text
        segmentation_annotations.append((token_text, '', '#FFF'))
    return segmentation_annotations

def annotate_pos(tokens):
    pos_annotations = []
    for token in tokens:
        token_text = token.text
        token_pos = token.pos
        token_ann = pos_ann.get(token_pos, '')
        if token_ann:
            pos_annotations.append((token_text, token_pos, token_ann))
        else:
            pos_annotations.append(token_text)
    return pos_annotations

def get_annotated_text(annotated_tokens):
    out = div()
    for word in annotated_tokens:
        if isinstance(word, str):
            out(html.escape(word))

        elif isinstance(word, HtmlElement):
            out(word)

        elif isinstance(word, tuple):
            out(annotation(*word))

        else:
            raise Exception("Oh noes!")

    st.markdown(str(out), unsafe_allow_html=True)

level_annotations = []
segmentation_annotations = []
pos_annotations = []
user_input = st.text_area("Enter text here", "")
tokens = get_tokens(user_input)
level_annotations = annotate_level(tokens)
segmentation_annotations = annotate_segmentations(tokens)
pos_annotations = annotate_pos(tokens)


col1, col2, col3 = st.beta_columns(3)
with col1:
    assess_level_flag = st.button('Assess Level')
with col2:
    seg_flag = st.button('Get Segmentation')
with col3:
    pos_flag = st.button('Get PosTag')

if assess_level_flag:
    get_annotated_text(annotated_tokens=level_annotations)

if seg_flag:
    get_annotated_text(annotated_tokens=segmentation_annotations)

if pos_flag:
    get_annotated_text(annotated_tokens=pos_annotations)

# ང་བོད་ལ་འགྲོ་ནས་སླེད་པ་ཡིན་ སེམས་ཅན་ཐམས་ཅད་ལ་བཀྲ་ཤིས་བདེ་ལེགས་ཞུས་རྒྱུ་ཡིན་ སེམས་པ་སྐྱིད་པོ་འདུག།