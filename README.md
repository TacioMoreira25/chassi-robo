# Chassi Robô UGV - Creative Home Tank

Este é o projeto de modelagem 3D paramétrica e procedural de um chassi de robô com esteiras, inteiramente codificado em Python utilizando a biblioteca build123d. O chassi é baseado num tanque UGV caseiro de compensado 12mm e catracas de bicicleta (18T).

## Estrutura do Projeto

O modelo é modular para facilitar a edição e fabricação paramétrica:

- `main.py`: Script principal que compila todo o projeto e o renderiza.
- `montagem.py`: Une todas as sub-peças (madeiras, motores, catracas e eixos).
- `config.py`: Variáveis e medidas globais do chassi (comprimentos e espessuras).
- `pecas_madeira/`: Modelos das chapas de compensado 12mm (Base, Paredes laterais em trapézio e travessas).
- `pecas_mecanicas/`: Mockups das peças de hardware (Motores Johnson, Catracas 18T, Parafusos M8x75mm, Arruelas, Porcas e Rolamentos).

## Pré-Requisitos

- Python 3.9+ instalado.
- Recomendável uso de ambiente virtual (venv).

Instale as dependências:
```bash
pip install -r requirements.txt
```
## Como Executar e Visualizar

A forma mais prática de visualizar a modelagem 3D é executar o servidor web do OCP CAD Viewer localmente em segundo plano e acessar pelo navegador.

1. No terminal da pasta do projeto, inicie o servidor do OCP Viewer:
```bash
python -m ocp_vscode &
```

2. Em seguida, compile o modelo principal do chassi rodando:
```bash
python main.py
```

3. Abra o seu navegador e acesse o endereço fornecido no terminal (geralmente `http://127.0.0.1:3939`). A estrutura completa do robô UGV será exibida.

## Personalização Paramétrica

Todas as medidas do robô estão unificadas nos arquivos de configuração:
- `config.py`: Altere "COMP_TOTAL" ou "ESPESSURA_MADEIRA" para escalar o chassi inteiro.
- A furação e os eixos recalcularão automaticamente de forma procedural.
