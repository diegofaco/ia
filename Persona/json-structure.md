As mentioned, you shouldn't rely on a LLM to give any specific structured response. I do this kind of thing by extracting the json using a regex.

Having said this, you can pretty reliable insist on only json with something like this: 

"From now on when you respond you will provide only a codeblock with json and nothing else. I am going to describe a project and you will provide a json describing it. The json will have the following properties: estimatedHours, complexity(1-10) and summary. The job to respond to is: \`\`\`Power wash a 4 x 5 concrete slab\`\`\` Remember you must provide only a codeblock containing json, absolutely no additional text or explanation"