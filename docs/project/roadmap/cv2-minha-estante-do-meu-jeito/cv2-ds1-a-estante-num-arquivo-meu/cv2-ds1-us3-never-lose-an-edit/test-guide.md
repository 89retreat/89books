[< Story](index.md)

# Test Guide — CV2.DS1.US3 Never lose an edit

## Automated Validation

```bash
uv run pytest tests/test_history.py tests/test_cli.py tests/test_main.py tests/test_status.py tests/test_gitignore.py
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Cobrir snapshots exatos, marcador de draw, nomes collision-safe, retenção 20,
arquivos desconhecidos, history sem leitura de conteúdo, restore seguro,
recreate confirmado e todas as falhas antes/depois de cada write.

## Navigator Validation

Na cópia descartável de uma foto:

1. edição + draw cria uma versão; draw idêntico não cria outra;
2. history lista metadados; arquivo quebrado pode voltar por restore e também
   fica preservado;
3. recreate recusado não muda nem gasta;
4. depois de nova confirmação explícita, uma única recriação paga de uma foto
   guarda a versão atual, troca somente a fonte e recomenda draw;
5. restaurar a versão pré-recreate e desenhar devolve a estante editada.

Não comparar o conteúdo das versões reais sem autorização adicional.

## Validation Evidence

A registrar depois da implementação e da validação do Navigator.
