#!/usr/bin/env python3
"""
Script para calibrar coordenadas do jogo
"""

import subprocess
import time
from PIL import Image

def capture_and_show_coordinates():
    """Captura tela e mostra coordenadas do clique"""
    print("Script de calibração de coordenadas")
    print("Clique na tela para obter coordenadas, Ctrl+C para sair")
    
    try:
        while True:
            input("Pressione Enter para capturar tela...")
            
            # Captura tela
            result = subprocess.run("adb exec-out screencap -p", shell=True, capture_output=True)
            if result.returncode == 0:
                with open("calibration_screen.png", 'wb') as f:
                    f.write(result.stdout)
                
                # Abre a imagem
                img = Image.open("calibration_screen.png")
                img.show()
                
                print("Imagem salva como 'calibration_screen.png'")
                print("Use um editor de imagem para encontrar as coordenadas dos elementos")
                
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nCalibração encerrada")

if __name__ == "__main__":
    capture_and_show_coordinates()