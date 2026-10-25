"""Versões do prompt de extração. No máximo três, conforme o plano."""

V1 = """Você recebe uma imagem de livros: uma foto de estante ou uma tela da biblioteca do Kindle.
Liste todos os livros cujo título você consegue ler na imagem.

Regras:
- Inclua apenas livros cujo título esteja legível, ao menos em parte. Não adivinhe livros ilegíveis.
- Se o título estiver truncado ou cortado na borda, devolva o título completo só se reconhecer o livro com segurança; senão, devolva o trecho que lê.
- Autores: os que aparecem na imagem ou que você reconhece com segurança pelo título. Se não souber, lista vazia.
- Em telas do Kindle, ignore a miniatura do livro em reprodução no canto inferior esquerdo, a barra de navegação e os selos. Use os selos só para o status: "lido" para o selo READ, "em leitura" para um percentual, senão null.
- Em fotos de estante, leia as lombadas, inclusive as verticais, e os livros deitados com título legível.
- Cada livro aparece uma vez por imagem.

Responda apenas com JSON, sem comentários:
{"livros": [{"titulo": "...", "autores": ["..."], "status": "lido" | "em leitura" | null, "confianca": "alta" | "media" | "baixa", "trecho": "texto como aparece na imagem"}]}"""

PROMPTS = {"v1": V1}
