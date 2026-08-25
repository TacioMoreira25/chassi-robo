# Chassi Robô - Parametric CAD Project

Este projeto consiste na modelagem CAD paramétrica de um chassi de robô utilizando a biblioteca **build123d** em Python. O chassi é composto por peças de madeira e peças impressas em 3D.

## Tecnologias e Dependências

- **Linguagem:** Python 3.x
- **Core CAD:** [build123d](https://github.com/gumyr/build123d)
- **Visualização:** [ocp_vscode](https://github.com/bernhard-42/vscode-ocp-cad-viewer) (OCP CAD Viewer no VS Code)
- **Utilitários:** `watchfiles` para recarregamento automático durante o desenvolvimento.

## Estrutura do Projeto

- `main.py`: Ponto de entrada principal que realiza a montagem final e exibe o modelo no visualizador.
- `config.py`: Dimensões globais e estruturais base. Alterar aqui escala o robô por completo.
- `medidas.py`: Parâmetros de furação, variáveis calculadas e medidas específicas de peças.
- `montagem.py`: Orquestra a composição das diferentes sub-montagens e partes.
- `pecas_madeira/`: Contém os scripts para geração das peças estruturais de madeira (ex: chapa base, paredes laterais).
- `pecas_impressas/`: Contém os scripts para as peças destinadas à impressão 3D (ex: suporte do motor).
- `pecas_mecanicas/`: Destinado a representações de componentes prontos (motores, parafusos, rodas).

## Como Executar

### Pré-requisitos
1. Ter o **Python** instalado.
2. Instalar as dependências: `pip install -r requirements.txt`.
3. No VS Code, instalar a extensão **OCP CAD Viewer**.

### Visualização
Para ver o chassi completo:
```bash
python main.py
```

Para visualizar uma peça individualmente, você pode executar o script da própria peça:
```bash
python pecas_madeira/chapa_base.py
```

## Convenções de Desenvolvimento

1. **Parametricidade:** Nunca utilize "magic numbers" diretamente nos scripts de peças. Sempre utilize ou derive valores a partir do `config.py`.
2. **Modularidade:** Cada peça deve estar em seu próprio arquivo dentro da pasta correspondente e possuir uma função principal `criar_<nome_da_peca>()` que retorna um objeto `Part` ou `Compound`.
3. **Visualização Local:** Todo script de peça deve conter um bloco `if __name__ == "__main__":` para permitir a visualização isolada da peça durante o desenvolvimento.
4. **Idioma:** O código e os comentários seguem o padrão em Português do Brasil (PT-BR), conforme estabelecido no início do projeto.
5. **Estilo build123d:** Prefira o uso de contextos (`with BuildPart() as ...`, `with BuildSketch() ...`) para manter o código declarativo e legível.
arativo e legível.
