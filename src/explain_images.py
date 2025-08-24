from langchain_core.messages import HumanMessage, SystemMessage

class ExplanationGenerator:
    """
    AI-Powered Explanation Generator for image–query relevance.

    Responsibilities:
        • Generate concise explanations for why an image is relevant to a query
        • Highlight specific visual elements, attributes, or context
        • Ensure explanations are business-appropriate and technically sound
    """

    def __init__(self, llm_model):
        """
        Args:
            llm_model : Chatopenapi endpoint (open/closed source)
        """
        self.llm = llm_model

        # Define reusable system prompt
        self.system_prompt = SystemMessage(
            content=(
                "You are an AI assistant that generates short, "
                "business-appropriate explanations for why an image is relevant to a search query. "
                "Always:\n"
                "• Write in 2–3 concise sentences.\n"
                "• Highlight specific visual elements, attributes, or context.\n"
                "• Avoid vague or generic phrases (e.g., 'This image matches the query').\n"
                "• Keep tone professional and technically sound."
            )
        )

    def explain(self, query: str, img_b64: str) -> str:
        """
        Generate an explanation for why the given image matches the query.

        Args:
            query (str): The search query (user intent).
            img_b64 (str): Base64-encoded image content.

        Returns:
            str: A concise, business-appropriate explanation (2–3 sentences).
        """
        image_input = {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}
        }

        user_message = HumanMessage(content=[
            {
                "type": "text",
                "text": (
                    f"Query: '{query}'\n"
                )
            },
            image_input
        ])

        response = self.llm.invoke([self.system_prompt, user_message])
        return response.content.strip()
