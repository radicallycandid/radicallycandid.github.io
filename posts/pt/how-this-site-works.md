---
title: "Como este site funciona"
date: 2026-03-03
draft: true
excerpt: Um único script Python, uma dependência, e muitas opiniões sobre como texto deveria ser apresentado na web.
---

## Um script

Este site inteiro é gerado por um único script Python. Cerca de 1.300 linhas. Uma dependência de runtime (`markdown`). Sem framework, sem CMS, sem pipeline de build com uma dúzia de ferramentas encadeadas.

O script lê arquivos Markdown, interpreta seus metadados, converte para HTML, aplica templates e escreve a saída. Rode `python build.py` e você tem um site estático completo numa pasta chamada `output/`. É isso.{mn}Tem também `python build.py serve` para um servidor local de desenvolvimento e `python build.py clean` para limpar o diretório de saída. Três comandos no total.{/mn}

Eu construí tudo com o Claude Code. Não só o site, o gerador em si. Eu definia o que queria, revisava o que ele produzia, testava, pedia ajustes. O resultado é algo que eu entendo completamente e consigo modificar sem consultar documentação de um framework que vou esquecer até o ano que vem.

O diagrama abaixo mostra o pipeline completo: como os arquivos fonte passam pelo script de build até virar o site final. Clique em qualquer etapa de processamento para ver uma transformação concreta de antes e depois.

<div class="graph-embed" style="height: 650px;">
  <iframe src="/static/embeds/build-pipeline-pt.html?embed" title="Visualização do pipeline de build"></iframe>
</div>
<script>
(function() {
  var iframe = document.querySelector('.graph-embed iframe[src*="build-pipeline"]');
  var observer = new MutationObserver(function() {
    var theme = document.documentElement.getAttribute('data-theme');
    if (iframe.contentWindow) {
      iframe.contentWindow.postMessage({ type: 'theme-change', theme: theme }, '*');
    }
  });
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
})();
</script>

## Markdown entra, HTML sai

Todo post começa como um arquivo Markdown com metadados no estilo YAML no topo:

```
---
title: "Como este site funciona"
date: 2026-03-03
excerpt: Um único script Python...
---

O conteúdo real aqui.
```

O script de build interpreta isso dividindo o conteúdo pelas cercas `---`, extraindo pares de chave e valor, e depois passando o corpo para a biblioteca `markdown` do Python.{mn}Na verdade existe um conversor de fallback completo embutido no script para quando a biblioteca não está instalada. Ele lida com cabeçalhos, negrito, itálico, blocos de código, links, listas e tabelas. Desnecessário na prática, mas significa que o gerador tem zero dependências obrigatórias.{/mn} O resultado é HTML padrão, que então passa por três transformações específicas do Tufte.

## Extensões Tufte

Eu conheci o Edward Tufte lendo *The Visual Display of Quantitative Information* na faculdade. As ideias dele sobre densidade informacional e minimizar o supérfluo foram fundamentais na minha carreira em ciência de dados. O Tufte CSS traduz essa filosofia para a web, e este site o estende com três sintaxes customizadas no Markdown:

**Sidenotes** (`{sn}...{/sn}`) viram notas numeradas na margem. Elas referenciam uma afirmação ou frase específica.

**Margin notes** (`{mn}...{/mn}`) não são numeradas. Adicionam contexto sem indicar um ponto de ancoragem específico.{mn}Como esta aqui. Sem número, sem interrupção. Apenas contexto adicional se você quiser.{/mn}

**New thoughts** (`{nt}...{/nt}`) renderizam como texto em versalete (small caps), a convenção do Tufte para iniciar uma nova seção dentro de um capítulo.

Por baixo dos panos, são substituições via regex que rodam depois da conversão de Markdown para HTML. Uma sidenote vira um `<label>`, um `<input>` checkbox (para toggle no mobile) e um `<span>`. O truque do checkbox significa que sidenotes funcionam no celular sem nenhum JavaScript: toque no número para mostrar ou esconder a nota.

## O motor de templates

Em vez de puxar Jinja2 ou Mako, o gerador usa um motor de templates caseiro. Ele suporta duas coisas:

**Variáveis**: `{{title}}` é substituído pelo valor de um dicionário de contexto.

**Blocos**: `{{#key}}...{{/key}}` funciona tanto como condicional (renderiza a seção se `key` for verdadeiro) quanto como loop (se `key` for uma lista, renderiza o conteúdo interno uma vez por item).

Essa é a API inteira. O template base tem 30 linhas de HTML. O template de post tem 19. Não tem herança, não tem filtros, não tem macros. Quando seus templates são simples assim, você não precisa de uma linguagem de templates. Você precisa de substituição de strings.{mn}O trade-off é real: não tem escape de HTML, não tem aninhamento de blocos do mesmo tipo. Ambos são aceitáveis aqui porque todo o conteúdo é controlado pelo autor e nenhum template de fato aninha blocos.{/mn}

## Bilíngue por design

Todo conteúdo existe em inglês e português. A estrutura de arquivos espelha isso:

```
posts/en/how-this-site-works.md
posts/pt/how-this-site-works.md
```

O script de build encontra pares de conteúdo comparando nomes de arquivo entre os diretórios de cada idioma. Se um post existe tanto em `en/` quanto em `pt/`, o gerador adiciona um seletor de idioma (o ícone de bandeira no header) que linka diretamente para a outra versão.

O `index.html` da raiz é só um redirect. Ele verifica o `localStorage` para uma escolha anterior de idioma, depois consulta `navigator.language`, e por último usa inglês como padrão. Nenhuma lógica server-side necessária.{mn}Isso significa que visitantes recorrentes vão direto para seu idioma sem um flash da versão errada. Visitantes do Brasil recebem português automaticamente na primeira visita.{/mn}

Escrever nos dois idiomas dá mais trabalho, mas força clareza. Quando uma frase não traduz bem, geralmente é porque a ideia não está clara o suficiente.

## O frontend

### Velocidade

O site carrega três arquivos CSS (Tufte base, customizações, e declarações da fonte ET Book) e três pequenos arquivos JavaScript (toggle de tema, preferência de idioma, índice de conteúdo). Sem requests externos. Sem CDN. Sem analytics. Sem web fonts carregadas do Google.{mn}A ET Book é hospedada localmente em `static/css/et-book/`. O conjunto completo da fonte tem cerca de 300KB, mas os navegadores só baixam os pesos efetivamente usados.{/mn}

As páginas são HTML estático servido pelo GitHub Pages. Não tem o que ser lento.

### Modo escuro

O sistema de tema usa CSS custom properties no `:root` para o modo claro e `[data-theme="dark"]` para o escuro. Um script no `<head>` verifica o `localStorage` antes do navegador pintar, então nunca há um flash do tema errado.{mn}O botão de toggle é injetado via JavaScript depois do DOM carregar. Se JS estiver desabilitado, você recebe a preferência do sistema e pronto. Degradação graciosa.{/mn}

### Índice de conteúdo

Posts com três ou mais cabeçalhos ganham um índice. Em telas largas (1440px+), ele aparece como uma sidebar fixa à esquerda. Em telas menores, fica escondido. O script de build extrai as tags `h2` e `h3`, gera IDs e produz o HTML de navegação. Um pequeno script usa `IntersectionObserver` para destacar a seção atual conforme você rola a página.

### Visualizações interativas

As visualizações em D3.js (como o diagrama do pipeline acima) são arquivos HTML autocontidos em `static/embeds/`. Cada um funciona tanto standalone quanto embutido via iframe. Quando carregados com `?embed` na URL, eles escondem seu próprio chrome (toggle de tema, instruções) e escutam eventos `postMessage` da página pai para sincronizar o tema de cores.

## Rascunhos

Definir `draft: true` no frontmatter de um post significa que ele é gerado e fica acessível pela URL direta, mas não aparece na página inicial nem no feed Atom. Eu uso isso para posts que quero compartilhar com pessoas específicas antes de publicar amplamente. Este post, por exemplo, é um rascunho agora.

## Por que customizado

Eu poderia ter usado Hugo ou Jekyll. São boas ferramentas. Mas eu queria entender cada parte do sistema que publica o que eu escrevo. Quando algo quebra, eu não quero pesquisar no issue tracker de um framework. Eu quero ler 1.300 linhas de Python que eu revisei linha por linha.

É um site pessoal. Deveria ser pessoal até o último detalhe.
