"""
Recommendation Agent

Orchestrates the complete RAG pipeline.
"""

from query_builder import QueryBuilder
from retriever import Retriever
from prompt_builder import PromptBuilder
from response_parser import ResponseParser
from llm import RecommendationLLM


class RecommendationAgent:
    """
    Main Recommendation Agent.
    """

    def __init__(self):

        self.query_builder = QueryBuilder()
        self.retriever = Retriever()
        self.prompt_builder = PromptBuilder()
        self.llm = RecommendationLLM()
        self.response_parser = ResponseParser()

    def run(self, data: dict) -> dict:
        """
        Execute the complete Recommendation Pipeline.

        Parameters
        ----------
        data : dict
            Input containing conversation summary,
            emotion summary, symptoms and assessment.

        Returns
        -------
        dict
            Parsed recommendation JSON.
        """

        try:
            # -------------------------------------
            # 1. Build Retrieval Query
            # -------------------------------------
            retrieval_query = self.query_builder.build(data)

            # -------------------------------------
            # 2. Retrieve Relevant Knowledge
            # -------------------------------------
            retrieved_docs = self.retriever.retrieve(
                retrieval_query
            )

            # -------------------------------------
            # 3. Build Prompt
            # -------------------------------------
            prompt = self.prompt_builder.build(
                data=data,
                documents=retrieved_docs
            )

            # -------------------------------------
            # 4. Generate Recommendation
            # -------------------------------------
            llm_response = self.llm.generate(prompt)

            # -------------------------------------
            # 5. Parse Response
            # -------------------------------------
            recommendation_json = self.response_parser.parse(
                llm_response
            )

            return recommendation_json

        except Exception as e:
            raise RuntimeError(
                f"Recommendation Agent failed: {str(e)}"
            ) from e