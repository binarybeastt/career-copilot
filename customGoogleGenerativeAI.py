from typing import Any, Dict, Optional, List
from langchain_core.runnables import Runnable
from langchain_core.prompt_values import ChatPromptValue
import google.generativeai as genai
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Define the log format
    handlers=[
        logging.StreamHandler(),  # Log to the console
        logging.FileHandler("app.log"),  # Log to a file
    ],
)

# Create a logger for this module
logger = logging.getLogger(__name__)

class LLMResult:
    def __init__(self, content: str):
        self.content = content
        logger.debug(f"LLMResult initialized with content: {content}")

class ChatGoogleGenerativeAI(Runnable):
    def __init__(self, model: str, temperature: float = 0.5, verbose: bool = False, google_api_key: str = None):
        self.model_name = model
        self.temperature = temperature
        self.verbose = verbose
        self.tools = []  # Initialize an empty list to store tools

        # Configure the API key
        self.api_key = google_api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            logger.error("GOOGLE_API_KEY must be provided or set as an environment variable.")
            raise ValueError("GOOGLE_API_KEY must be provided or set as an environment variable.")
        genai.configure(api_key=self.api_key)
        logger.info(f"Configured Google Generative AI with API key: {self.api_key}")

        # Initialize the model
        self.model = genai.GenerativeModel(self.model_name)
        logger.info(f"Initialized model: {self.model_name}")

    def bind_tools(self, tools: List[Any]):
        """
        Bind tools to the LLM so that it can call them when necessary.

        Args:
            tools (List[Any]): A list of tools to be bound to the LLM.
        """
        self.tools = tools
        logger.debug(f"Bound tools to the model: {tools}")

    def invoke(self, input: Any, config: Optional[Dict[str, Any]] = None) -> LLMResult:
        """
        Generate a response to the given prompt.

        Args:
            input (Any): The input, which can be a dictionary or a ChatPromptValue.
            config (Optional[Dict[str, Any]]): Additional configuration options.

        Returns:
            LLMResult: An object containing the generated response.
        """
        logger.info("Starting invoke method")

        # Handle ChatPromptValue input
        if isinstance(input, ChatPromptValue):
            prompt = input.to_string()  # Convert ChatPromptValue to a string
            logger.debug(f"Converted ChatPromptValue to string: {prompt}")
        elif isinstance(input, dict):
            prompt = input.get("query", "")  # Extract the prompt from the input dictionary
            logger.debug(f"Extracted query from input dictionary: {prompt}")
        else:
            logger.error(f"Unsupported input type: {type(input)}")
            raise ValueError(f"Unsupported input type: {type(input)}")

        if self.verbose:
            logger.info(f"Generating response for prompt: {prompt}")

        # Generate the response
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"temperature": self.temperature}
            )
            logger.debug(f"Generated response: {response.text}")
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

        if self.verbose:
            logger.info(f"Response: {response.text}")

        return LLMResult(content=response.text)  # Return an LLMResult object

# Example usage
if __name__ == "__main__":
    logger.info("Starting script")

    # Set up the API key (or use environment variable)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.error("GOOGLE_API_KEY environment variable not found.")
        raise ValueError("GOOGLE_API_KEY environment variable not found.")

    # Initialize the custom wrapper
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.5,
            verbose=True,
            google_api_key=api_key
        )
        logger.info("Initialized ChatGoogleGenerativeAI")
    except Exception as e:
        logger.error(f"Error initializing ChatGoogleGenerativeAI: {e}")
        raise

    # Generate a response
    input_data = {"query": "Explain how AI works"}
    logger.debug(f"Input data: {input_data}")

    try:
        response = llm.invoke(input_data)
        logger.info(f"Response content: {response.content}")
        print(response.content)
    except Exception as e:
        logger.error(f"Error invoking model: {e}")
        raise

    logger.info("Script completed successfully")