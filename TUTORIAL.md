# Como Testar o Auto-Character-RAG Localmente

Para rodar o nosso servidor inteligente e testar a geração de personagens, siga os 3 passos abaixo na sua máquina:

### 1. Configure a IA (`config.json`)
Abra o arquivo `config.json` que está na raiz desse projeto. Na seção `"llm"`, coloque a **base_url** e a **api_key** da API que você usa no Silly Tavern. 
- *Exemplo LM Studio:* `http://127.0.0.1:1234/v1` (não precisa de key).
- *Exemplo OpenAI:* `https://api.openai.com/v1` e coloque sua key real.

### 2. Jogue suas Novels pra dentro!
Copie os seus arquivos `.txt` brutões das Novels para a pasta `data/novels/`. (Já deixei um `novel.txt` vazio ali, você pode jogar o texto dentro dele ou colocar outros arquivos).

### 3. Ligue o Servidor Backend!
Abra o terminal dentro dessa pasta do projeto e rode:
```bash
python main.py
```

### 4. Usando o Sistema (Sem precisar de Frontend por enquanto!)
O servidor vai ligar! Agora é só você abrir seu navegador de internet e acessar: 
**`http://127.0.0.1:8000/docs`**

Essa é a interface mágica do Swagger. Para testar:
1. Clique na rota verde chamada `/api/v1/ingest`, clique em "Try it out" e depois no botão azul "Execute". Ele começará a ler e vetorizar suas novels no terminal (aguarde terminar).
2. Quando a ingestão acabar, abra a rota `/api/v1/generate_card`, clique em "Try it out", escreva o nome do personagem (ex: `"Guts"`) no campo `character_name` e clique em "Execute".
3. **Pronto!** O Card novinho em folha vai aparecer na pasta `data/output/` no formato JSON do Silly Tavern!
