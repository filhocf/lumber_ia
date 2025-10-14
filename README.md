# IA para Lumber Inc. - Android Físico

Este projeto implementa uma IA para automatizar o jogo Lumber Inc. em dispositivos Android físicos.

## Pré-requisitos

- Dispositivo Android com depuração USB ativada
- Python 3.7+
- ADB (Android Debug Bridge)
- Jogo Lumber Inc. instalado

## Configuração

1. **Preparar o dispositivo Android:**
   - Ative "Opções do desenvolvedor"
   - Ative "Depuração USB"
   - Conecte via USB e autorize o computador

2. **Instalar dependências:**
   ```bash
   python setup.py
   ```

3. **Calibrar coordenadas (importante!):**
   ```bash
   python calibrate.py
   ```
   - Use as coordenadas obtidas para atualizar o arquivo `lumber_ai.py`

## Uso

Execute a IA:
```bash
python lumber_ai.py
```

## Estrutura do Projeto

- `lumber_ai.py` - IA principal
- `config.py` - Configurações
- `setup.py` - Script de setup
- `calibrate.py` - Calibração de coordenadas
- `templates/` - Imagens para reconhecimento
- `screenshots/` - Capturas de tela
- `logs/` - Logs de execução

## Funcionalidades

- Coleta automática de recursos
- Verificação e execução de upgrades
- Navegação entre áreas do jogo
- Detecção e fechamento de anúncios
- Reconhecimento de imagem para elementos visuais

## Personalização

Edite `config.py` para ajustar:
- Resolução da tela
- Intervalos de tempo
- Threshold de reconhecimento
- Caminhos dos templates

## Segurança

- Não compartilhe informações pessoais
- Use apenas em seu próprio dispositivo
- Respeite os termos de serviço do jogo