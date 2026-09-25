# Robô de Inspeção sobre Esteiras de Pneu MTB

Projeto de Engenharia Mecatrônica para modelagem CAD paramétrica e procedural de um **Robô de Inspeção** para áreas confinadas e terrenos industriais hostis (atendendo às normas NR-10 e NR-33), construído inteiramente em **Python** utilizando o kernel paramétrico [build123d](https://github.com/gumyr/build123d) e visualizado interativamente com o [OCP CAD Viewer](https://github.com/bernhard-42/vscode-ocp-cad-viewer).

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
├── exportar_pecas.py           # Script para exportação automatizada (.STL / .STEP)
├── modelos_cad/                # Modelos CAD oficiais em STEP dos componentes industriais
│   ├── rolamento_608zz.step    # Rolamento de esferas 608-ZZ com pistas e blindagens
│   ├── flange_acoplamento_6mm.step # Flange de alumínio 6mm com parafusos prisioneiros M3
│   ├── motor_jgb37_520.step    # Motorredutor 12V DC com redução e eixo D
│   ├── ponte_h_l298n.step      # Driver Ponte H L298N completo
│   └── step_down_lm2596_hw411.step # Módulo regulador DC-DC HW-411
├── pecas_impressas/            # Peças estruturais para manufatura aditiva (PETG)
│   ├── chassi_banheira.py      # Casco monobloco 240x160x75mm com glacis a 45°, cantos arredondados, grelhas e aletas
│   ├── tampa_superior.py       # Carenagem stealth com Cooler Fan Rise Mode 80mm, Suporte Tilt e Painel
│   ├── roda_motriz.py          # Polia motriz maciça Ø60mm com abas altas de 12mm e rebaixo para flange
│   ├── roda_livre.py           # Polias livres Ø50mm com abas altas de 12mm e alojamento duplo 608-ZZ
│   └── suporte_eletronica.py   # Bandeja interna removível com berço central para pack 3S 18650
└── pecas_mecanicas/            # Integração cinemática e circuitos
    ├── conjunto_eixo_rolamento.py # Centro de fixação da roda com rolamentos 608-ZZ e porca M8
    ├── flange_aluminio.py      # Flange metálico usinado Ø22x4mm (eixo 6mm -> M3)
    ├── motor_jgb37_520.py      # Motorredutor JGB37-520 integrado
    ├── esteira_pneu_mtb.py     # Cinta contínua oca de borracha com cravos 3D e placa de união
    └── eletronica.py           # Módulos eletrônicos (L298N, LM2596, ESP32-CAM e bateria 3S)
```

---

## 2. Especificação Elétrica e Pinagem

### Topologia de Alimentação
1. **Fonte Primária:** Pack 3S Li-Ion 18650 (11.1V nominal ~ 12.6V pico) posicionado no centro geométrico da bandeja para equilíbrio de CG.
2. **Barramento de Potência dos Motores:** Alimentação direta no borne **VMS (12V)** da Ponte H L298N.
3. **Barramento de Lógica do Microcontrolador:** Bateria 3S ligada à entrada do **Step-Down LM2596**, reduzida para **5.0V estáveis** dedicados ao pino `5V` do ESP32-CAM.
4. **Referência Comum:** GND unificado em estrela (Bateria, LM2596, ESP32-CAM e L298N).

> [!WARNING]
> O jumper de 5V do L298N deve ser desconectado se a tensão de entrada passar de 12V para proteger o regulador 78M05 interno. **Nunca alimente o ESP32-CAM pela saída 5V do L298N**, pois os surtos de corrente do rádio Wi-Fi (até 500mA) provocam quedas de tensão e *brownout reset* no microcontrolador.

### Pinagem Oficial ESP32-CAM $\rightarrow$ Ponte H L298N

| Sinal | Pino ESP32-CAM | Pino L298N | Função Mecatrônica |
| :--- | :---: | :---: | :--- |
| **Motor Esquerdo** | | | |
| `ENA` | **GPIO 14** | `ENA` | Sinal PWM de modulação de velocidade |
| `IN1` | **GPIO 12** | `IN1` | Controle de direção (Frente / Horário) |
| `IN2` | **GPIO 13** | `IN2` | Controle de direção (Ré / Anti-horário) |
| **Motor Direito** | | | |
| `ENB` | **GPIO 15** | `ENB` | Sinal PWM de modulação de velocidade |
| `IN3` | **GPIO 2** | `IN3` | Controle de direção (Frente / Horário) |
| `IN4` | **GPIO 4** | `IN4` | Controle de direção (Ré / Flash LED) |

---

## 3. Gestão Térmica e Módulo de Sensores

- **Cooler Fan Rise Mode 80mm:** Montado sob a tampa superior com recorte de Ø 75 mm e 4 furos M4 em quadrado de 71,5 x 71,5 mm, protegido por grelha integrada impressa em 3D.
- **Ventilação Cruzada:** Glacis frontal com grelhas inclinadas e aletas defletoras traseiras voltadas para baixo a 30° para expulsão passiva de ar quente protegendo contra poeira e respingos d'água.
- **Módulo Frontal Articulado Tilt (55 x 38 x 25 mm):**
  - Janela quadrada de 10 x 10 mm para câmera OV2640 (ESP32-CAM).
  - Alojamento para Sensor Térmico sem contato MLX90614 (Ø 10,2 mm).
  - 2x Faróis auxiliares Olho de Águia 12V (Ø 10,2 mm / rosca M10).
- **Painel Externo de Controle:**
  - Chave gangorra liga/desliga KCD1 iluminada (19,2 x 13,0 mm).
  - Mini voltímetro digital LED DC 0-30V (22,5 x 14,0 mm).
  - Buzzer ativo 5V (Ø 12 mm) e LED difuso vermelho 5mm de alarme térmico.
  - Conector para antena articulada SMA 2.4 GHz de 5 dBi (Ø 6,5 mm).

---

## 4. Como Executar e Visualizar

Execute o script principal:
```bash
python main.py
```
O modelo completo com seus 6 subsistemas hierárquicos e didáticos será carregado na extensão **OCP CAD Viewer** no VS Code.
