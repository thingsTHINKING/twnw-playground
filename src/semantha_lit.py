import streamlit as st
from PIL import Image

from abstract_page import AbstractPage
from subpage.semantic_compare import SemanticCompare
from subpage.semantic_search import SemanticSearch
from subpage.smart_cluster import SmartCluster


class SemanthaLit(AbstractPage):
    def __init__(self):
        super().__init__("playground")
        self.__page_config()

    def build(self):
        self.page_description()
        pages = [SemanticCompare(), SemanticSearch(), SmartCluster()]
        tabs = st.tabs([t.name() for t in pages])
        for i in range(len(pages)):
            with tabs[i]:
                pages[i].build()

    def page_description(self):
        image = Image.open("data/Semantha-PLAYGROUND_positiv-RGB.png")
        st.image(image, use_column_width="always")
        st.markdown(
            "This is an interactive application to demonstrate some of semantha®'s capabilities. Feel free to play "
            "around and have some fun. But don't fall off the swing."
        )

    @staticmethod
    def __page_config():
        st.set_page_config(
            page_title="🦸🏼‍♀️ semantha® playground",
            page_icon="data/favicon.png",
            layout="centered",
        )


if __name__ == "__main__":
    sl = SemanthaLit()
    sl.build()
