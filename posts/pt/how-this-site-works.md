---
title: "Como este site funciona"
date: 2026-03-03
draft: true
excerpt: Um gerador de sites estático customizado em 1.150 linhas de Python. Uma dependência, quatro templates, e um pipeline de build que transforma Markdown num site bilíngue.
---

## Um gerador de sites estático

Este site roda sobre um gerador de sites estático customizado: um único script Python chamado `build.py`, com cerca de 1.150 linhas. Ele tem uma dependência de runtime (`markdown`) e três comandos: `python build.py` para gerar o site, `python build.py serve` para iniciar um servidor local, e `python build.py clean` para limpar o diretório de saída.

O conceito é o mesmo do Hugo, Jekyll ou Eleventy: pegar arquivos de texto, interpretar seus metadados, converter para HTML, envolvê-los em templates e gravar o resultado como arquivos estáticos. A diferença é o escopo. Hugo é um binário em Go com sistema de plugins, ecossistema de temas, taxonomias e centenas de opções de configuração. Jekyll precisa de Ruby e uma cadeia de dependências de gems. Aqui é um script único com exatamente as funcionalidades que um site precisa, nada mais.{mn}Os motores de template também diferem. Hugo usa Go templates, Jekyll usa Liquid, Eleventy usa Nunjucks. Este site usa um motor caseiro que suporta dois construtos: substituição de variáveis e blocos condicionais/de loop.{/mn}

## Estrutura do repositório

O diagrama abaixo mostra como os arquivos fonte se conectam através do `build.py` até a saída final. Passe o mouse sobre qualquer nó para rastrear suas conexões.

<div class="graph-embed" style="height: 650px;">
  <iframe src="/static/embeds/repo-architecture.html?embed&amp;lang=pt" title="Visualização da arquitetura do repositório"></iframe>
</div>

O conteúdo é escrito em `posts/` e `pages/`, dividido por idioma nos subdiretórios `en/` e `pt/`. Os templates definem a estrutura HTML. Os assets estáticos (CSS, JavaScript, fontes, embeds interativos) passam sem alteração. O diretório `output/` é efêmero e está no gitignore.

## O pipeline de build

Para cada idioma, o `build.py` executa uma sequência de transformações em cada arquivo Markdown: interpreta o frontmatter, converte Markdown para HTML (já com as extensões Tufte), extrai cabeçalhos para o índice de conteúdo, e depois renderiza o resultado em duas passagens de template (template de conteúdo primeiro, template base depois). Depois que todos os posts e páginas são gerados, ele monta a homepage, o feed Atom, copia os assets estáticos e grava a página da raiz.

O diagrama abaixo mostra essas etapas de processamento em detalhe. Clique em qualquer etapa para ver uma transformação concreta de antes e depois.

<div class="graph-embed" style="height: 650px;">
  <iframe src="/static/embeds/build-pipeline.html?embed&amp;lang=pt" title="Visualização do pipeline de build"></iframe>
</div>

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

O script de build interpreta isso dividindo pelas cercas `---`, extraindo pares de chave e valor, e depois passando o corpo para a biblioteca `markdown` do Python com extensões de blocos de código, tabelas, índice de conteúdo e uma pequena extensão Tufte habilitadas.{mn}O script tinha um conversor de fallback próprio para quando a biblioteca não estivesse instalada. Nunca fez falta na prática, então saiu, e o `markdown` agora é dependência obrigatória.{/mn} O resultado é HTML padrão, com as três construções do Tufte já convertidas.

## Extensões Tufte

O Tufte CSS traduz os princípios de design informacional de Edward Tufte para a web: alta densidade informacional, mínimo de ruído visual, e sidenotes em vez de notas de rodapé. Este site o estende com três sintaxes customizadas no Markdown:

**Sidenotes** (`{sn}...{/sn}`) viram notas numeradas na margem. Elas referenciam uma afirmação ou frase específica.

**Margin notes** (`{mn}...{/mn}`) não são numeradas. Adicionam contexto sem indicar um ponto de ancoragem específico.{mn}Como esta aqui. Sem número, sem interrupção. Apenas contexto adicional se você quiser.{/mn}

**New thoughts** (`{nt}...{/nt}`) renderizam como texto em versalete (small caps), a convenção do Tufte para iniciar uma nova seção dentro de um capítulo.

Por baixo dos panos, elas são uma extensão do Python-Markdown: um padrão inline que roda durante a conversão, depois que trechos e blocos de código já foram separados, então um `{sn}` dentro de código fica literal. Uma sidenote vira um `<label>`, um `<input>` checkbox (para toggle no mobile) e um `<span>`. O truque do checkbox significa que sidenotes funcionam no celular sem nenhum JavaScript: toque no número para mostrar ou esconder a nota.

## O motor de templates

Em vez de puxar Jinja2 ou Mako, o gerador usa um motor de templates caseiro. Ele suporta duas coisas:

**Variáveis**: `{{title}}` é substituído pelo valor de um dicionário de contexto.

**Blocos**: `{{#key}}...{{/key}}` funciona tanto como condicional (renderiza a seção se `key` for verdadeiro) quanto como loop (se `key` for uma lista, renderiza o conteúdo interno uma vez por item).

Essa é a API inteira. Quatro templates definem o site: `base.html` (30 linhas, a estrutura do site com header, nav e meta tags), `post.html` (19 linhas), `page.html` (15 linhas) e `index.html` (20 linhas). A renderização tem duas passagens: o template de conteúdo roda primeiro (ex: `post.html` preenche título, data e corpo), depois o resultado é envolvido pelo `base.html`.{mn}O trade-off é real: não tem escape de HTML, não tem aninhamento de blocos do mesmo tipo. Ambos são aceitáveis aqui porque todo o conteúdo é controlado pelo autor e nenhum template de fato aninha blocos. A renderização é feita numa passada só, então um `{{` dentro do corpo de um post nunca vira placeholder, e um placeholder que falta no contexto interrompe o build em vez de sair em branco.{/mn}

## Arquitetura bilíngue

Todo conteúdo existe em inglês e português. A estrutura de arquivos espelha isso:

```
posts/en/how-this-site-works.md
posts/pt/how-this-site-works.md
```

O script de build encontra pares de conteúdo comparando nomes de arquivo entre os diretórios de cada idioma. Se um post existe tanto em `en/` quanto em `pt/`, o gerador adiciona um seletor de idioma (o ícone de bandeira no header) que linka diretamente para a outra versão.

O `index.html` da raiz é a própria homepage em português. Um pequeno script no `<head>` verifica o `localStorage` atrás de uma escolha anterior de idioma, depois consulta `navigator.language`, e só manda o visitante para `/en/` se um dos dois indicar inglês. Nenhuma lógica server-side necessária.{mn}Quem lê em português cai na homepage sem nenhum redirecionamento, e o mesmo vale para quem está sem JavaScript e para os previews de link. Quem já escolheu inglês é redirecionado antes de a página aparecer.{/mn}

## O frontend

### Velocidade

O site carrega dois arquivos CSS (o Tufte base, que também declara as fontes, e as customizações) e até três pequenos arquivos JavaScript (toggle de tema, preferência de idioma e, nos posts que têm, o índice de conteúdo). Sem requests externos. Sem CDN. Sem analytics.{mn}A ET Book e a Source Code Pro são hospedadas localmente em `static/css/`. As quatro variações da ET Book somam cerca de 150KB em WOFF2, e os navegadores só baixam as que a página de fato usa.{/mn}

As páginas são HTML estático servido pelo GitHub Pages. Não tem o que ser lento.

### Modo escuro

O sistema de tema usa CSS custom properties no `:root` para o modo claro e `[data-theme="dark"]` para o escuro. Um script no `<head>` verifica o `localStorage` antes do navegador pintar, então nunca há um flash do tema errado.{mn}O botão de toggle é injetado via JavaScript depois do DOM carregar. Se JS estiver desabilitado, você recebe a preferência do sistema e pronto. Degradação graciosa.{/mn}

### Índice de conteúdo

Posts com três ou mais cabeçalhos ganham um índice. Em telas largas (1440px+), ele aparece como uma sidebar fixa à esquerda. Em telas menores, fica escondido. O script de build extrai as tags `h2` e `h3`, gera IDs e produz o HTML de navegação. Um pequeno script usa `IntersectionObserver` para destacar a seção atual conforme você rola a página.

### Visualizações interativas

As visualizações em D3.js (como os diagramas acima) são arquivos HTML autocontidos em `static/embeds/`, um arquivo por visualização para os dois idiomas, com o D3 servido pelo próprio site. Cada um funciona tanto standalone quanto embutido via iframe. O `?lang=en` ou `?lang=pt` na URL escolhe o idioma. Com `?embed`, eles escondem seu próprio chrome (toggle de tema, instruções) e acompanham o tema da página pai pelo evento `storage` do navegador: o toggle grava no `localStorage`, e os iframes da mesma origem ficam sabendo.

## Rascunhos

Definir `draft: true` no frontmatter de um post significa que ele é gerado e fica acessível pela URL direta, mas não aparece na página inicial nem no feed Atom. Útil para compartilhar posts específicos antes de publicar amplamente.
