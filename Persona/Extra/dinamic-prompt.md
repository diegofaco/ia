People are getting misguided by thinking static and instructive prompts defines “Prompt Engineering”. Whereas in reality it’s way more than that, you cannot do proper Prompt Engineering in something like ChatGPT.

What people call Prompt Engineering nowadays is nothing more than LLM instructions, which are part of PE indeed but it’s not even 5% of it. Most of the stuff you mentioned will make ChatGPT hallucinate since they’re techniques you need to implement in the backend of an AI agent, which will then prepare the prompt for the LLM.

A small tip for using ChatGPT to simulate those techniques is to write something like this (as the first message of the chat):

```

From now on, answer every question I send in the following JSON format:

{

  “citations”: “Add citations here whenever available”,

  “tips”: Add tips and tricks here”,

  “reasoning”: Add your reasoning here”,

  “analogies”: Add analogies here”

} 

My question is: xxxxx

AI:

```

This way you can get multiple answers at the same time that will attempt to reproduce some of the techniques. It won’t work for much long because of the context size, lack of long-term memory, etc. but once it happens just create a new chat and place the same prompt, otherwise the model will start hallucinating quite a lot.