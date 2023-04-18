import io
from typing import List

import semantha_sdk
from semantha_sdk.model.document import Document
from semantha_sdk.model.domain_settings import PatchDomainSettings


def _to_text_file(text: str):
    input_file = io.BytesIO(text.encode("utf-8"))
    input_file.name = "input.txt"
    return input_file


class SemanthaConnector:
    def __init__(
        self,
        server_base_url="http://localhost/tt-platform-server",
        streamlit_domains_prefix="",
        api_key=None,
    ):
        self.__sdk = semantha_sdk.login(server_url=server_base_url, key=api_key)
        self.__streamlit_domains_prefix = streamlit_domains_prefix

    def get_streamlit_domains(self) -> List[str]:
        domains = self.__sdk.domains.get()
        return [d.name for d in domains if self.__streamlit_domains_prefix in d.name]

    def query_library(
        self, text: str, domain: str, threshold=0.75, max_references=10, tags=None
    ):
        doc = self.__sdk.domains(domain).references.post(
            file=_to_text_file(text),
            similaritythreshold=threshold,
            maxreferences=max_references,
            tags=tags if tags is not None else [],
        )
        result_dict = {}
        if doc.references:
            for ref in doc.references:
                result_dict[ref.document_id] = {
                    "doc_name": self.__get_ref_doc_name(ref.document_id, domain),
                    "content": self.__get_document_content(ref.document_id, domain),
                    "similarity": ref.similarity,
                }
        return result_dict

    def get_library(self, domain: str, tags=None, **kwargs):
        limit = kwargs.get("limit", None)
        if limit is None:
            offset = None
        else:
            offset = kwargs.get("offset", 0)
        ref_doc_coll = self.__sdk.domains(domain).referencedocuments.get(
            tags=tags, offset=offset, limit=limit
        )
        library = []
        for d in ref_doc_coll.documents:
            library.append(
                {
                    "doc_name": d.name,
                    "content": self.__get_document_content(d.id, domain),
                }
            )
        return library

    def do_semantic_string_compare(
        self, input_0: str, input_1: str, domain: str
    ) -> float:
        doc = self.__get_references(input_0, input_1, domain)
        if doc.references:
            return doc.references[0].similarity
        return 0.0

    def get_opposite_meaning(self, input_0: str, input_1: str, domain: str) -> bool:
        doc = self.__get_references(
            input_0, input_1, domain, "23d06b42-4a32-4531-b00e-640f538e2aee"
        )
        return (
            doc.pages[0].contents[0].paragraphs[0].references
            and doc.pages[0]
            .contents[0]
            .paragraphs[0]
            .references[0]
            .has_opposite_meaning
        )

    def change_model(self, domain: str, model_id: int) -> int:
        return int(
            self.__sdk.domains(domain)
            .settings.patch(PatchDomainSettings(similarity_model_id=str(model_id)))
            .similarity_model_id
        )

    def __get_references(self, input_0, input_1, domain, doc_type=None):
        return self.__sdk.domains(domain).references.post(
            file=_to_text_file(input_0),
            referencedocument=_to_text_file(input_1),
            similaritythreshold=0.01,
            maxreferences=1,
            tags=[],
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
