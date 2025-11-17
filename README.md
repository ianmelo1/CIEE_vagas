# CIEE Vagas Scraper

Automação para buscar vagas de estágio/aprendiz no portal CIEE com filtros personalizados.

## O que faz

Acessa o site do CIEE, aplica filtros (tipo de vaga, área, cidade, etc) e salva todas as vagas encontradas em um arquivo JSON.

## Tecnologias

- Python 3.x
- Selenium WebDriver
- ChromeDriver

## Instalação

```bash
# Instale o Selenium
uv pip install selenium
```

## Configuração

Edite os filtros no arquivo `main.py`:

```python
filtros = {
    'tipo_vaga': 'ESTÁGIO',           # ESTÁGIO, APRENDIZ, PCD
    'nivel_ensino': 'Superior',        # Superior, Técnico, Médio
    'area_profissional': 'Tecnologia da Informação',
    'cidade': 'São Paulo'
}
```

## Como Usar

```bash
python main.py
```

O script vai:
1. Abrir o Chrome
2. Acessar o CIEE
3. Aplicar os filtros
4. Extrair as vagas
5. Salvar em `vagas_ciee_YYYYMMDD_HHMMSS.json`

## Dados Extraídos

Para cada vaga:
- Código
- Tipo (Estágio/Aprendiz/PCD)
- Empresa/Descrição
- Área profissional
- Localização
- Horário
- Salário
- Link

## Estrutura do JSON

```json
[
  {
    "codigo": "5860000",
    "tipo": "Estágio",
    "descricao": "Comércio varejista",
    "area": "LOGISTICA",
    "localizacao": "São Paulo - SP",
    "horario": "09:00 às 15:00",
    "salario": "R$ 900,00 / Mês",
    "link": "https://..."
  }
]
```

## Principais Funções

- `inicializar_driver()` - Abre o Chrome
- `aplicar_filtros()` - Seleciona os filtros
- `buscar_vagas()` - Encontra os cards das vagas
- `_extrair_dados_vaga()` - Pega os dados de cada vaga
- `salvar_resultados()` - Salva em JSON

## Troubleshooting

**Chrome não abre**: Instale o ChromeDriver ou use webdriver-manager

**Nenhuma vaga encontrada**: Verifique se os filtros têm vagas disponíveis no site

**Timeout**: Aumente o tempo de espera no código: `WebDriverWait(self.driver, 20)`

## Observações

- Apenas coleta da primeira página de resultados
- Campos que não existem aparecem como 'N/A'
- Use com responsabilidade e respeite o site do CIEE

## Autor

Projeto educacional de web scraping.
