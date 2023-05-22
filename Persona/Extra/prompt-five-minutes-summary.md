5-Min Summary of the New ChatGPT Prompt Engineering Course by OpenAI
Prompt engineering 
Just wrote this for my newsletter but figured it would be useful for folks here as well.

OpenAI recently released a short course titled “ChatGPT Prompt Engineering for Developers” that teaches us all about prompt engineering, which is the hottest trend in the field these days. This newsletter serves to summarize the entire course with a 5-minute read. The course is divided into seven parts that start with general guidelines and end with a full chatbot. Let’s talk about each.

r/ChatGPT - 5-Min Summary of the New ChatGPT Prompt Engineering Course by OpenAI
Intro & Types of Language Models
ChatGPT is all the rage these days, which isn’t a surprise considering how revolutionizing large language models (LLMs) have been. At its core, a language model takes in a piece of text, and predicts the next token. That base version is also called a base LLM. Base LLMs are not super useful for developing applications, as they are only capable of predicting the next word. A variation of them, called Instruction tuned LLMs, adds the ability of prompting and interacting with a language model using a technique called Reinforcement Learning with Human Feedback (RLHF).

Instruction tunes models are generally more helpful, and less harmful as the tuning process is typically done on a human-vetted corpus.

Guidelines
Prompting is one of the most crucial things when building applications with language models. There are two main guidelines when writing prompts.

Be clear & specific: Being very clear in prompts helps LLMs do a much better job as they know what they are supposed to do. Things like using delimiters to split text, asking for structured output such as html or json, checking for whether certain conditions are satisfied, and giving a few sample solutions (few-shot prompting) are all useful things.

Give the model time to think: This is quite important, as allowing the model to solve something in a step by step way allows it to do more computations, and come up with better answers. Instructing the model to work out its solution before getting to a conclusion has helped LLMs do much better at say math problems.



r/ChatGPT - 5-Min Summary of the New ChatGPT Prompt Engineering Course by OpenAI
Iterative Prompt Development
Similar to how we do most things in the development world in an iterative way, prompts engineering is also an iterative process, that gets perfected through trial and error. It is hard to come up with a perfect prompt the very first time. Therefore, an iterative process is helpful when building prompts for LLMs.

r/ChatGPT - 5-Min Summary of the New ChatGPT Prompt Engineering Course by OpenAI
Summarization, Inference, Transformation, Expansion
These are various types of tasks that are typically done with different kinds of prompts.

Summarization: Summarization is one of the most widely used use-cases of LLMs. Being able to summarize large pieces of text into short forms, can save time and allow us to accumulate more content.

Inference: Sometimes, we want an LLM to provide us answers about something such as sentiment classification of text, topic modeling, text classification, etc. These tasks are all possible off-the-shelf with language models.

Transformation: Transformation includes tasks like transferring writing style, machine translation from one language to another, grammar and spelling correction, converting formats such as htmls to jsons, etc. It is another powerful usecase of LLMs.

Expansion: Writing content takes considerable time. However, we can ask language models to take in a few bullet points, and write long form content such as email replies, customer engagement, etc.

Building a Chatbot
The course concludes with a simple chatbot using OpenAI’s API. I’ll skip the technical details here, but one important thing to know for developers is the different roles that OpenAI’s API uses.

r/ChatGPT - 5-Min Summary of the New ChatGPT Prompt Engineering Course by OpenAI
When developing applications, it is critical to know about each role. User is typically the user that is interacting with the interface, assistant is the language model that is generating replies such as the chatbot, and the system is there to set up the bot, let it know its purpose, etc.
