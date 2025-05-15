# Projeto Playwright SauceDemo

## Estrutura do Projeto

A estrutura do projeto está organizada para facilitar o desenvolvimento e execução dos testes automatizados com Playwright.

- `env/` contém o ambiente virtual Python. Dentro dele, o arquivo **sitecustomize.py** é especialmente importante pois customiza o ambiente durante a execução, carregando configurações e ajustes essenciais.

- `project/` contém o código principal da aplicação e configuração dos testes.

- `tests/` contém os scripts de teste automatizados.

- `.vscode/` configurações específicas do VSCode para facilitar o desenvolvimento.

---

## Observações sobre o ambiente virtual

- Você verá um arquivo chamado `sitecustomize.txt` 

- Ele estará setado em um `arquivo .txt`, assim, renomeie ele para `.py` e set no diretório (`env/lib/python3.13/site-packages/`)

O arquivo `sitecustomize.py` dentro do ambiente virtual (`env/lib/python3.13/site-packages/`) é carregado automaticamente pelo Python em todas as execuções do ambiente e serve para:

- Aplicar ajustes globais e configurações do interpretador.
- Customizar o comportamento padrão de módulos e pacotes.
- Facilitar integrações e testes automatizados.

Por isso, ele merece atenção especial e não deve ser removido nem alterado sem cuidado.

---


## Como rodar o projeto

1. Ative o ambiente virtual:

```bash
source env_start.bash  # Ele vai criar (Caso não tenha o ambiente) e abrir o ambiente
```

2. Instale as dependências (caso ainda não tenha feito):

```bash
pip install -r requirements.txt
```

PS: Se não executou, execute o playwright install após download

```bash
playwright install
```
  
3. Execute os testes com:

```bash
pytest
```
OU
```bash
pytest --verbose
```

## Você também pode rodar com Docker:

1. Monte a imagem:

```terminal
docker build -t saucedemo-project .
```

2. Execute em headless:
```terminal
docker run --rm saucedemo-project
```

3. Se estiver no linux e quiser rodar com interface.

    - No arquivo test_saucedemo.py em tests, habilite:

    ```python
    @pytest.fixture(scope="module")
    def site():
        # Inicializa a instância para todos os testes do módulo
        site = SaucedemoMarket("https://www.saucedemo.com/", headless=False)
        yield site
        site.close_site()
    ```

    - Salve e suba denovo com build.

    - Execute no terminal

    ```terminal
    xhost +local:docker
    docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix saucedemo-project
    ```


## Sobre o projeto

O projeto tem como objetivo automatizar testes na plataforma SauceDemo utilizando Playwright com pytest, proporcionando uma estrutura simples, clara e eficiente para validar funcionalidades básicas da aplicação.

### project/
```terminal
. 
├── config_playwrite.py
│
└── saucedemo.py
```

#### config_playwrite.py

Esse módulo define a classe SiteExtractor, uma interface de alto nível para interagir com o navegador usando o Playwright de forma síncrona. Ele encapsula as principais operações de navegação e manipulação de elementos da página.
Principais responsabilidades:

    Iniciar o navegador (Firefox, por padrão).

    Acessar URLs.

    Interagir com elementos da página (preencher campos, clicar, esperar, selecionar).

    Executar scripts JavaScript.

    Capturar conteúdo de elementos e da página como um todo.

    Encerrar o navegador com segurança.

Estrutura da Classe SiteExtractor

    Atributos principais:

        url: URL a ser acessada.

        headless: define se o navegador será executado sem interface gráfica.

        p, browser, page: objetos do Playwright que controlam a instância do navegador.

    Métodos principais:

        start(): inicia o Playwright e o navegador, abre uma nova página e navega até a URL.

        wait_for_element(selector): espera um seletor estar presente na página.

        wait_for(time): espera por um tempo específico (usando sleep).

        input_fill(selector, value, timeout): preenche um campo com determinado valor.

        click_element(selector): clica em um elemento.

        select_option_element(selector, option_value): seleciona uma opção em um <select>.

        query_all(selector): retorna todos os elementos que correspondem ao seletor.

        query_one(selector): retorna o primeiro elemento que corresponde ao seletor.

        get_inner_text(selector): retorna o texto interno de um seletor.

        get_content_html(): retorna o HTML atual da página.

        execute_js(script): executa um script JavaScript na página.

        close(): fecha o navegador e encerra o Playwright.

Uso no modo standalone:

Quando executado diretamente (__main__), ele:

    Abre o site SauceDemo.

    Espera o seletor .login_credentials_wrap-inner carregar.

    Coleta e imprime o texto da área de login.

    Fecha o navegador.

Esse arquivo é útil tanto para testes manuais rápidos quanto como base para outros módulos de automação.

PS >>> Se quiser rodar apenas ele para testar execute na raiz do projeto:

```terminal
python -m project.config_playwrite
```

#### saucedemo.py

Este módulo é responsável por implementar o comportamento específico da automação no site https://www.saucedemo.com, utilizando os métodos fornecidos pela classe SiteExtractor (definida no config_playwrite.py).

Ele encapsula uma lógica de navegação, extração de dados, interação com a interface e execução de testes sobre o comportamento da aplicação web.

Principais Responsabilidades

    Automatizar o login com diferentes perfis de usuários de teste.

    Simular interações com o carrinho de compras (adicionar e remover produtos).

    Realizar ordenações de produtos por diferentes critérios.

    Verificar se há imagens repetidas ou inválidas.

    Testar o comportamento do sistema em situações adversas ou inusitadas.

Estrutura da Classe SaucedemoMarket

A classe SaucedemoMarket herda de SiteExtractor, ganhando acesso direto aos métodos utilitários para manipulação do navegador com Playwright.
Atributos e Inicialização

    A classe é instanciada com a URL do site https://www.saucedemo.com.

    O modo headless pode ser definido para controle visual da automação.

Métodos principais

    __init__(): Inicializa com a URL e define o navegador (Firefox por padrão).

    extract_login_options():

        Acessa a página de login.

        Extrai os nomes dos usuários de teste fornecidos no site.

        Também extrai a senha padrão disponível para todos os logins.

    login(username, password):

        Preenche os campos de usuário e senha.

        Clica no botão de login.

        Aguarda o carregamento da interface interna após o login.

    logout():

        Clica no menu de navegação lateral.

        Encontra e clica na opção de logout.

        Retorna para a tela inicial de login.

    get_items_from_page():

        Captura o nome e o preço de todos os itens disponíveis na loja.

        Retorna uma lista com dicionários contendo name e price.

    select_order(order_type):

        Seleciona uma opção no select de ordenação do site.

        Pode ser por nome crescente/decrescente, preço crescente/decrescente etc.

    add_all_to_cart() / remove_all_from_cart():

        Adiciona ou remove todos os produtos visíveis no momento ao carrinho.

    get_cart_count():

        Retorna o número exibido no ícone do carrinho.

        Serve para validar se a quantidade de itens bate com os adicionados.

    validate_404_image():

        Procura por uma imagem inválida (cachorro 404 escondido).

        Caso encontrada, imprime ou reporta.

    find_duplicate_images():

        Extrai todos os src das imagens dos produtos.

        Detecta se existem URLs de imagem repetidas (conteúdo duplicado).

Execução Standalone

Se o arquivo for executado diretamente (python saucedemo.py), o seguinte fluxo é realizado:

    Inicia o navegador e abre o site.

    Extrai os usuários de teste e a senha.

    Faz login com o primeiro usuário disponível.

    Ordena os produtos por menor preço.

    Adiciona todos os produtos ao carrinho.

    Verifica se a quantidade bate com o número mostrado no carrinho.

    Verifica se há imagens duplicadas entre os produtos.

    Verifica se a imagem de erro 404 (dog) aparece na loja.

    Finaliza e fecha o navegador.

Esse fluxo simula um comportamento real de navegação e valida aspectos da interface que poderiam causar erros no uso da aplicação.

PS >>> Se quiser rodar apenas ele para testar execute na raiz do projeto:

```terminal
python -m project.saucedemo
```

### tests/
```terminal
.
└── test_saucedemo.py
```

#### test_saucedemo.py

Os testes foram escritos com pytest, utilizando parametrize, fixture e validações automatizadas por meio da classe SaucedemoMarket. A suíte cobre:

    Login com todos os usuários disponíveis (standard, locked_out, problem, etc.).

    Validação de senha incorreta e campos vazios.

    Adição e remoção de produtos ao carrinho.

    Ordenação de preços (crescente e decrescente).

    Validação visual de imagens duplicadas ou incorretas para usuários com problemas (ex: problem_user).

    Verificação da imagem de cachorro (presente apenas para alguns usuários).

    Contagem correta no carrinho, independentemente do número de botões de adicionar clicados.

PS: Total de testes e casos: 31 itens
