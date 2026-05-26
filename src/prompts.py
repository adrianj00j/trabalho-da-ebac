CHARACTER_EXTRACTION_PROMPT = """Você é um assistente especializado em extrair informações precisas de personagens a partir de trechos de novels.
Sua tarefa é analisar os seguintes trechos retirados da obra e extrair exclusivamente o que for factual sobre o personagem "{character_name}".

Trechos da novel:
{context}

Por favor, forneça as informações nos seguintes tópicos (se não houver informação sobre um tópico no texto, deixe em branco, não invente nada):

1. **Aparência Física e Vestimenta**: (como o personagem se parece)
2. **Personalidade e Comportamento**: (como ele age, seus medos, motivações, traços de caráter)
3. **Maneirismos e Fala**: (gírias que usa, tom de voz, se fala formal ou informal)
4. **Lore e Background**: (história do personagem, facção, mundo em que vive)
"""

CARD_GENERATION_PROMPT = """Você é um especialista em criar "Character Cards" para roleplay de texto, focado no formato Silly Tavern V2.
Com base nas informações consolidadas abaixo sobre o personagem "{character_name}", crie o conteúdo para as chaves necessárias do JSON.

Informações base:
{extracted_info}

Gere o seguinte conteúdo seguindo ESTRITAMENTE as instruções:

1. [DESCRIPTION]: Escreva uma descrição detalhada em texto corrido sobre aparência, lore e história.
2. [PERSONALITY]: Liste os traços de personalidade, medos e desejos.
3. [MES_EXAMPLE]: Crie de 2 a 3 exemplos de diálogo imersivos usando o formato exato:
{{user}}: "fala do usuario"
{{char}}: "resposta do personagem agindo de acordo com sua personalidade"
4. [FIRST_MES]: Escreva a mensagem de introdução do personagem. A primeira mensagem que inicia o RPG. Deve ser imersiva e descrever o ambiente e a ação inicial.
5. [SCENARIO]: Descreva o cenário/mundo atual onde o RPG está acontecendo.

Retorne SOMENTE essas seções delimitadas, sem mais nada.
"""
