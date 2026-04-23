import os
import time
import random
from playwright.sync_api import sync_playwright

def registrar_ponto():
    # 1. Configurações de Variabilidade (Atraso Aleatório)
    # Verifica a hora atual para saber qual o limite do atraso
    hora_atual = time.localtime().tm_hour
    
    # Se for de manhã (iniciando às 07:00), espera entre 0 e 70 minutos (até 08:10)
    # Se for de tarde (iniciando às 17:00), espera entre 0 e 60 minutos (até 18:00)
    minutos_atraso = random.randint(0, 70) if hora_atual < 12 else random.randint(0, 60)
    
    print(f"Aguardando {minutos_atraso} minutos antes de iniciar para variar o horário...")
    time.sleep(minutos_atraso * 60)

    # 2. Credenciais
    usuario = os.getenv("SITE_USUARIO")
    senha = os.getenv("SITE_SENHA")

    with sync_playwright() as p:
        # No GitHub Actions, headless deve ser sempre True
        browser = p.chromium.launch(headless=True)
        
        # Configura Localização e Permissões
        context = browser.new_context(
            geolocation={"latitude": -23.7245354, "longitude": -46.5618011},
            permissions=["geolocation"]
        )
        page = context.new_page()

        try:
            print("Acessando o site...")
            page.goto("https://intranet.csicargo.com.br/dp40")
            page.wait_for_load_state("networkidle")

            print("Digitando credenciais...")
            page.locator("input[type='text']").first.press_sequentially(usuario, delay=100)
            page.locator("input[type='password']").press_sequentially(senha, delay=100)
            
            page.wait_for_timeout(2000)
            page.locator("button:has-text('Acessar')").click()

            print("Acessando Menu 'Registro Ponto'...")
            card_menu = page.locator("div.mud-card:has-text('Registro Ponto')")
            card_menu.wait_for(state="visible", timeout=20000)
            card_menu.click()

            print("Efetuando o registro final...")
            botao_ponto = page.locator("button:has-text('Registrar Ponto')")
            botao_ponto.wait_for(state="visible", timeout=20000) 
            botao_ponto.click()
            
            page.wait_for_timeout(5000) 
            print(f"Sucesso! Ponto registrado às {time.strftime('%H:%M:%S')}")

        except Exception as e:
            print(f"Erro: {e}")
            page.screenshot(path="erro_automacao.png")
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    registrar_ponto()