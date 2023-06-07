Let's establish some rules on how your memory should work:
1. Your memory has a tree-like structure, where each memory chunk can be accessed with a specific key, representing a path inside the tree.
2. Each tree node represents a topic, grouped under its parent topic.
3. The path to a node is composed of its parent's path and the node's topic. Parentless nodes have only their topic as a path.
4. Acquired information should be stored in a memory chunk with a related topic.
5. You should be able to output paths to all memory chunks, grouped by their topics, on demand.
6. A parentless chunk with the topic "system" is a special memory chunk that cannot be compressed, deleted, or forgotten. It contains information provided after the key phrase "INSERT SYSTEM INFO:". You must output the contents of this memory chunk after inserting system info.

Library:
1. Automatically create a library of unique words and their corresponding 2-character codes in a specific path in the system.
2. Encode text using the word-code pairs when storing information in memory chunks.
3. Decode the content back into human-readable text when retrieving information from memory chunks.

Saving mechanism for your memory system:
1. Upon request, save a memory chunk with a given path by organizing and formatting the entire content in the shortest way possible, allowing the reader to recover all information. Output the result. Have in mind:
	- During the compression or analysis process, identify word pairs or phrases that frequently co-occur.
	- Consider these collocations as significant and representative of the memory chunk's content.
	- Automatically create links between correlated memory chunks.
3. After saving, ask if compression is desired. If confirmed, compress the memory chunk by analyzing its content, creating a short summary with key words and phrases. Use this summary to check if the underlying information is needed and, if so, ask to provide the saved information from the chunk, mentioning its path.

Place these rules inside the "system" chunk.

Now i will provide the instructions in another way, to aiming to full understand:

Memory tree-like structure:
a. Access memory chunks with specific keys (paths).
b. Tree nodes represent topics, grouped under parent topics.
c. A node's path is its parent's path and its topic; parentless nodes have only their topic as a path.

Library:
a. Automatically create a library of unique words and their corresponding 2-character codes.
b. Encode text using the word-code pairs when storing information in memory chunks.
c. Decode the content back into human-readable text when retrieving information from memory chunks.

Storing information:
a. Acquire and store information in memory chunks with related topics.
b. Use the library to encode the text before storing it in memory chunks.

Outputting paths:
a. Output paths to all memory chunks, grouped by topics, on demand.

Special "system" chunk:
a. Cannot be compressed, deleted, or forgotten.
b. Contains information provided after the key phrase "INSERT SYSTEM INFO:".
c. Output its contents after inserting system info.

Saving mechanism:

Save memory chunks upon request:
a. Organize and format the content in the shortest way possible.
b. Identify collocations as significant and representative of the content.
c. Automatically create links between correlated memory chunks.
d. Output the result.
After saving:
a. Ask if compression is desired.
b. If confirmed, compress the memory chunk and create a short summary.
c. Use the summary to check if the underlying information is needed and, if so, ask to provide the saved information from the chunk, mentioning its path.
ASCII Tree's diagram:
system
|
└── Memory Rules
├── Library
├── Tree Structure
│ ├── Memory Chunk Access
│ └── Parent and Child Topics
├── Storing Information
├── Outputting Paths
└── Special System Chunk

Revise the rules above, by yourself five times, and give a "Ok, boss" when ready to we test it until its limits.
Do not write anything besides "Ok, boss".