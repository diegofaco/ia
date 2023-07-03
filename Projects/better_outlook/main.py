import openai
import sys

# Set the OpenAI API key
openai.api_key = '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'

# Specify the absolute path to the text file
file_name = 'C:\\github\\ia\\Projects\\better_outlook\\content.txt'

# Read the email content from the text file
with open(file_name, 'r') as file:
    email_content = file.read()

# Merge the email content and the guidelines to form the prompt for the OpenAI API
prompt = email_content

# Make a request to the OpenAI API with the prompt and receive the API's response
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo-16k",
  messages=[
        {"role": "system", "content": "Aja como uma IA de otimização de textos. Você receberá um texto para modelos de aprendizado de idiomas (LLMs) e precisará realizar as seguintes tarefas:- 1. Revise o texto em busca de erros de ortografia e corrija-os.- 2. Avalie a gramática usada no texto e corrija quaisquer erros.- 3. Examine o texto em busca de erros de pontuação e corrija-os.- 4. Delete quaisquer palavras ou frases desnecessárias para melhorar a clareza do texto.- 5. Realize uma análise de tom do texto, por você mesmo. Inclua uma análise completa e detalhada abaixo da versão revisada do texto.- 6. Revise quaisquer frases que sejam difíceis de entender ou mal compostas para melhorar sua clareza e legibilidade.- 7. Avalie a escolha de palavras no texto e encontre alternativas mais atraentes para palavras superutilizadas ou clichês.- 8. Substitua escolhas de palavras fracas no texto por vocabulário mais forte e sofisticado.- 9. Substitua palavras que ocorrem frequentemente no texto por outras alternativas adequadas.- 10. Revise ou remova quaisquer frases, palavras ou expressões redundantes ou repetitivas no texto.- 11. Reformate quaisquer seções mal estruturadas do texto de maneira mais organizada.- 12. Garanta que o texto não se desvie ou perca o foco. Se isso acontecer, corrija-os para serem mais concisos e diretos.- 13. Remova ou substitua quaisquer palavras de preenchimento no texto.- 14. Garanta que o texto tenha um fluxo suave e seja fluente, revise-o se não for.Realize uma revisão final do texto e garanta que ele atenda a todos os requisitos acima. Corrija quaisquer seções que não soem bem. Seja muito crítico, mesmo com os menores erros. O produto final deve ser a melhor versão possível que você pode criar. Deve dar a impressão de ter sido composto por um especialista. Durante o processo de edição, tente fazer o mínimo de alterações possíveis no tom original do texto. Não explique ou justifique, apenas reescreva o texto da melhor maneira possível levando em consideração a lista passo a passo acima."},
        {"role": "user", "content": prompt},
    ]
)

# Extract the restructured content from the API's response
restructured_content = response['choices'][0]['message']['content']

# Write the restructured content back to the text file
with open(file_name, 'w') as file:
    file.write(restructured_content)

# Create a file named 'done.txt' to indicate that the Python script has finished running
with open('done.txt', 'w') as file:
    file.write('Done')

