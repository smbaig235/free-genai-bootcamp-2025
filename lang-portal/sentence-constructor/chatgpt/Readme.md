# French Language:  Sentence Constructor


### AI Assistant: ChatGPT 

### LLM Model: ChatGPT-4-turbo (free)
OpenAI hasn't publicly disclosed the exact number of parameters for GPT-4 or GPT-4-turbo.
However, it's significantly larger and more efficient than previous models like GPT-3, which had 175 billion parameters. 
GPT-4-turbo is optimized for speed and cost while maintaining high performance.
GPT-4 Turbo shows lower accuracy. 


## Objective:

The goal is to assist an AI-powered assistant in helping students learn French through sentence structure, grammar, tenses, examples, and contextual clues. This AI assistant serves as a virtual French language teacher, guiding students throughout their learning journey.

## Custom Prompt:

Prompt engineering often requires an iterative approach. We began with a highly relevant prompt, reviewed the response, and refined it based on the results. As needed, we added more context or simplified the request to better align with the intended outcome.

## Applied Prompt Techniques:

### Chain of Thought:
This technique encourages the model to generate more thoughtful, well-reasoned responses by providing step-by-step instructions.

#### Benefits:
* Improved Coherence: 
This method helps the model think through questions logically and structurally, resulting in more coherent and relevant responses.

* Increased Depth: 
By offering a series of prompts or questions, we enable the model to explore topics in greater detail and depth.

### Retrieval-Augmented Generation (RAG):
This technique combines retrieval-based methods with generative models to improve response quality. First, the system retrieves relevant documents or pieces of information based on the input query. This retrieved data is then used to augment the model’s input, allowing the generative model to produce more informed, contextually relevant responses.

#### Benefits:
* Enables the model to access external knowledge that may not be part of its training data, improving the accuracy and contextual relevance of responses.

### Few-Shot or Zero-Shot Prompting:
This technique involves providing examples to the model in order to improve the accuracy and precision of the output.

### Use of Delimiters in the Prompt:
Delimiters help segment the text within a prompt, making it clear to the model what specific text needs to be translated or addressed.

### Role-Based Prompting:
By assigning a specific role to the AI, we can guide it to produce responses that align with the desired outcome. In our case, the AI assistant assumes the role of a French language teacher, which helps generate more engaging and relevant responses.

#### Benefits:
* Improved Relevance: Tailoring the prompt to a specific role ensures the response is better aligned with the context.
* Increased Accuracy: Role-based prompting enhances the model’s ability to produce precise and appropriate responses.

### Eliminating Hallucinations:
To improve accuracy, we test the prompt across different AI assistants to identify and address any potential hallucinations (incorrect or fabricated information). Additional context is provided as needed to guide the model towards more accurate results.

### Conclusion:

By applying both input and output guardrails to the model and prompt engineering techniques, we achieved more refined and reliable results, ensuring the AI assistant delivers better guidance for students learning French.

#### Resources:
  - [https://chatgpt.com/]
  - [https://help.openai.com/en/articles/10032626-prompt-engineering-best-practices-for-chatgpt]