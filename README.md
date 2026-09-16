# The Iron Vanguard - UGV de Inspeção sobre Esteiras de Pneu

Projeto de Engenharia Mecatrônica para modelagem CAD paramétrica e procedural de um **UGV (Veículo Terrestre Não Tripulado)** para inspeção em áreas confinadas e terrenos hostis, construído inteiramente em **Python** utilizando o kernel paramétrico [build123d](https://github.com/gumyr/build123d) e visualizado interativamente com o [OCP CAD Viewer](https://github.com/bernhard-42/vscode-ocp-cad-viewer).

---

## 1. Visão Geral da Arquitetura

O sistema é modular, totalmente desacoplado e 100% paramétrico:

```
chassi-robo/
├── main.py                     # Montagem global e renderização no OCP CAD Viewer
├── config.py                   # Dimensões estruturais, tolerâncias FDM e paleta de cores
├── medidas.py                  # Medidas derivadas, cálculos de offsets e dados de montagem
├── montagem.py                 # Orquestrador da montagem dos 6 subsistemas
├── pinagem_eletronica.py       # Especificação técnica de pinagem e arquitetura elétrica
├── iron_vanguard_cad.py        # Script monolítico com exportação STL/STEP
├── modelos_cad/                # Modelos CAD oficiais em STEP dos componentes industriais
│   ├── rolamento_608zz.step    # Rolamento de esferas 608-ZZ com pistas e blindagens
│   ├── flange_acoplamento_6mm.step # Flange de alumínio 6mm com parafusos prisioneiros M3
│   ├── motor_jgb37_520.step    # Motorredutor 12V DC com redução e eixo D
│   ├── ponte_h_l298n.step      # Driver Ponte H L298N completo
│   └── step_down_lm2596_hw411.step # Módulo regulador DC-DC HW-411
├── pecas_impressas/            # Peças estruturais para manufatura aditiva (PETG)
│   ├── chassi_banheira.py      # Casco estanque monobloco com glacis frontal a 45° e grelhas
│   ├── tampa_superior.py       # Carenagem stealth chanfrada com torre FPV frontal integrada
│   ├── roda_motriz.py          # Roda motriz de 5 raios com rebaixo para flange de alumínio
│   ├── roda_livre.py           # Roda côncava (deep dish) com alojamento para rolamentos 608-ZZ
│   └── suporte_eletronica.py   # Bandeja interna removível com alívios para motores
└── pecas_mecanicas/            # Integração cinemática e circuitos
    ├── conjunto_eixo_rolamento.py # Centro de fixação da roda com rolamento 608-ZZ e porca M8
    ├── flange_aluminio.py      # Flange metálico usinado Ø22x4mm (eixo 6mm -> M3)
    ├── motor_jgb37_520.py      # Motorredutor JGB37-520 integrado
    ├── esteira_pneu_mtb.py     # Cinta contínua oca de borracha com cravos 3D e placa de união
    └── eletronica.py           # Módulos eletrônicos (L298N, LM2596, ESP32-CAM e bateria 3S)
```

---

## 2. Especificação Elétrica e Pinagem

### Topologia de Alimentação
1. **Fonte Primária:** Pack 3S Li-Ion 18650 (11.1V nominal ~ 12.6V pico).
2. **Barramento de Potência dos Motores:** Alimentação direta no borne **VMS (12V)** da Ponte H L298N.
3. **Barramento de Lógica do Microcontrolador:** Bateria 3S ligada à entrada do **Step-Down LM2596**, reduzida para **5.0V estáveis** dedicados ao pino `5V` do ESP32-CAM.
4. **Referência Comum:** GND unificado em estrela (Bateria, LM2596, ESP32-CAM e L298N).

> [!WARNING]
> O jumper de 5V do L298N deve ser desconectado se a tensão de entrada passar de 12V para proteger o 78M05 interno. **Nunca alimente o ESP32-CAM pela saída 5V do L298N**, pois os surtos de corrente do rádio Wi-Fi (até 500mA) provocam quedas de tensão e *brownout reset* contínuo no ESP32.

### Pinagem ESP32-CAM $\rightarrow$ Ponte H L298N

| Sinal | Pino ESP32-CAM | Pino L298N | Função Mecatrônica |
| :--- | :---: | :---: | :--- |
| **Motor Esquerdo** | | | |
| `ENA` | **GPIO 14** | `ENA` | Sinal PWM de modulação de velocidade |
| `IN1` | **GPIO 12** | `IN1` | Controle de direção (Frente / Horário) |
| `IN2` | **GPIO 13** | `IN2` | Controle de direção (Ré / Anti-horário) |
| **Motor Direito** | | | |
| `ENB` | **GPIO 15** | `ENB` | Sinal PWM de modulação de velocidade |
| `IN3` | **GPIO 2**  | `IN3` | Controle de direção (Frente / Horário) |
| `IN4` | **GPIO 4**  | `IN4` | Controle de direção (Ré / Anti-horário) *(Atenção: GPIO 4 aciona o Flash LED)* |

---

## 3. Como Executar e Visualizar no OCP CAD Viewer

### Visualizar o Robô Completo
1. Abra o VS Code com a extensão **OCP CAD Viewer** instalada e ativada.
2. No terminal do projeto, execute:
   ```bash
   python main.py
   ```

3. No painel lateral do **OCP CAD Viewer**, explore a árvore hierárquica (1 a 6) para habilitar/desabilitar cada subsistema (carenagem, chassi, bandeja, eletrônica, trens de rodagem esquerdo e direito).

### Visualizar Peças Individualmente
Cada arquivo dentro de `pecas_impressas/` e `pecas_mecanicas/` possui execução autônoma didática:

```bash
# Roda Motriz Raiada (5 raios)
python pecas_impressas/roda_motriz.py

# Roda Livre Côncava com alojamento 608-ZZ
python pecas_impressas/roda_livre.py

# Chassi tipo Banheira com Glacis e Grelhas
python pecas_impressas/chassi_banheira.py

# Carenagem Superior Stealth com Torre FPV
python pecas_impressas/tampa_superior.py

# Bandeja de suporte da eletrônica
python pecas_impressas/suporte_eletronica.py

# Esteira Oca com Cravos 3D e Placa de Emenda
python pecas_mecanicas/esteira_pneu_mtb.py

# Motorredutor JGB37-520 integrado
python pecas_mecanicas/motor_jgb37_520.py

# Visualização da pinagem e conexões
python pinagem_eletronica.py
```

### Exportar STL e STEP para Manufatura
Para gerar os arquivos para o fatiador (Cura, PrusaSlicer, OrcaSlicer) e CAD:
```bash
python iron_vanguard_cad.py
```
Os arquivos serão gerados na pasta `./exportacoes/`:
- `chassi_banheira_ugv.stl` / `.step`
- `carenagem_superior_stealth.stl` / `.step`
- `roda_motriz_raiada.stl` / `.step`
- `roda_livre_concava.stl` / `.step`
- `suporte_interna_eletronica.stl` / `.step`

---

## 4. Recomendações de Manufatura Aditiva (FDM / PETG)

- **Filamento:** PETG (alta resistência ao impacto e flexão sob esforço das esteiras).
- **Polia Motriz e Livre:**
  - Perímetros: 4 a 5 paredes sólidas.
  - Preenchimento (Infill): $\ge$ 40% (Giroide ou Cúbico).
  - Orientação na Mesa: Face externa voltada para baixo.
- **Chassi Banheira:**
  - Perímetros: 4 paredes sólidas (espessura final 3.5mm sólida em bico 0.4mm com 8 loops ou bico 0.6mm).
  - Preenchimento: 30% Giroide.
- **Tolerâncias:**
  - Alojamento dos rolamentos 608-ZZ calibrado para $\varnothing 22.18\text{ mm}$ (compensando a contração do PETG para encaixe sob pressão firme).
