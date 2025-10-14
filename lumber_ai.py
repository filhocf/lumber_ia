import subprocess
import time
import os
from PIL import Image
import cv2
import numpy as np
from typing import Optional, Tuple, List

class LumberIncAI:
    def __init__(self, device_id: Optional[str] = None):
        self.device_id = device_id
        self.screen_width = 1080  # Ajustar conforme resolução do dispositivo
        self.screen_height = 2340  # Ajustar conforme resolução do dispositivo
        
        # Templates para reconhecimento de imagem (serão carregados posteriormente)
        self.templates = {}
        
        # Coordenadas de elementos importantes (ajustar conforme necessário)
        self.coordinates = {
            'collect_resources': (500, 1800),
            'upgrade_button': (800, 2000),
            'workshop_button': (300, 2000),
            'factory_button': (500, 2000),
        }
    
    def adb_command(self, command: str) -> str:
        """Executa comando ADB"""
        if self.device_id:
            full_command = f"adb -s {self.device_id} {command}"
        else:
            full_command = f"adb {command}"
        
        try:
            result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            print(f"Erro ao executar comando ADB: {e}")
            return ""
    
    def capture_screen(self, output_path: str = "screen.png") -> Optional[Image.Image]:
        """Captura a tela do dispositivo"""
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
    
    def tap(self, x: int, y: int) -> bool:
        """Executa toque na coordenada especificada"""
        try:
            self.adb_command(f"shell input tap {x} {y}")
            return True
        except Exception as e:
            print(f"Erro ao executar toque: {e}")
            return False
    
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 100) -> bool:
        """Executa swipe entre coordenadas"""
        try:
            self.adb_command(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")
            return True
        except Exception as e:
            print(f"Erro ao executar swipe: {e}")
            return False
    
    def find_template(self, template_path: str, threshold: float = 0.8) -> Optional[Tuple[int, int]]:
        """Encontra template na tela usando OpenCV"""
        try:
            # Captura tela atual
            screen = self.capture_screen("current_screen.png")
            if not screen:
                return None
            
            # Converte para OpenCV format
            screen_cv = cv2.imread("current_screen.png")
            template = cv2.imread(template_path)
            
            if screen_cv is None or template is None:
                print("Erro ao carregar imagens")
                return None
            
            # Realiza template matching
            result = cv2.matchTemplate(screen_cv, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= threshold:
                # Retorna coordenadas do centro do template
                h, w = template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                return (center_x, center_y)
            
            return None
        except Exception as e:
            print(f"Erro no reconhecimento de imagem: {e}")
            return None
    
    def collect_resources(self) -> bool:
        """Coleta recursos disponíveis"""
        print("Coletando recursos...")
        return self.tap(*self.coordinates['collect_resources'])
    
    def check_and_upgrade(self) -> bool:
        """Verifica e executa upgrades se disponíveis"""
        print("Verificando upgrades...")
        return self.tap(*self.coordinates['upgrade_button'])
    
    def navigate_to_workshop(self) -> bool:
        """Navega para a oficina"""
        print("Navegando para oficina...")
        return self.tap(*self.coordinates['workshop_button'])
    
    def navigate_to_factory(self) -> bool:
        """Navega para a fábrica"""
        print("Navegando para fábrica...")
        return self.tap(*self.coordinates['factory_button'])
    
    def handle_ads(self) -> bool:
        """Tenta fechar anúncios se detectados"""
        # Implementar lógica para detectar e fechar anúncios
        # Usar templates de botões de fechar anúncio
        close_ad_coords = self.find_template("templates/close_ad.png")
        if close_ad_coords:
            print("Fechando anúncio...")
            return self.tap(*close_ad_coords)
        return False
    
    def main_loop(self):
        """Loop principal da IA"""
        print("Iniciando IA do Lumber Inc...")
        
        while True:
            try:
                # 1. Verificar e fechar anúncios
                self.handle_ads()
                
                # 2. Coletar recursos
                self.collect_resources()
                
                # 3. Verificar upgrades
                self.check_and_upgrade()
                
                # 4. Navegar entre áreas periodicamente
                if int(time.time()) % 30 == 0:  # A cada 30 segundos
                    self.navigate_to_workshop()
                    time.sleep(1)
                    self.navigate_to_factory()
                
                # 5. Aguardar antes da próxima iteração
                time.sleep(2)
                
            except KeyboardInterrupt:
                print("\nParando IA...")
                break
            except Exception as e:
                print(f"Erro no loop principal: {e}")
                time.sleep(5)

def main():
    # Verificar se dispositivo está conectado
    result = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
    if "device" not in result.stdout:
        print("Nenhum dispositivo Android encontrado!")
        print("Certifique-se de que:")
        print("1. O dispositivo está conectado via USB")
        print("2. A depuração USB está ativada")
        print("3. Você autorizou o computador no dispositivo")
        return
    
    # Inicializar e executar IA
    ai = LumberIncAI()
    ai.main_loop()

if __name__ == "__main__":
    main()