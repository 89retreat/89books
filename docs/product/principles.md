# Product Principles

Princípios de comportamento do produto. Devem orientar escolhas de
implementação, não ficar como slogans. Os oito primeiros vieram da
[ES-001](../project/exploration/es-001-a-estante-como-retrato/index.md); os
três últimos, da avaliação da CV2 em 2026-10-28. A direção de mais longo prazo
(para quem o produto vai, e por que caminho) está em
[direction.md](direction.md).

## Principles

### A estante é o centro

O gesto fundador é visitar a estante de alguém. Recomendações, resenhas e
listas giram em torno dela, nunca o contrário.

Na prática, a estante aparece como conjunto (capas reunidas), não como lista de
dados. Qualquer nova funcionalidade precisa dizer o que acrescenta à visita.

### Não começar vazio

Ninguém deveria entrar diante de um perfil vazio e cadastrar a própria
identidade leitora do zero. A pessoa traz livros que já existem: uma foto de
estante, um print do Kindle ou um primeiro conjunto escolhido.

Na prática, a pessoa recebe a estante pronta, com a leitura da IA, e a
corrige aos poucos. Corrigir é a primeira visita à própria estante, não um
formulário que vem antes dela.

### A foto da estante física é a presença

A estante física é lenta e material; o que está nela carrega peso. A foto
apresenta a pessoa (capa, miniatura) e não deve ser trocada por um avatar
genérico.

### Cada leitor revela a própria lógica

Não impor uma taxonomia universal. Lugares, agrupamentos e posições podem ter
significados que só o leitor conhece. A organização autoral (prateleiras,
ordem, livros de frente, textos) entra na CV2; lugares da casa e várias
estantes continuam no horizonte, e o modelo de dados não deve fechar essa
porta.

### A estante não precisa explicar a pessoa

Sem timeline obrigatória, sem inferência da "jornada" de leitura. A estante dá
matéria para perguntas; a resposta vem na conversa.

### A conversa acontece onde as pessoas já estão

O produto faz o livro aparecer entre as pessoas; não precisa hospedar a
conversa. Na CV1, a pessoa leva a estante a quem quiser, por arquivo ou link;
na CV4, os movimentos vão para um grupo dedicado do Telegram.

Na prática, nada de feed, comentários ou mensagens internas até o uso pedir.

### Interesse, não intimidade

O recorte são pessoas para quem livro rende assunto, sejam amigos, conhecidos
ou alguém que se admira. O alcance público fica para depois do dogfood.

### A leitura não vira prestação de contas

Registrar e compartilhar devem servir a quem lê. Nada de metas, sequências,
contadores, estrelas ou lembretes que cobrem leitura.

Na prática, compartilhar um insight é sempre uma escolha, e a frequência dos
movimentos não pode virar ruído. Se o grupo silenciar o bot, o produto falhou.

### A última palavra é de quem lê

A IA propõe a primeira estante: livros, prateleiras, retrato. Depois, a
pessoa decide. Nenhuma rodada automática passa por cima do que ela escreveu ou
arrumou.

Na prática, o que a pessoa edita (no `shelf.yaml` hoje, numa tela amanhã) é a
fonte da estante; as regras automáticas valem só para o que ela não decidiu.

### Nada se perde

Editar a própria estante não pode dar medo. Todo gesto que reescreve a estante
guarda antes a versão anterior e diz onde ela ficou; voltar é simples.

### Gastar é sempre uma escolha

Ver a estante, conferir e redesenhar nunca custam. O que custa (ler fotos,
escrever um retrato) diz quanto vai custar e espera a confirmação. Entrar no
produto sem saber o que fazer nunca gasta: mostra onde a pessoa está e o
próximo passo.

## Questions to Answer

- O que separa um movimento que vale bater à porta de alguém de um que é ruído?
- Até onde o reconhecimento automático pode errar antes de estragar a entrada?
- Que edições as pessoas fazem de fato na própria estante? Elas querem
  controle total ou só consertar meia dúzia de coisas?
