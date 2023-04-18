import streamlit as st
from abstract_page import SemanthaBasePage


class OMD(SemanthaBasePage):
    def __init__(self):
        super().__init__("🦸🏼‍♀️ Opposite Meaning Detection")
        self.__compare_domain = "PG_Compare"

    def build(self):
        st.markdown("## Opposite Meaning Detection")
        st.write(
            "Directly compare two texts by entering them below. The texts will be compared using semantha's® opposite meaning model. The model will return if the two sentences share the same meaning and will recognize negations and contradictions."
        )
        input_0 = st.text_input(label="Input I", value="I hate you.")
        input_1 = st.text_input(label="Input II", value="I love you.")
        _, col, _ = st.columns([1, 1, 1])
        if col.button("⇆ Opposite Meaning Detection", key="omdbutton"):
            with st.spinner('Wait for it...'):
                self.compute_and_display_omd(input_0, input_1)

    def compute_and_display_omd(self, input_0: str, input_1: str):
        omd = self._semantha_connector.get_opposite_meaning(
            input_0, input_1, self.__compare_domain
        )
        if omd:
            st.error(f"🦸🏼‍♀️ The texts are of opposite meaning.")
        else:
            st.success(f"🦸🏼‍♀️ The texts are of the same meaning.")
