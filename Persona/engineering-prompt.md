ChatGPT is most likely the single AI tool that will have the greatest impact on how most of us work. People have dubbed it a “Google killer” due to its ease of use and extremely powerful language model, and while this is debatable, there is no denying its impact will be enormous. However, when working with ChatGPT, one will notice that the AI produces mixed results, especially when the instructions are more complex. Often, this does not imply that ChatGPT cannot solve the problem; it simply means that the Language Model does not understand what we expect from it. In this article, I will present a convenient way to engineer prompts that generate the expected output while being able to leverage the complexity of the instructions.

Table of Contents

· Basic Concepts

· Introducing a Generic Framework for Prompt Engineering

∘ Basic Instructions

∘ Specifiers

· List of Elements

· Engineering a prompt

∘ Reprompting

∘ Prompt Editing

· Conclusion

Basic Concepts

While you can talk to ChatGPT in the same way you talk to people, the results may be less than ideal. Despite its name, the notion that ChatGPT is a chatbot is somewhat misleading. ChatGPT is based on a large language model (GPT3) that does not respond to your messages, but instead provides the most accurate output based on its training data. While it was trained on a more specific training data to understand human instructions, the basic concept remains the same.

ChatGPT’s language model was trained using a large amount of data comprised of pairs of sample input and expected output. It would look something like this when trained for a chatbot:

Prompt: Hey, why did you just leave?

Completion: I felt sick suddenly, sorry for not telling you. When did you leave?

Prompt: At 4am — the cocktails were sooooo good!

Completion: Definitely, but I guess the tuna was bad…

The more complex the input, the harder it is for the language model to find corresponding patterns in its training data, resulting in less accurate responses. The level of perplexity is used to determine the complexity of a prompt. This metric measures how well a language model can predict a given piece of text. A lower perplexity value indicates that the model can predict the test set better.

So, in order to optimize our output, we must first optimize our input. The table below displays some prompts, the corresponding output, and the level of perplexity as calculated by the betterprompt tool.

As we can see in the majority of examples, the perplexity is related to the output quality. But the perplexity in the last example is relatively low, whereas ChatGPT generates nonsense. That is because the structure of the input is illogical to ChatGPT. Also, the level of perplexity does not directly correlate with the length of the input.

This leads to the work’s main assumption: That the structure of a prompt is crucial.

Introducing a Generic Framework for Prompt Engineering

In a series of test prompts, I created a generic framework for optimizing prompts. The schemes color-coded design makes engineering ChatGPT prompts simple, replicable, and easy to document, while a color code does not affect the syntax. Although this idea is based on ChatGPT, it can be applied to other LLM.

Basic Instructions

For our scheme, we assume that a great ChatGPT prompt is made up of various elements. All these elements are somehow related to instructions, but we need to understand what the different elements of our prompts are actually influencing. Let us take prompt 3 from the table above:

You are a banking professional. Answer the following E-Mail:

I’ve highlighted three parts of this prompt: The Initiation, the Functional Instruction and the Data Input. These Basic Elements are the most common elements: An Instruction OR a Data Input (for completition tasks) is mandatory to get any useful output (at least in all cases I could think of).

Initiation

The first, blue highlighted element is what we’ll call “Initiation”. An initiation instructs ChatGPT on how to behave. It establishes the context and tone for the generation, giving the model an understanding of the role it is expected to play. It can be from different points of view (“I am a banking professional. Answer my E-Mail:”) or contain additional data (“I wrote a program that allows to divide by 0. Give me a good name for the software.”).

Functional Instruction

The second, red element is an instruction, we will call it the “Functional Instruction”. It instructs the model on the task at hand, in this case responding to an email. It can be imperative or a question.

Data Input

“Data Input” is the third, violet element. It contains the specific information or data that the model requires to complete the task. In this case, the model is expected to respond to the email. This is the input that the model will use to generate the output based on the context and instructions provided.

This classification enables the prompt to be precisely designed to the expected output — and, moreover, it enables the prompt to be changed without breaking the logic of the prompt. We could change the Initiation of our prompt to something else, for example:

Imagine you are a confused, angry customer. Answer the following E-Mail:

Despite using the same Functional Instruction, the output is fundamentally different now:

Dear Richard,

I am not sure what you are talking about with a new credit line. I did not make any phone call to you yesterday and I am not interested in discussing any credit lines. I am extremely confused and frustrated about this situation. Please clarify what is going on and provide any information that you may have about this supposed phone call.

Sincerely, Thorbjörn

Of course, if we change the Functional Instruction or the Data Input, the output will also change, but if we keep this general structure, we will always get a reasonably good output.

Specifiers

However, there are times when we need to specify something else in the output. For example, we could tell ChatGPT to format the output in Markdown.

Hi Richard,

Thanks for your call yesterday. I wanted to follow up and see if you would be available to chat about our **new credit line** on Tuesday at 11:00 a.m.?

As a valued customer of our bank, I wanted to make sure you were aware of this **great opportunity** to increase your credit line and have more financial flexibility. Our credit card also offers **rewards and benefits** such as cash back, travel points, and exclusive discounts.

Let me know if this time works for you and we can schedule a call. Thank you in advance!

Best,

Thorbjörn

We run a similair task, but instructed ChatGPT to format our output in a special way with what we’ll call a Format Specifier. It’s one of several Specifiers that all have in common that they define our task in detail by fine-tuning, restraining or enhancing the Basic Instructors. Specifiers typically are called in the later part of the prompt.

Format Specifier

This green highlighted element is what we’ll call a Format Specifier as it helps us to instruct ChatGPT to a specific output format. We can tell Chat GPT to format the content (like hoighlighting) or or how to render the output data (e.g. as html; in a code block; in a table).

This is a list of possible Elements I could identify so far:

List of Elements

Keep in mind: Since we are dealing with language, the possible inputs are endless. Our goal is not to get any valid input into our scheme, but to find a way of engineering prompts. So, let’s see how we can use the Scheme to design a prompt.

Engineering a prompt

When creating a prompt, we must focus on the output. We have to specify precisely what we want, in what format we want it, and what information is required for that task. When having trouble with finding the right prompt, I open up a Google Docs and write down my expectations. Then I will rephrase my expectations to get the Elements mentioned, above. Assume we need a summary of Goethe’s Faust:

Expected output

Content: A summary of Goethes Faust with an emphasis on the figure of Mephisto.

Format: In markup, with subtitles, in a code block.

Tone: Like a professor of the field

Needed input

Initiation: Imagine you are a Professor of German studies.

Instruction: Write a summary of Goethe’s Faust.

Scopes: With an emphasis on emphasis on the figure of Mephisto.

Format Specifier: Format in markdown, use subtitles. Use a code block.

Then I will copy the parts, highlight them in the corresponding colors and start trying the ideal wording for each part in order to get the best result. To be able to analyze the prompts, I like to use tables to protocol every single try and its corresponding output. Changes will be easy since all our prompts are color-coded.

Reprompting

Reprompts are what makes ChatGPT feel like a chat: We can ask further questions or anything else — but as you might expect, it’s not a good idea to switch topics all too often. Use another Conversation instead.

Note that the whole history of the conversation is included in every reprompt, hence it quickly results in weird outputs. It is crucial to minimize the amount of reprompts and to optimize the structure of the reprompts. The basic structure remains the same.

Especially when it comes to Format Specifiers, it is a good practice to repeat them in a reprompt if needed, since ChatGPT tends to “forget” them.

Prompt Editing

Editing a prompt is a good way to test different prompts for the same task. Try to minimize the editing of prompts that are not the last, since you and ChatGPT will get confused by the inconsistency of the prompt history.

Bild von Gerd Altmann auf Pixabay

Conclusion

ChatGPT is a powerful AI tool that has the potential to change the way we work. However, the outcome can be mixed, especially when the instructions are more complex. To optimize the output, we must first optimize the input. This approach is based on the premise that the structure of a prompt is critical and that a great ChatGPT prompt is made up of various elements. By understanding these elements and how they influence the output, we can create prompts that generate the expected results while leveraging the complexity of the instructions.

We can make working with ChatGPT more efficient and effective using a standardized framework for quick engineering. The suggested scheme is easy to replicate and document, and can be applied to other large language models as well. Overall, by using this method, we can extend the potential of working with ChatGPT and take our work to the next level.