'''
IA Básica para Lumber Inc. - Versão Simplificada

Esta é uma IA baseada em regras fixas para testes rápidos.
Para a versão avançada com aprendizado, use ia_avancada.py
'''

import subprocess
import time
import os
from typing import Optional

class LumberIABasica:
    def __init__(self, device_id: Optional[str] = None):
        self.device_id = device_id
        
        # Coordenadas básicas (ajustar via calibrate.py)
        self.coordinates = {
            'collect_resources': (500, 1800),
            'upgrade_button': (800, 2000),
            'workshop_button': (300, 2000),
            'factory_button': (500, 2000),
        }
    
    def adb_command(self, command: str) -> str:
        '''Executa comando ADB'''
        if self.device_id:
            full_command = f'adb -s {self.device_id} {command}'
        else:
            full_command = f'adb {command}'
        
        try:
            result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            print(f'Erro ADB: {e}')
            return ''
    
    def tap(self, x: int, y: int) -> bool:
        '''Executa toque na coordenada'''
        try:
            self.adb_command(f'shell input tap {x} {y}')
            print(f'👆 Toque em ({x}, {y})')
            return True
        except Exception as e:
            print(f'Erro toque: {e}')
            return False
    
    def coletar_recursos(self) -> bool:
        '''Coleta recursos disponíveis'''
        print('Coletando recursos...')
        return self.tap(*self.coordinates['collect_resources'])
    
    def verificar_upgrades(self) -> bool:
        '''Verifica e executa upgrades'''
        print('Verificando upgrades...')
        return self.tap(*self.coordinates['upgrade_button'])
    
    def navegar_oficina(self) -> bool:
        '''Navega para oficina'''
        print('Navegando para oficina...')
        return self.tap(*self.coordinates['workshop_button'])
    
    def navegar_fabrica(self) -> bool:
        '''Navega para fábrica'''
        print('Navegando para fábrica...')
        return self.tap(*self.coordinates['factory_button'])
    
    def loop_principal(self, duracao_minutos: int = 10):
        '''Loop principal simples'''
        print(f'🤖 IA Básica iniciada por {duracao_minutos} minutos...')
        
        fim = time.time() + (duracao_minutos * 60)
        ciclos = 0
        
        try:
            while time.time() < fim:
                ciclos += 1
                print(f'🔄 Ciclo {ciclos}')
                
                # Sequência básica de ações
                self.coletar_recursos()
                self.verificar_upgrades()
                
                # Alterna entre áreas periodicamente
                if ciclos % 5 == 0:
                    self.navegar_oficina()
                    time.sleep(1)
                    self.navegar_fabrica()
                
                time.sleep(3)
                
        except KeyboardInterrupt:
            print('\\n⏹️ Parado pelo usuário')
        
        print(f'✅ Finalizado. {ciclos} ciclos executados.')

def main():
    # Verificar ADB
    result = subprocess.run('adb devices', shell=True, capture_output=True, text=True)
    if 'device' not in result.stdout:
        print('❌ Nenhum dispositivo Android!')
        return
    
    ai = LumberIABasica()
    
    print('🤖 IA Básica para Lumber Inc.')
    print('1 - Executar IA Básica (10 min)')
    print('2 - Executar IA Básica (30 min)')
    
    escolha = input('\\nEscolha: ')
    
    if escolha == '1':
        ai.loop_principal(10)
    elif escolha == '2':
        ai.loop_principal(30)
    else:
        print('❌ Opção inválida')

if __name__ == '__main__':
    main()