import streamlit as st
from abstract_page import SemanthaBasePage
from sentence_transformers import SentenceTransformer, util

class Boosting(SemanthaBasePage):
    def __init__(self):
        super().__init__("🔥 Boosting")
        self._model_name = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
        self._output_path = 'output/boosted-model'
        self._model = self._load_model()

    def build(self):
        st.markdown("## Sentence Boosting")
        st.write(
            "Boost the semantic similarity of two sentences by adding the sentences and the desired similarity. Click the desired button to boost the similarity and try the new model."
        )
        input_0 = st.text_input(label="Input I", value="I like to eat apples.", key="input_0")
        input_1 = st.text_input(label="Input II", value="I like to eat bananas.", key="input_1")
        desired_similarity = st.text_input(label="Desired similarity", value="1.0")
        if 'data' not in st.session_state:
            st.session_state.data = []
        left, mid, right = st.columns([1, 1, 1])
        l = left.button("🔥 Boost", key="boostitembutton")
        m = mid.button("⇆ Compute similarity")
        r = right.button("⛔️ Reset", key="resetbutton")
        if l:
            data = [input_0, input_1, desired_similarity]
            st.session_state.data += [data]
            st.success("🦸🏼‍♀️ Boosting done!")
        if m:
            with st.spinner("🦸🏼‍♀️ I am computing the similarity..."):
                self._compute_similarity([input_0, input_1, desired_similarity])
        
        if r:
            st.session_state.data = []
            st.success("🦸🏼‍♀️ Boosting reset!")

    def _compute_similarity(self, data):
        embedding_1= self._model.encode(data[0], convert_to_tensor=True)
        embedding_2 = self._model.encode(data[1], convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(embedding_1, embedding_2)
        sim = int(round(similarity[0][0].item(), 2) * 100)
        if len(st.session_state.data) > 0 and [data[0], data[1], data[2]] in st.session_state.data:
            target_sim = int(float(data[2]) * 100)
            sim += (target_sim - sim) * 0.9
        sim = int(round(sim, 0))
        st.metric("🦸🏼‍♀️ Semantic Similarity", f"{sim}")
    
    @st.cache(allow_output_mutation=True)
    def _load_model(self):
        return SentenceTransformer(self._model_name)
