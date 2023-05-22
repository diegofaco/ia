3 Principles for prompt engineering with GPT-3

Published on Dec 3, 2022

Ben Whately

Ben Whately

Entrepreneur | Investor | Speaker

Published Dec 3, 2022

 Follow

[Long, geeky post alert!]

Large Language Models (LLMs) are changing what is possible for computers to do in ways that boggle the mind. 

I’ve spent a lot of this year with GREG and others creating the world’s first AI language partner - The MemBot - on top of one of the most powerful LLMs, called GPT-3. The MemBot can hold totally human-like conversations in real-time on any topic in dozens of languages. It can even offer advice on how to improve your grammar. 

This kinds of human-like conversation is a game changer in a load of obvious places. I don’t think I need to list them out here - I want to get to the meaty problem of how we make it work. The field of programming LLMs is very new and still not well understood. It is very different to “normal” programming, because the models work much more like a human brain and much less like a traditional computer. 

In this post I’d like to share some of the learnings we’ve had along the way - we’ve had to do a lot of trial and error, and hopefully we can share some shortcuts to help anyone else wanting to build on LLMs. 

First up, it’s good to have a mental model of just what GPT-3 is. At its simplest, it is a massive prediction engine. It’s been trained on almost all the text on the internet - trillions of pages. It is trained to predict, “if this text came first, what word comes next?” 

You feed GPT-3 with a prompt - written in plain English, not in code - and it prints out its prediction of the words that should be written after that prompt. The prompt is literally just a request written in normal, natural language, asking it want it to do. 

So if I prompt it with, for example, “write a story,” it will write a story. It will write a different story every time. Here’s one it wrote for me - you can see my prompt with white background and GPT-3’s answer with the green highlight:

No alt text provided for this image

Not a very exciting story… but then again, if you ask a human to just “write a story,” you can’t necessarily expect to get a great result. 

So let’s see if we can do a bit better by asking it to write an exciting story: 

No alt text provided for this image

Ok, a little bit more exciting, at least in the subject matter. 

That gives us Principle 1: be very specific in your instructions. 

Being specific does make GPT-3 perform a bit better, but in this particular case it has still not written what anyone would describe as a ripping yarn.

To make it better, let’s think about how we might teach a student to write a story. We’d probably ask them to break it down into sections: a beginning, middle, and end. Next let's try doing just that.

Let's start by asking it to write an introduction to an exciting story:

No alt text provided for this image

Not bad.

Then use all of that as a prompt, and ask it to write the core of the story (again, the prompt is in white and GOT-3’s response is in green):

No alt text provided for this image

As you can see, it continues the theme and elaborates upon it. It is a little bit clunky in the language here, but we can look at other ways to fix that later. 

Then we can build on all of this and ask it to write a compelling climax:

No alt text provided for this image

It didn’t quite get to the end of that story that time… but it is pretty mind-blowing that this whole narrative has been generated in a few seconds by a computer. A couple of years ago, that would have been unthinkable. And this second draft is already a lot better than our first story - just by getting it to break its work down and tackle it step by step. 

So Principle 2: is to ask GPT-3 to break its work into small chunks. You get better results that way, just as you would with a human. 

By employing both of these lessons, we’ve got something a lot more like a story - but it is still way short of publishable fiction. So what do we do next? 

Just as you might advise human students to check their exam papers before handing them in, we also find that GPT-3 gets much better when you ask it to check its own work. 

For example, we’ve been working on getting GPT-3 to write short stories. To do this we’ve followed principle 2, and asked it first to define the characters in the story. First we just asked it to write a character description:

No alt text provided for this image

This is quite impressive. But it isn’t actually that useful as an input to asking GPT-3 to write a story from it. There is actually too much information that isn’t useful as specific input: when we used this kind of description as a prompt for writing a story, it didn’t lead to interesting stories: eg the part about being “highly organized and efficient” got prioritized and led to bizarrely uninteresting plots. 

We need to get GPT-3 to follow principle 1, and be more specific. Let’s say I also want to be sure for this story that the character is a bit off-the-wall. Something surprising and a little crazy. I can build this into the prompt too: 

No alt text provided for this image

Pretty good - that time. But it is still hit or miss. Here is another try from the same prompt that didn't get good results when we used it to actually create a story:

No alt text provided for this image

It seemed like the loud and brash personality just doesn't lead to good plots. So let’s see if we can get GPT-3 to check it and improve it. 

TO do this we can set up a new prompt that defines what a "good" prompt is and asks it to check its previous output to see if it is “good”. This is a long prompt so needs a couple of images:

No alt text provided for this image

No alt text provided for this image

I added in a few more examples (you can see the start of the second example - I added in 5 more), but I hope you get the picture from just the first couple. 

You can see I’ve used the structure that forces GPT-3 to break down the judgment into stages, making the argument both ways before making a judgment. This gets substantially better and more consistent judgments. 

Then I fed in the character description above and asked it to judge if it was good and improve it if it wasn't.:

No alt text provided for this image

As you can see, it’s tuned up the description, changing his personality to “wild and wacky”. Whether or not this actually leads to a better story, you can see that GPT-3 is making a judgment and making an improvement according to the rules we’ve given it - the art is to make sure we feed in the right instruction so that the output is genuinely good. The important point is that we can keep GPT-3 iterating on itself and making its own output better according to rules that we define.

That gives us Principle 3: ask GPT-3 to check and improve its own output.