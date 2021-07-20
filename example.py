import streamlit as st
from annotated_text import annotation
import html

from htbuilder import H, HtmlElement, styles
from htbuilder.units import unit

# Only works in 3.7+: from htbuilder import div, span
div = H.div

"""
# Annotated text example

Below is an example of how to use the annotated_text function:
"""
level_dict = {
    'hi': 'level1',
    'together': 'level3',
    'love': 'level2',
    'I': 'level1',
    'you': 'level1',
    'lets':'level2',
    'live': 'level3'
}

level_code_lookup = {
    'level1': '#8ef',
    'level2': '#faa',
    'level3': '#afa'
}

def check_level(word):
    level = level_dict.get(word, '')
    level_code = ''
    if level:
        level_code = level_code_lookup.get(level, '')
    return level, level_code

    
def assess_level(text):
    level_annotated = []
    words = text.split(' ')
    for word in words:
        level, level_code = check_level(word)
        level_annotated.append((f'{word} ', level, level_code))
    return level_annotated

user_input = st.text_area("Enter text here", "")

level_assesement = []
level_assesement = assess_level(user_input)

if st.button('Assess Level'):
    out = div()

    for word in level_assesement:
        if isinstance(word, str):
            out(html.escape(word))

        elif isinstance(word, HtmlElement):
            out(word)

        elif isinstance(word, tuple):
            out(annotation(*word))

        else:
            raise Exception("Oh noes!")

    st.markdown(str(out), unsafe_allow_html=True)