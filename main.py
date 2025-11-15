from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import json
from datetime import datetime


class CIEEScraper:
    """Scraper para buscar vagas no portal CIEE"""

    def __init__(self, headless=False):
        """
        Inicializa o scraper

        Args:
            headless (bool): Se True, executa o navegador em modo headless
        """
        self.driver = None
        self.headless = headless
        self.url_base = "https://www.ciee.org.br/portal/estudantes/ofertas/estagios"

    def inicializar_driver(self):
        """Configura e inicializa o WebDriver"""
        options = webdriver.ChromeOptions()

        if self.headless:
            options.add_argument('--headless')

        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def acessar_site(self):
        """Acessa o site do CIEE"""
        print(f"Acessando {self.url_base}...")
        self.driver.get(self.url_base)
        time.sleep(5)
        print("✅ Página carregada!")

    def aplicar_filtros(self, filtros):
        """
        Aplica filtros na busca de vagas

        Args:
            filtros (dict): Dicionário com os filtros desejados
        """
        print("\n" + "=" * 50)
        print("APLICANDO FILTROS")
        print("=" * 50)

        # Filtro 1: Tipo de vaga
        if 'tipo_vaga' in filtros:
            self._selecionar_tipo_vaga(filtros['tipo_vaga'])

        # Filtro 2: Nível de ensino
        if 'nivel_ensino' in filtros:
            self._selecionar_nivel_ensino(filtros['nivel_ensino'])

        # Filtro 3: Área profissional
        if 'area_profissional' in filtros:
            self._selecionar_area_profissional(filtros['area_profissional'])

        # Filtro 4: Cidade
        if 'cidade' in filtros:
            self._selecionar_cidade(filtros['cidade'])

        print("\n✅ Todos os filtros aplicados!")
        time.sleep(2)

        # IMPORTANTE: Clicar no botão "Aplicar" após definir todos os filtros
        self._clicar_botao_aplicar()

    def _selecionar_tipo_vaga(self, tipo_vaga):
        """
        Seleciona o tipo de vaga clicando na opção da lista

        Args:
            tipo_vaga (str): 'ESTÁGIO', 'APRENDIZ', 'PCD', etc
        """
        try:
            print(f"\n🔹 Selecionando tipo de vaga: {tipo_vaga}")

            # Clica no dropdown para abrir
            tipo_vaga_input = self.wait.until(
                EC.element_to_be_clickable((By.ID, "TipoVaga"))
            )
            tipo_vaga_input.click()
            time.sleep(1)

            # Mapa de tipos para IDs do HTML
            mapa_tipos = {
                'ESTÁGIO': 'estagio',
                'APRENDIZ': 'aprendiz',
                'PCD': 'pcd',
                'PROCESSOS PÚBLICOS': 'pp',
                'SOLUÇÕES ESPECIAIS': 'se'
            }

            # Pega o ID correto
            id_opcao = mapa_tipos.get(tipo_vaga.upper())

            if not id_opcao:
                print(f"❌ Tipo '{tipo_vaga}' não reconhecido!")
                print(f"Opções válidas: {list(mapa_tipos.keys())}")
                return

            # Clica na opção da lista
            opcao = self.wait.until(
                EC.element_to_be_clickable((By.ID, id_opcao))
            )
            opcao.click()
            time.sleep(1)

            print(f"  ✅ '{tipo_vaga}' selecionado!")

        except TimeoutException:
            print(f"  ❌ Timeout ao selecionar tipo de vaga")
        except Exception as e:
            print(f"  ❌ Erro: {e}")

    def _selecionar_nivel_ensino(self, nivel_ensino):
        """
        Seleciona o nível de ensino clicando na opção da lista

        Args:
            nivel_ensino (str): 'Superior', 'Técnico', 'Médio', 'Fundamental', 'Todos'
        """
        try:
            print(f"\n🔹 Selecionando nível de ensino: {nivel_ensino}")

            # Clica no dropdown para abrir
            nivel_input = self.wait.until(
                EC.element_to_be_clickable((By.ID, "NivelEnsino"))
            )
            nivel_input.click()
            time.sleep(1.5)

            # Mapa de níveis para IDs do HTML
            mapa_niveis = {
                'TODOS': 'TODOS',
                'ENSINO FUNDAMENTAL': 'EF',
                'FUNDAMENTAL': 'EF',
                'ENSINO MÉDIO': 'EM',
                'MÉDIO': 'EM',
                'TÉCNICO': 'TE',
                'SUPERIOR': 'SU'
            }

            # Pega o ID correto
            id_opcao = mapa_niveis.get(nivel_ensino.upper())

            if not id_opcao:
                print(f"❌ Nível '{nivel_ensino}' não reconhecido!")
                print(f"Opções válidas: {list(mapa_niveis.keys())}")
                return

            # Clica na opção da lista
            opcao = self.wait.until(
                EC.element_to_be_clickable((By.ID, id_opcao))
            )
            opcao.click()
            time.sleep(1)

            print(f"  ✅ '{nivel_ensino}' selecionado!")

        except TimeoutException:
            print(f"  ❌ Timeout ao selecionar nível de ensino")
        except Exception as e:
            print(f"  ❌ Erro: {e}")

    def _selecionar_area_profissional(self, area_profissional):
        """
        Seleciona a área profissional clicando na opção da lista

        Args:
            area_profissional (str): Ex: 'Informática', 'Administração'
        """
        try:
            print(f"\n🔹 Selecionando área profissional: {area_profissional}")

            # Clica no dropdown para abrir
            area_input = self.wait.until(
                EC.element_to_be_clickable((By.ID, "AreaProfissional"))
            )

            # Scroll até o elemento antes de clicar
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", area_input)
            time.sleep(0.5)

            area_input.click()
            time.sleep(1.5)

            # Mapa de áreas profissionais com IDs corretos
            mapa_areas = {
                'INFORMÁTICA': '18',
                'TECNOLOGIA DA INFORMAÇÃO': '18',
                'TI': '18',
                'ADMINISTRAÇÃO': '1',
                'ENGENHARIA': '73',
                'GASTRONOMIA': '11241',
                'LETRAS': '20',
                'INDUSTRIA': '17',
                'INSTITUIÇÕES FINANCEIRAS': '11241',
                'MARKETING': '22',
                'MEIO AMBIENTE': '24',
                'GEOCIÊNCIAS': '73',
                'GEOMÁTICA': '45',
                'ASTRONOMIA': '10081',
                # Adicione mais conforme necessário
            }

            # Pega o ID correto
            id_opcao = mapa_areas.get(area_profissional.upper())

            if not id_opcao:
                print(f"⚠️ Área '{area_profissional}' não mapeada, tentando busca por texto...")
                # Tenta buscar pelo texto
                try:
                    xpath_opcao = f"//ul[@id='ComboAreaProfissional']//li[contains(text(), '{area_profissional}')]"
                    opcao = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, xpath_opcao))
                    )
                    # Scroll na lista até o elemento
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", opcao)
                    time.sleep(0.3)
                    opcao.click()
                except:
                    print(f"❌ Não foi possível encontrar '{area_profissional}'")
                    return
            else:
                # Aguarda a lista aparecer
                time.sleep(0.5)

                # Clica pela ID usando JavaScript como fallback
                try:
                    opcao = self.wait.until(
                        EC.presence_of_element_located((By.ID, id_opcao))
                    )
                    # Scroll até a opção dentro da lista
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", opcao)
                    time.sleep(0.3)

                    # Tenta clicar normalmente primeiro
                    try:
                        opcao.click()
                    except:
                        # Se falhar, usa JavaScript
                        self.driver.execute_script("arguments[0].click();", opcao)
                except:
                    print(f"❌ Não foi possível clicar na opção")
                    return

            time.sleep(1)
            print(f"  ✅ '{area_profissional}' selecionada!")

        except TimeoutException:
            print(f"  ❌ Timeout ao selecionar área profissional")
        except Exception as e:
            print(f"  ❌ Erro: {e}")

    def _selecionar_cidade(self, cidade):
        """
        Seleciona a cidade clicando na opção da lista

        Args:
            cidade (str): Ex: 'BRASÍLIA - DF', 'SÃO PAULO - SP'
        """
        try:
            print(f"\n🔹 Selecionando cidade: {cidade}")

            # Clica no campo para abrir o dropdown
            cidade_input = self.wait.until(
                EC.element_to_be_clickable((By.ID, "CidadeVaga"))
            )
            cidade_input.click()
            time.sleep(1)

            # Digita parte do nome para filtrar as opções
            cidade_input.clear()
            # Pega apenas a primeira palavra da cidade para facilitar a busca
            termo_busca = cidade.split()[0].upper()
            cidade_input.send_keys(termo_busca)
            time.sleep(2)  # Aguarda filtrar

            # Mapa de cidades conhecidas com IDs
            mapa_cidades = {
                'BRASÍLIA - DF': '5300108',
                'BRASÍLIA DE MINAS - MG': '3108602',
                'SÃO PAULO - SP': '3550308',
                'RIO DE JANEIRO - RJ': '3304557',
                # Adicione mais cidades conforme necessário
            }

            cidade_normalizada = cidade.upper().strip()
            id_cidade = mapa_cidades.get(cidade_normalizada)

            if id_cidade:
                # Clica pelo ID
                try:
                    opcao = self.wait.until(
                        EC.element_to_be_clickable((By.ID, id_cidade))
                    )
                    opcao.click()
                except:
                    # Se não encontrar pelo ID, tenta pelo texto
                    xpath_opcao = f"//ul[@id='ComboCidade']//li[contains(text(), '{cidade_normalizada}')]"
                    opcao = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, xpath_opcao))
                    )
                    opcao.click()
            else:
                # Busca pelo texto
                xpath_opcao = f"//ul[@id='ComboCidade']//li[contains(text(), '{cidade_normalizada}')]"
                opcao = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, xpath_opcao))
                )
                opcao.click()

            time.sleep(1)
            print(f"  ✅ '{cidade}' selecionada!")

        except TimeoutException:
            print(f"  ❌ Timeout ao selecionar cidade")
        except Exception as e:
            print(f"  ❌ Erro: {e}")

    def _clicar_botao_aplicar(self):
        """Clica no botão 'Aplicar' para efetivar os filtros"""
        try:
            print(f"\n🔹 Clicando no botão 'Aplicar'...")

            # Procura pelo botão "Aplicar" usando a classe correta
            botao_aplicar = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.btn-search.btn-purple"))
            )
            botao_aplicar.click()

            # Aguarda a página recarregar com os filtros
            time.sleep(4)

            print(f"  ✅ Filtros aplicados com sucesso!")

        except TimeoutException:
            print(f"  ❌ Timeout ao clicar no botão Aplicar")
        except Exception as e:
            print(f"  ❌ Erro ao aplicar filtros: {e}")

    def buscar_vagas(self):
        """Busca e extrai informações das vagas"""
        print("\n" + "=" * 50)
        print("BUSCANDO VAGAS")
        print("=" * 50)
        vagas = []

        try:
            # Aguarda os cards carregarem - vários seletores possíveis
            time.sleep(3)

            # Tenta diferentes seletores para encontrar as vagas
            seletores = [
                "a.vaga-item",
                ".vaga-row",
                ".card-vaga",
                "[class*='vaga']",
                "div[class*='item-vaga']",
                "a[href*='codigoVaga']"
            ]

            cards_vagas = None
            for seletor in seletores:
                try:
                    cards_vagas = self.driver.find_elements(By.CSS_SELECTOR, seletor)
                    if cards_vagas and len(cards_vagas) > 0:
                        print(f"✅ Usando seletor: {seletor}")
                        break
                except:
                    continue

            if not cards_vagas or len(cards_vagas) == 0:
                print("❌ Nenhuma vaga encontrada com os seletores testados")
                print("🔍 Tentando seletor genérico...")

                # Última tentativa: qualquer link que contenha informações de vaga
                cards_vagas = self.driver.find_elements(By.TAG_NAME, "a")
                cards_vagas = [c for c in cards_vagas if
                               'vaga' in c.get_attribute('class').lower() or 'codigoVaga' in c.get_attribute('href')]

            print(f"✅ {len(cards_vagas)} vagas encontradas!\n")

            # Extrai dados de cada vaga
            for index, card in enumerate(cards_vagas, 1):
                print(f"📄 Extraindo vaga {index}/{len(cards_vagas)}...")
                vaga = self._extrair_dados_vaga(card)

                # Só adiciona se tiver pelo menos o código ou link
                if (vaga['codigo'] and vaga['codigo'] != 'N/A') or (vaga['link'] and vaga['link'] != 'N/A'):
                    vagas.append(vaga)
                else:
                    print(f"  ⚠️ Vaga {index} sem dados válidos, ignorando...")

        except TimeoutException:
            print("❌ Nenhuma vaga encontrada (timeout)")
        except Exception as e:
            print(f"❌ Erro ao buscar vagas: {e}")

        return vagas

    def _extrair_dados_vaga(self, elemento):
        """
        Extrai dados de uma vaga específica

        Args:
            elemento: WebElement contendo informações da vaga

        Returns:
            dict: Dicionário com dados da vaga
        """
        vaga = {
            'codigo': '',
            'tipo': '',
            'descricao': '',
            'area': '',
            'localizacao': '',
            'horario': '',
            'salario': '',
            'link': ''
        }

        try:
            # Link da vaga (pega primeiro)
            try:
                link_href = elemento.get_attribute('href')
                if link_href:
                    vaga['link'] = link_href
                else:
                    vaga['link'] = 'N/A'
            except:
                vaga['link'] = 'N/A'

            # Código da vaga
            try:
                codigo_elem = elemento.find_element(By.CSS_SELECTOR, ".codigo-vaga, .cod-vaga")
                vaga['codigo'] = codigo_elem.text.strip()
            except:
                vaga['codigo'] = 'N/A'

            # Tipo da vaga
            try:
                tipo_elem = elemento.find_element(By.CSS_SELECTOR, ".tipo-vaga, .badge")
                vaga['tipo'] = tipo_elem.text.strip()
            except:
                vaga['tipo'] = 'N/A'

            # Descrição/Título da vaga
            try:
                desc_elem = elemento.find_element(By.CSS_SELECTOR, ".titulo-vaga, .descricao, h3")
                vaga['descricao'] = desc_elem.text.strip()
            except:
                vaga['descricao'] = 'N/A'

            # Área profissional
            try:
                area_elem = elemento.find_element(By.CSS_SELECTOR, ".area-vaga, .info-area")
                vaga['area'] = area_elem.text.strip()
            except:
                vaga['area'] = 'N/A'

            # Localização
            try:
                local_elem = elemento.find_element(By.CSS_SELECTOR, ".local-vaga, .info-local, .localizacao")
                vaga['localizacao'] = local_elem.text.strip()
            except:
                vaga['localizacao'] = 'N/A'

            # Horário
            try:
                horario_elem = elemento.find_element(By.CSS_SELECTOR, ".horario-vaga, .info-horario")
                vaga['horario'] = horario_elem.text.strip()
            except:
                vaga['horario'] = 'N/A'

            # Salário/Bolsa
            try:
                salario_elem = elemento.find_element(By.CSS_SELECTOR, ".salario-vaga, .info-salario, .bolsa-auxilio")
                vaga['salario'] = salario_elem.text.strip()
            except:
                vaga['salario'] = 'N/A'

        except Exception as e:
            print(f"  ⚠️ Erro ao extrair vaga: {e}")

        return vaga

    def salvar_resultados(self, vagas, formato='json'):
        """
        Salva os resultados em arquivo

        Args:
            vagas (list): Lista de vagas encontradas
            formato (str): 'json' ou 'csv'
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if formato == 'json':
            arquivo = f"vagas_ciee_{timestamp}.json"
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(vagas, f, ensure_ascii=False, indent=4)
            print(f"\n💾 Resultados salvos em: {arquivo}")

        elif formato == 'csv':
            # TODO: Implementar CSV se necessário
            pass

    def fechar(self):
        """Fecha o navegador"""
        if self.driver:
            self.driver.quit()
            print("\n🔒 Navegador fechado.")


def main():
    """Função principal"""

    # CONFIGURE SEUS FILTROS AQUI
    filtros = {
        'tipo_vaga': 'ESTÁGIO',  # ESTÁGIO, APRENDIZ, PCD
        'nivel_ensino': 'Superior',  # Superior, Técnico, Médio
        'area_profissional': 'Informática',  # Informática, Administração, etc
        'cidade': 'BRASÍLIA - DF'
    }

    scraper = CIEEScraper(headless=False)

    try:
        # Executa o scraper
        scraper.inicializar_driver()
        scraper.acessar_site()
        scraper.aplicar_filtros(filtros)
        vagas = scraper.buscar_vagas()

        # Mostra resumo
        print("\n" + "=" * 50)
        print(f"TOTAL: {len(vagas)} vagas encontradas!")
        print("=" * 50)

        # Salva em JSON
        if vagas:
            scraper.salvar_resultados(vagas, formato='json')

            # Mostra as 3 primeiras vagas
            print("\n📋 Primeiras vagas:")
            for i, vaga in enumerate(vagas[:3], 1):
                print(f"\n  {i}. {vaga['tipo']} - {vaga['descricao']}")
                print(f"     📍 {vaga['localizacao']}")
                print(f"     💰 {vaga['salario']}")

    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")

    finally:
        scraper.fechar()


if __name__ == "__main__":
    main()