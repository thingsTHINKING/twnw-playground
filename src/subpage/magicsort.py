import json
import ast
import os

import pandas as pd
import plotly.io as pio
import streamlit as st
from src.abstract_page import AbstractPage
from data.read_config import read_config

__config_path = os.path.join("magicsort", "config.toml")
CONFIG = read_config(__config_path)


class MagicSort(AbstractPage):
    def __init__(self):
        super().__init__("✨ Smart Cluster")
        self._use_cases = ast.literal_eval(CONFIG["use_cases"]["names"])
        self._tot_use_cases = ast.literal_eval(CONFIG["use_cases"]["topics_over_time"])

    def build(self):
        selected_case = st.selectbox(
            "Which use case would you like to see?", (self._use_cases.keys())
        )
        self._use_case = self._use_cases[selected_case]
        data = self._load_data()
        granularity = self._determine_granularity()
        _, col, _ = st.columns(3)
        self._sort_documents(data, granularity, col)

    def _sort_documents(self, data, granularity, col):
        if col.button("Sort documents ✨"):
            with st.spinner("Wait for it..."):
                self._show_sorted_documents(data, granularity)
            self._visualize_clustering(granularity)

    def _visualize_clustering(self, granularity):
        with st.expander("Visualization 📚"):
            st.write(
                """
                        The charts show the library documents and their similarity in 2D space.
                    """
            )
            if self._use_case in self._tot_use_cases:
                self._topic_over_time_visualization(granularity)
            else:
                tab1, tab2 = st.tabs(["All Documents", "Cluster"])

                with tab1:
                    doc_map = self._load_figure("doc_map", granularity)
                    st.plotly_chart(doc_map, use_container_width=True)

                with tab2:
                    cluster = self._load_figure("map", granularity)
                    st.plotly_chart(cluster, use_container_width=True)

    def _show_sorted_documents(self, data, granularity):
        st.success(f"Here are your document clusters!", icon="🦸🏼‍♀️")
        topics = pd.read_excel(
            f"data/magicsort/{self._use_case}/{granularity}/{granularity}_excel.xlsx"
        )
        st.write(topics[["Topic", "Name"]])
        col_selection = f"{granularity}_topics"
        sorted_library = data[[col_selection, "Name", "Content"]]
        sorted_library.columns = ["Topic", "Name", "Text"]
        st.write("Here is your sorted library:")
        st.write(sorted_library)

    def _determine_granularity(self):
        st.write(
            "A broad overview of the documents can be achieved by using a high granularity. A high granularity means that the documents are clustered into a few topics. A low granularity means that the documents are clustered into many topics."
        )
        option = st.selectbox(
            "How would you like your documents to be sorted?", ("Broad", "Detailed")
        )
        granularity = "broad" if option == "Broad" else "fine"
        return granularity

    def _load_data(self):
        st.markdown("### Library")
        temp_dict = dict((v, k) for k, v in self._use_cases.items())
        st.write(
            f"This is your library of documents, in this instance, the documents are descriptions of {temp_dict[self._use_case]}. You can use MagicSort to get an overview over the documents and to find trends."
        )
        data = pd.read_excel(f"data/magicsort/{self._use_case}/data.xlsx")
        library = data[["Name", "Content"]]
        library.columns = ["Name", "Text"]
        st.write(library)
        return data

    def _load_figure(self, type, granularity):
        with open(
            f"data/magicsort/{self._use_case}/{granularity}/{granularity}_{type}.json",
            "r",
        ) as f:
            data = json.loads(f.read())
            return pio.from_json(data)

    def _topic_over_time_visualization(self, granularity):
        doc_map_tab, cluster_map_tab, tot_map = st.tabs(
            ["All Documents", "Cluster", "Topics over Time"]
        )

        with doc_map_tab:
            doc_map = self._load_figure("doc_map", granularity)
            st.plotly_chart(doc_map, use_container_width=True)

        with cluster_map_tab:
            cluster = self._load_figure("map", granularity)
            st.plotly_chart(cluster, use_container_width=True)

        with tot_map:
            tot = self._load_figure("tot", granularity)
            st.plotly_chart(tot, use_container_width=True)
