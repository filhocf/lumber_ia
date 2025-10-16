# ia_avancada.py - IA Generativa com Persistência Completa

import subprocess
import time
import os
import json
import base64
import requests
import pickle
from datetime import datetime
from PIL import Image
import cv2
import numpy as np
from typing import Optional, Dict, List, Tuple

class LumberAIAvancada:
    def __init__(self, device_id: Optional[str] = None, ollama_url: str = "http://localhost:11434"):
        self.device_id = device_id
        self.ollama_url = ollama_url
        
        # Arquivos de persistência
        self.persistence_files = {
            'game_state': 'ai_game_state.json',
            'decision_history': 'ai_decision_history.json', 
            'learned_strategies': 'ai_strategies.pkl',
            'performance_metrics': 'ai_performance.json'
        }
        
        # Modelos Ollama
        self.models = {
            'vision': 'llava:7b',
            'reasoning': 'mistral:7b', 
            'planning': 'codellama:13b'
        }
        
        # Carregar conhecimento anterior
        self.game_state = self.load_game_state()
        self.decision_history = self.load_decision_history()
        self.learned_strategies = self.load_learned_strategies()
        
        print(f"🧠 IA Avançada Inicializada")
        print(f"📚 {len(self.decision_history)} decisões históricas carregadas")
        print(f"🎯 {len(self.learned_strategies['successful_patterns'])} estratégias aprendidas")
        
        self.check_ollama_connection()

    # ========== SISTEMA DE PERSISTÊNCIA ==========
    
    def load_game_state(self) -> Dict:
        """Carrega estado do jogo salvo"""
        try:
            if os.path.exists(self.persistence_files['game_state']):
                with open(self.persistence_files['game_state'], 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"❌ Erro ao carregar estado: {e}")
        
        return {
            'current_strategy': 'collect_resources',
            'total_cycles': 0,
            'successful_actions': 0,
            'last_session': datetime.now().isoformat(),
            'session_count': 0
        }
    
    def save_game_state(self):
        """Salva estado atual do jogo"""
        try:
            self.game_state['last_session'] = datetime.now().isoformat()
            self.game_state['session_count'] += 1
            with open(self.persistence_files['game_state'], 'w') as f:
                json.dump(self.game_state, f, indent=2)
        except Exception as e:
            print(f"❌ Erro ao salvar estado: {e}")
    
    def load_decision_history(self) -> List[Dict]:
        """Carrega histórico de decisões"""
        try:
            if os.path.exists(self.persistence_files['decision_history']):
                with open(self.persistence_files['decision_history'], 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return []
    
    def save_decision_history(self):
        """Salva histórico de decisões"""
        try:
            # Mantém apenas decisões recentes
            if len(self.decision_history) > 1000:
                self.decision_history = self.decision_history[-1000:]
            
            with open(self.persistence_files['decision_history'], 'w') as f:
                json.dump(self.decision_history, f, indent=2)
        except Exception as e:
            print(f"❌ Erro ao salvar histórico: {e}")
    
    def load_learned_strategies(self) -> Dict:
        """Carrega estratégias aprendidas"""
        try:
            if os.path.exists(self.persistence_files['learned_strategies']):
                with open(self.persistence_files['learned_strategies'], 'rb') as f:
                    return pickle.load(f)
        except Exception:
            pass
        return {
            'successful_patterns': {},
            'coordinate_effectiveness': {},
            'strategy_performance': {}
        }
    
    def save_learned_strategies(self):
        """Salva estratégias aprendidas"""
        try:
            with open(self.persistence_files['learned_strategies'], 'wb') as f:
                pickle.dump(self.learned_strategies, f)
        except Exception as e:
            print(f"❌ Erro ao salvar estratégias: {e}")

    # ========== APRENDIZADO PERSISTENTE ==========
    
    def update_learned_strategies(self, action_result: bool, action_data: Dict):
        """Atualiza estratégias baseadas no resultado"""
        action_type = action_data.get('action', 'unknown')
        coordinates = action_data.get('coordinates', (0, 0))
        
        # Atualiza padrões de sucesso
        if action_type not in self.learned_strategies['successful_patterns']:
            self.learned_strategies['successful_patterns'][action_type] = {
                'success_count': 0,
                'total_count': 0,
                'success_rate': 0.0
            }
        
        pattern = self.learned_strategies['successful_patterns'][action_type]
        pattern['total_count'] += 1
        if action_result:
            pattern['success_count'] += 1
        pattern['success_rate'] = pattern['success_count'] / pattern['total_count']
        
        # Atualiza efetividade de coordenadas
        coord_key = f"{coordinates[0]}_{coordinates[1]}"
        if coord_key not in self.learned_strategies['coordinate_effectiveness']:
            self.learned_strategies['coordinate_effectiveness'][coord_key] = {
                'success_count': 0,
                'total_count': 0,
                'last_used': datetime.now().isoformat()
            }
        
        coord_data = self.learned_strategies['coordinate_effectiveness'][coord_key]
        coord_data['total_count'] += 1
        if action_result:
            coord_data['success_count'] += 1
        coord_data['last_used'] = datetime.now().isoformat()
    
    def choose_best_action(self, actions: List[Dict]) -> Dict:
        """Escolhe melhor ação baseada no aprendizado"""
        if len(actions) == 1:
            return actions[0]
        
        scored_actions = []
        for action in actions:
            score = 1.0
            action_type = action.get('action', 'unknown')
            coordinates = action.get('coordinates', {})
            
            # Ajusta score baseado em histórico
            if action_type in self.learned_strategies['successful_patterns']:
                pattern = self.learned_strategies['successful_patterns'][action_type]
                score *= (1.0 + pattern['success_rate'])
            
            # Ajusta score baseado em coordenadas
            if coordinates:
                coord_key = f"{coordinates.get('x', 0)}_{coordinates.get('y', 0)}"
                if coord_key in self.learned_strategies['coordinate_effectiveness']:
                    coord_data = self.learned_strategies['coordinate_effectiveness'][coord_key]
                    score *= (1.0 + (coord_data['success_count'] / max(1, coord_data['total_count'])))
            
            scored_actions.append((score, action))
        
        return max(scored_actions, key=lambda x: x[0])[1]

    # ========== MÉTODOS PRINCIPAIS ==========
    
    def capture_screen(self, output_path: str = "current_screen.png") -> Optional[Image.Image]:
        """Captura tela do dispositivo"""
        try:
            command = f"exec-out screencap -p"
            if self.device_id:
                command = f"-s {self.device_id} {command}"
            
            result = subprocess.run(f"adb {command}", shell=True, capture_output=True)
            
            if result.returncode == 0:
                with open(output_path, 'wb') as f:
                    f.write(result.stdout)
                return Image.open(output_path)
            else:
                print("Erro ao capturar tela")
                return None
        except Exception as e:
            print(f"Erro na captura de tela: {e}")
            return None
    
    def image_to_base64(self, image_path: str) -> str:
        """Converte imagem para base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def analyze_screen_with_ai(self, image_path: str) -> Dict:
        """Analisa tela usando IA generativa"""
        print(f"🔍 Iniciando análise da tela: {image_path}")
        try:
            image_base64 = self.image_to_base64(image_path)
            print("✅ Imagem convertida para base64")
            
            prompt = """
            Analise esta tela do jogo Lumber Inc. e identifique elementos interativos.
            Responda em JSON com: elementos visíveis, estado do jogo e ações recomendadas.
            """
            
            payload = {
                "model": self.models['vision'],
                "prompt": prompt,
                "images": [image_base64],
                "stream": False
            }
            
            print(f"🤖 Enviando para modelo: {self.models['vision']}")
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Resposta recebida do Ollama")
                analysis = json.loads(result['response'])
                print(f"📊 Análise completada: {len(analysis.get('elements', []))} elementos detectados")
                return analysis
            else:
                print(f"❌ Erro na análise: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Erro na análise generativa: {e}")
            return {}

    def tap(self, x: int, y: int) -> bool:
        """Executa toque na coordenada"""
        try:
            command = f"shell input tap {x} {y}"
            if self.device_id:
                command = f"-s {self.device_id} {command}"
            
            subprocess.run(f"adb {command}", shell=True)
            print(f"👆 Toque em ({x}, {y})")
            return True
        except Exception as e:
            print(f"Erro ao executar toque: {e}")
            return False
    
    def execute_ai_decision(self, analysis: Dict) -> bool:
        """Executa decisões da IA com aprendizado"""
        if not analysis:
            print("❌ Nenhuma análise disponível")
            return False
            
        if 'recommended_actions' not in analysis:
            print("❌ Nenhuma ação recomendada na análise")
            return False
        
        actions = analysis['recommended_actions']
        if not actions:
            print("⚠️ Lista de ações vazia")
            return False
        
        print(f"🎯 {len(actions)} ações recomendadas disponíveis")
        
        # Escolhe ação considerando aprendizado
        best_action = self.choose_best_action(actions)
        coordinates = best_action.get('coordinates', {})
        
        if coordinates:
            x = coordinates.get('x', 0)
            y = coordinates.get('y', 0)
            if x > 0 and y > 0:
                print(f"🎯 Executando ação: {best_action.get('action', 'unknown')} em ({x}, {y})")
                print(f"📝 Razão: {best_action.get('reason', 'N/A')}")
                
                success = self.tap(x, y)
                
                # Registra decisão
                decision = {
                    'timestamp': datetime.now().isoformat(),
                    'action': best_action.get('action', 'unknown'),
                    'coordinates': (x, y),
                    'reason': best_action.get('reason', ''),
                    'result': 'success' if success else 'unknown'
                }
                self.decision_history.append(decision)
                
                # Atualiza aprendizado
                self.update_learned_strategies(success, decision)
                self.game_state['total_cycles'] += 1
                if success:
                    self.game_state['successful_actions'] += 1
                
                # Salva periodicamente
                if self.game_state['total_cycles'] % 10 == 0:
                    self.save_all_data()
                
                return success
        else:
            print("❌ Coordenadas inválidas na ação")
        
        return False
    
    def save_all_data(self):
        """Salva todos os dados"""
        self.save_game_state()
        self.save_decision_history()
        self.save_learned_strategies()
        print("💾 Dados salvos!")
    
    def check_ollama_connection(self):
        """Verifica conexão com Ollama"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                print("✅ Ollama conectado!")
                return True
            else:
                print("❌ Ollama não responde")
                return False
        except Exception as e:
            print(f"❌ Erro Ollama: {e}")
            return False
    
    def gameplay_autonomo(self, duration_minutes: int = 30):
        """Loop de gameplay autônomo"""
        print(f"🤖 Iniciando gameplay autônomo por {duration_minutes} minutos...")
        print(f"🧠 Modelos configurados: {self.models}")
        print(f"📚 Dados carregados: {len(self.decision_history)} decisões históricas")
        
        end_time = time.time() + (duration_minutes * 60)
        cycles = 0
        
        try:
            while time.time() < end_time:
                cycles += 1
                print(f"\n=== CICLO {cycles} ===")
                
                # 1. Captura e analisa
                print("📱 Capturando tela...")
                screen = self.capture_screen("ai_screen.png")
                if not screen:
                    print("❌ Falha ao capturar tela, aguardando 5s...")
                    time.sleep(5)
                    continue
                print("✅ Tela capturada com sucesso")
                
                # 2. Análise generativa
                print("🔍 Iniciando análise com IA...")
                analysis = self.analyze_screen_with_ai("ai_screen.png")
                if analysis:
                    print("✅ Análise processada, executando decisão...")
                    executed = self.execute_ai_decision(analysis)
                    if executed:
                        print("✅ Ação executada com sucesso")
                    else:
                        print("⚠️ Nenhuma ação executada")
                else:
                    print("❌ Falha na análise da tela")
                
                # 3. Mostra status periódico
                if cycles % 5 == 0:
                    print(f"\n📈 STATUS INTERMEDIÁRIO - Ciclo {cycles}")
                    print(f"🔄 Total de ciclos: {self.game_state['total_cycles']}")
                    print(f"✅ Ações bem-sucedidas: {self.game_state['successful_actions']}")
                    if self.game_state['total_cycles'] > 0:
                        success_rate = (self.game_state['successful_actions'] / self.game_state['total_cycles']) * 100
                        print(f"📊 Taxa de sucesso: {success_rate:.1f}%")
                
                print(f"⏰ Aguardando próximo ciclo (8s)...")
                time.sleep(8)
                
        except KeyboardInterrupt:
            print("\n⏹️ Interrompido pelo usuário")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
        finally:
            print("\n💾 Salvando dados finais...")
            self.save_all_data()
            print(f"✅ Finalizado. {cycles} ciclos executados.")
    
    def mostrar_resumo(self):
        """Mostra resumo do aprendizado"""
        print("\n📊 RESUMO DO APRENDIZADO:")
        print(f"Sessões: {self.game_state['session_count']}")
        print(f"Ciclos totais: {self.game_state['total_cycles']}")
        print(f"Ações bem-sucedidas: {self.game_state['successful_actions']}")
        success_rate = (self.game_state['successful_actions'] / max(1, self.game_state['total_cycles'])) * 100
        print(f"Taxa de sucesso: {success_rate:.1f}%")
        print(f"Padrões aprendidos: {len(self.learned_strategies['successful_patterns'])}")

def main():
    # Verificar ADB
    result = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
    if "device" not in result.stdout:
        print("❌ Nenhum dispositivo Android!")
        return
    
    ai = LumberAIAvancada()
    
    print("🧠 IA Avançada para Lumber Inc.")
    print("1 - Gameplay Autônomo (IA aprende e lembra)")
    print("2 - Ver Resumo do Aprendizado")
    print("3 - Verificar Ollama")
    
    choice = input("\nEscolha: ")
    
    if choice == "1":
        duration = input("Duração (minutos, padrão 30): ")
        try:
            duration = int(duration) if duration else 30
        except ValueError:
            duration = 30
        ai.gameplay_autonomo(duration)
    
    elif choice == "2":
        ai.mostrar_resumo()
    
    elif choice == "3":
        ai.check_ollama_connection()
    
    else:
        print("❌ Opção inválida")

if __name__ == "__main__":
    main()