import streamlit as st
from PIL import Image

from abstract_page import AbstractPage
from subpage.semantic_compare import SemanticCompare
from subpage.semantic_search_semantha import SemanticSearchSemantha
from subpage.magicsort import MagicSort


class SemanthaLit(AbstractPage):
    def __init__(self):
        super().__init__("playground")
        st.set_page_config(
            page_title="🦸🏼‍♀️ playground",
            page_icon="data/favicon.png",
            layout="centered",
        )
        image = Image.open("data/Semantha-PLAYGROUND_positiv-RGB.png")
        st.image(image, use_column_width="always")
        st.markdown(
            "This is an interactive application to demonstrate some of semantha®'s capabilities. Feel free to play around and have some fun. But don't fall off the swing."
        )

    def build(self):
        tabs = [SemanticCompare(), SemanticSearchSemantha(), MagicSort()]
        html_tabs = st.tabs([t.name() for t in tabs])
        for i in range(len(tabs)):
            with html_tabs[i]:
                tabs[i].build()


if __name__ == "__main__":
    sl = SemanthaLit()
    sl.build()
