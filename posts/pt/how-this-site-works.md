---
title: "Como este site funciona"
date: 2026-03-03
draft: true
excerpt: Um gerador de sites estático customizado em 1.300 linhas de Python. Uma dependência, quatro templates, e um pipeline de build que transforma Markdown num site bilíngue.
---

## Um gerador de sites estático

Este site roda sobre um gerador de sites estático customizado: um único script Python chamado `build.py`, com cerca de 1.300 linhas. Ele tem uma dependência de runtime (`markdown`) e três comandos: `python build.py` para gerar o site, `python build.py serve` para iniciar um servidor local, e `python build.py clean` para limpar o diretório de saída.

O conceito é o mesmo do Hugo, Jekyll ou Eleventy: pegar arquivos de texto, interpretar seus metadados, converter para HTML, envolvê-los em templates e gravar o resultado como arquivos estáticos. A diferença é o escopo. Hugo é um binário em Go com sistema de plugins, ecossistema de temas, taxonomias e centenas de opções de configuração. Jekyll precisa de Ruby e uma cadeia de dependências de gems. Aqui é um script único com exatamente as funcionalidades que um site precisa, nada mais.{mn}Os motores de template também diferem. Hugo usa Go templates, Jekyll usa Liquid, Eleventy usa Nunjucks. Este site usa um motor caseiro que suporta dois construtos: substituição de variáveis e blocos condicionais/de loop.{/mn}

## Estrutura do repositório

O diagrama abaixo mostra como os arquivos fonte se conectam através do `build.py` até a saída final. Passe o mouse sobre qualquer nó para rastrear suas conexões.

<div class="graph-embed" style="height: 650px;">
  <iframe src="/static/embeds/repo-architecture-pt.html?embed" title="Visualização da arquitetura do repositório"></iframe>
</div>
<script>
(function() {
  var iframe = document.querySelector('.graph-embed iframe[src*="repo-architecture"]');
  var observer = new MutationObserver(function() {
    var theme = document.documentElement.getAttribute('data-theme');
    if (iframe.contentWindow) {
      iframe.contentWindow.postMessage({ type: 'theme-change', theme: theme }, '*');
    }
  });
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
})();
</script>

O conteúdo é escrito em `posts/` e `pages/`, dividido por idioma nos subdiretórios `en/` e `pt/`. Os templates definem a estrutura HTML. Os assets estáticos (CSS, JavaScript, fontes, embeds interativos) passam sem alteração. O diretório `output/` é efêmero e está no gitignore.

## O pipeline de build

Para cada idioma, o `build.py` executa uma sequência de transformações em cada arquivo Markdown: interpreta o frontmatter, converte Markdown para HTML, aplica as extensões Tufte, extrai cabeçalhos para o índice de conteúdo, e depois renderiza o resultado em duas passagens de template (template de conteúdo primeiro, template base depois). Depois que todos os posts e páginas são gerados, ele monta a homepage, o feed Atom, copia os assets estáticos e cria uma página de redirecionamento na raiz.

O diagrama abaixo mostra essas etapas de processamento em detalhe. Clique em qualquer etapa para ver uma transformação concreta de antes e depois.

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

## Conteúdo e frontmatter

Todo post começa como um arquivo Markdown com metadados no estilo YAML no topo:

```
---
title: "Como este site funciona"
date: 2026-03-03
excerpt: Um gerador de sites estático customizado...
---

O conteúdo real aqui.
```

O script de build interpreta isso dividindo pelas cercas `---`, extraindo pares de chave e valor, e depois passando o corpo para a biblioteca `markdown` do Python com extensões de blocos de código, tabelas e índice de conteúdo habilitadas.{mn}Existe um conversor de fallback completo embutido no script para quando a biblioteca não está instalada. Ele lida com cabeçalhos, negrito, itálico, blocos de código, links, listas e tabelas. Desnecessário na prática, mas significa que o gerador tem zero dependências obrigatórias.{/mn} O resultado é HTML padrão, que então passa por três transformações específicas do Tufte.

## Extensões Tufte

O Tufte CSS traduz os princípios de design informacional de Edward Tufte para a web: alta densidade informacional, mínimo de ruído visual, e sidenotes em vez de notas de rodapé. Este site o estende com três sintaxes customizadas no Markdown:

**Sidenotes** (`{sn}...{/sn}`) viram notas numeradas na margem. Elas referenciam uma afirmação ou frase específica.

**Margin notes** (`{mn}...{/mn}`) não são numeradas. Adicionam contexto sem indicar um ponto de ancoragem específico.{mn}Como esta aqui. Sem número, sem interrupção. Apenas contexto adicional se você quiser.{/mn}

**New thoughts** (`{nt}...{/nt}`) renderizam como texto em versalete (small caps), a convenção do Tufte para iniciar uma nova seção dentro de um capítulo.

Por baixo dos panos, são substituições via regex que rodam depois da conversão de Markdown para HTML. Uma sidenote vira um `<label>`, um `<input>` checkbox (para toggle no mobile) e um `<span>`. O truque do checkbox significa que sidenotes funcionam no celular sem nenhum JavaScript: toque no número para mostrar ou esconder a nota.

## O motor de templates

Em vez de puxar Jinja2 ou Mako, o gerador usa um motor de templates caseiro. Ele suporta duas coisas:

**Variáveis**: `{{title}}` é substituído pelo valor de um dicionário de contexto.

**Blocos**: `{{#key}}...{{/key}}` funciona tanto como condicional (renderiza a seção se `key` for verdadeiro) quanto como loop (se `key` for uma lista, renderiza o conteúdo interno uma vez por item).

Essa é a API inteira. Quatro templates definem o site: `base.html` (33 linhas, a estrutura do site com header, nav e meta tags), `post.html` (19 linhas), `page.html` (15 linhas) e `index.html` (20 linhas). A renderização tem duas passagens: o template de conteúdo roda primeiro (ex: `post.html` preenche título, data e corpo), depois o resultado é envolvido pelo `base.html`.{mn}O trade-off é real: não tem escape de HTML, não tem aninhamento de blocos do mesmo tipo. Ambos são aceitáveis aqui porque todo o conteúdo é controlado pelo autor e nenhum template de fato aninha blocos.{/mn}

## Arquitetura bilíngue

Todo conteúdo existe em inglês e português. A estrutura de arquivos espelha isso:

```
posts/en/how-this-site-works.md
posts/pt/how-this-site-works.md
```

O script de build encontra pares de conteúdo comparando nomes de arquivo entre os diretórios de cada idioma. Se um post existe tanto em `en/` quanto em `pt/`, o gerador adiciona um seletor de idioma (o ícone de bandeira no header) que linka diretamente para a outra versão.

O `index.html` da raiz é um redirect. Ele verifica o `localStorage` para uma escolha anterior de idioma, depois consulta `navigator.language`, e por último usa inglês como padrão. Nenhuma lógica server-side necessária.{mn}Isso significa que visitantes recorrentes vão direto para seu idioma sem um flash da versão errada. Visitantes do Brasil recebem português automaticamente na primeira visita.{/mn}

## O frontend

### Velocidade

O site carrega três arquivos CSS (Tufte base, customizações, e declarações da fonte ET Book) e três pequenos arquivos JavaScript (toggle de tema, preferência de idioma, índice de conteúdo). Sem requests externos para renderização. Sem CDN. Sem analytics.{mn}A ET Book é hospedada localmente em `static/css/et-book/`. O conjunto completo da fonte tem cerca de 300KB, mas os navegadores só baixam os pesos efetivamente usados.{/mn}

As páginas são HTML estático servido pelo GitHub Pages. Não tem o que ser lento.

### Modo escuro

O sistema de tema usa CSS custom properties no `:root` para o modo claro e `[data-theme="dark"]` para o escuro. Um script no `<head>` verifica o `localStorage` antes do navegador pintar, então nunca há um flash do tema errado.{mn}O botão de toggle é injetado via JavaScript depois do DOM carregar. Se JS estiver desabilitado, você recebe a preferência do sistema e pronto. Degradação graciosa.{/mn}

### Índice de conteúdo

Posts com três ou mais cabeçalhos ganham um índice. Em telas largas (1440px+), ele aparece como uma sidebar fixa à esquerda. Em telas menores, fica escondido. O script de build extrai as tags `h2` e `h3`, gera IDs e produz o HTML de navegação. Um pequeno script usa `IntersectionObserver` para destacar a seção atual conforme você rola a página.

### Visualizações interativas

As visualizações em D3.js (como os diagramas acima) são arquivos HTML autocontidos em `static/embeds/`. Cada um funciona tanto standalone quanto embutido via iframe. Quando carregados com `?embed` na URL, eles escondem seu próprio chrome (toggle de tema, instruções) e escutam eventos `postMessage` da página pai para sincronizar o tema de cores.

## Rascunhos

Definir `draft: true` no frontmatter de um post significa que ele é gerado e fica acessível pela URL direta, mas não aparece na página inicial nem no feed Atom. Útil para compartilhar posts específicos antes de publicar amplamente.
