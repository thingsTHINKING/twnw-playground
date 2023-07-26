import io
import logging

import semantha_sdk
from semantha_sdk.model.document import Document
from semantha_sdk.model.settings import Settings

import streamlit as st


def _to_text_file(text: str):
    input_file = io.BytesIO(text.encode("utf-8"))
    input_file.name = "input.txt"
    return input_file


class SemanthaConnector:
    def __init__(
        self,
        server_base_url="http://localhost/tt-platform-server",
        api_key=None,
    ):
        self.__sdk = semantha_sdk.login(server_url=server_base_url, key=api_key)

    @st.cache_data(show_spinner=False, persist="disk")
    def query_library(
        __self, text: str, domain: str, threshold=0.75, max_references=10, tags=None
    ):
        logging.info(f"Executing library search. Query string: '{text}'")
        doc = __self.__sdk.domains(domain).references.post(
            file=_to_text_file(text),
            similaritythreshold=threshold,
            maxreferences=max_references,
            tags=None if tags is None else ",".join(tags),
        )
        result_dict = {}
        if doc.references:
            for ref in doc.references:
                result_dict[ref.document_id] = {
                    "doc_name": __self.__get_ref_doc_name(ref.document_id, domain),
                    "content": __self.__get_document_content(ref.document_id, domain),
                    "similarity": ref.similarity,
                }
        return result_dict

    @st.cache_data(show_spinner=False, persist="disk")
    def get_library(__self, domain: str, tags=None, **kwargs):
        limit = kwargs.get("limit", None)
        logging.info(f"Fetching library documents with limit: {limit}")
        if limit is None:
            offset = None
        else:
            offset = kwargs.get("offset", 0)
        ref_doc_coll = __self.__sdk.domains(domain).referencedocuments.get(
            tags=None if tags is None else ",".join(tags), offset=offset, limit=limit
        )
        library = []
        for d in ref_doc_coll.data:
            library.append(
                {
                    "doc_name": d.name,
                    "content": __self.__get_document_content(d.id, domain),
                }
            )
        return library

    @st.cache_data(show_spinner=False, persist="disk")
    def do_semantic_string_compare(
        __self,
        input_0: str,
        input_1: str,
        domain: str,
        model_id: int,
        with_opposite_meaning=False,
    ) -> tuple[bool, float]:
        logging.info("Executing string compare...")
        logging.info(f"Text A: {input_0}")
        logging.info(f"Text B: {input_1}")
        logging.info(f"Using model with ID '{model_id}'")
        if with_opposite_meaning:
            logging.info("Also checking for opposite meaning")
            doc = __self.__get_references(
                input_0, input_1, domain, "23d06b42-4a32-4531-b00e-640f538e2aee"
            )
        else:
            doc = __self.__get_references(input_0, input_1, domain)
        if doc.references:
            if with_opposite_meaning:
                return (
                    doc.pages[0]
                    .contents[0]
                    .paragraphs[0]
                    .references[0]
                    .has_opposite_meaning,
                    doc.references[0].similarity,
                )
            else:
                return False, doc.references[0].similarity
        return False, 0.0

    def change_model(__self, domain: str, model_id: int) -> int:
        logging.info(f"Changing model for domain {domain} to {model_id}")
        return int(
            __self.__sdk.domains(domain)
            .settings.patch(Settings(similarity_model_id=str(model_id)))
            .similarity_model_id
        )

    def __get_references(self, input_0, input_1, domain, doc_type=None):
        return self.__sdk.domains(domain).references.post(
            file=_to_text_file(input_0),
            referencedocument=_to_text_file(input_1),
            similaritythreshold=0.01,
            maxreferences=1,
            documenttype=doc_type,
        )

    def __get_document_content(self, doc_id: str, domain: str) -> str:
        doc = self.__get_ref_doc(doc_id, domain)
        content = ""
        for p in doc.pages:
            for c in p.contents:
                if c.paragraphs is not None:
                    content += "\n".join([par.text for par in c.paragraphs])
        return content

    def __get_ref_doc_name(self, doc_id: str, domain: str) -> str:
        return self.__get_ref_doc(doc_id, domain).name

    def __get_ref_doc(self, doc_id: str, domain: str) -> Document:
        return self.__sdk.domains(domain).referencedocuments(doc_id).get()
