# Robô de Inspeção - Projeto CAD Paramétrico

Este projeto consiste na modelagem CAD paramétrica do **Robô de Inspeção** sobre esteiras de borracha de pneu MTB utilizando a biblioteca **build123d** em Python. A estrutura do robô é composta por casco monobloco ("banheira") e carenagem stealth em PETG, esteiras com cravos 3D e componentes comerciais integrados via modelos STEP e padronizados.

## Tecnologias e Dependências

- **Linguagem:** Python 3.x
- **Core CAD:** [build123d](https://github.com/gumyr/build123d)
- **Visualização:** [ocp_vscode](https://github.com/bernhard-42/vscode-ocp-cad-viewer) (OCP CAD Viewer no VS Code)
- **Modelos Comerciais:** Arquivos STEP normalizados em `modelos_cad/`

## Estrutura do Projeto

- `main.py`: Ponto de entrada principal que inicializa e exibe a montagem dos 6 subsistemas no OCP CAD Viewer.
- `config.py`: Dimensões globais, parâmetros estruturais, tolerâncias FDM e paleta de cores didática de engenharia.
- `medidas.py`: Parâmetros de furação, variáveis calculadas e tolerâncias de montagem.
- `montagem.py`: Orquestra a composição espacial e cinemática dos 6 subsistemas (carenagem, chassi, bandeja, eletrônica e trens de rodagem).
- `pinagem_eletronica.py`: Mapeamento elétrico oficial ESP32-CAM -> Ponte H L298N e especificações de alimentação.
- `modelos_cad/`: Modelos CAD industriais em formato STEP para os componentes comerciais padronizados:
  - `rolamento_608zz.step`: Rolamento industrial 608-ZZ com pistas e blindagens
  - `flange_acoplamento_6mm.step`: Flange de acoplamento rígido de alumínio de 6mm
  - `motor_jgb37_520.step`: Motorredutor 12V JGB37-520 com redução e eixo D
  - `ponte_h_l298n.step`: Driver de motores de potência L298N completo
  - `step_down_lm2596_hw411.step`: Módulo conversor DC-DC regulador de 5V
- `pecas_impressas/`: Componentes estruturais destinados à manufatura aditiva (PETG):
  - `chassi_banheira.py`: Casco inferior monobloco (240x160x75mm) com glacis frontal a 45°, cantos inferiores arredondados, grelhas e aletas defletoras
  - `tampa_superior.py`: Carenagem stealth chanfrada com Cooler Fan Rise Mode 80mm, Suporte Articulado Tilt (55x38x25mm) e painel externo
  - `roda_motriz.py`: Polia motriz maciça traseira de Ø60mm com abas guia altas de 12mm e rebaixo para flange de alumínio
  - `roda_livre.py`: Polias livres centrais e dianteiras de Ø50mm com abas guia altas de 12mm e cavidade para 2x rolamentos 608-ZZ
  - `suporte_eletronica.py`: Bandeja interna com berço central geométrico (70x58x12mm) para pack 3S 18650 e alívios
- `pecas_mecanicas/`: Componentes mecânicos, cinemáticos e circuitos:
  - `conjunto_eixo_rolamento.py`: Centro de fixação com rolamentos 608-ZZ, arruela funileiro M8 e porca sextavada M8
  - `flange_aluminio.py`: Acoplamento de torque 6mm em alumínio (22x4mm)
  - `motor_jgb37_520.py`: Motorredutor JGB37-520 integrado
  - `esteira_pneu_mtb.py`: Cinta contínua oca de borracha com cravos 3D e placa de união em alumínio
  - `eletronica.py`: Conjunto embarcado (L298N, LM2596, ESP32-CAM e bateria 3S 18650)
- `exportacoes/`: Destinado a arquivos exportados (.STL para fatiamento 3D e .STEP para usinagem).

## Como Executar

### Pré-requisitos
1. Ter o **Python** instalado.
2. Instalar as dependências: `pip install -r requirements.txt`.
3. No VS Code, ter a extensão **OCP CAD Viewer** instalada e ativa.

### Visualização
Para visualizar o robô completo com os 6 subsistemas:
```bash
python main.py
```

Para visualizar uma peça individualmente durante o desenvolvimento:
```bash
python pecas_impressas/chassi_banheira.py
```

## Convenções de Desenvolvimento

1. **Parametricidade:** Nunca utilize "magic numbers" diretamente nos scripts de peças. Sempre utilize ou derive valores a partir do `config.py`.
2. **Modularidade:** Cada peça deve estar em seu próprio arquivo dentro da pasta correspondente e possuir uma função principal `criar_<nome_da_peca>()` que retorna um objeto `Part` ou `Compound`.
3. **Visualização Local:** Todo script de peça deve conter um bloco `if __name__ == "__main__":` para permitir a visualização isolada da peça durante o desenvolvimento.
4. **Idioma:** O código e os comentários seguem o padrão em Português do Brasil (PT-BR).
5. **Estilo build123d:** Prefira o uso de contextos (`with BuildPart() as ...`, `with BuildSketch() ...`) para manter o código declarativo, limpo e legível.
