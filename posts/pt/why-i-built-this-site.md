---
title: "Por que eu construí este site do zero"
date: 2026-03-01
draft: true
excerpt: Eu queria o site pessoal mais simples e durável possível. Construí meu próprio gerador com a ajuda do Claude Code.
---

## A pergunta

Eu me pergunto há um bom tempo: qual é o jeito mais simples, elegante e robusto de ter um site pessoal?

Quando olho para sites pessoais que admiro, como o do Paul Graham e o do Gwern, o que me chama atenção é justamente o que está ausente. Não tem framework JavaScript. Não tem CMS. Não tem build pipeline com quinze dependências. São páginas que carregam instantaneamente e vão continuar funcionando daqui a dez anos.

## Por que não usar um gerador existente

Hugo, Jekyll, Gatsby, Next.js. Todas essas ferramentas existem e funcionam. Eu poderia ter escolhido qualquer uma. Mas toda vez que eu sentava pra avaliar, esbarrava na mesma sensação: é mais complexidade do que eu preciso.

Eu não quero aprender a configurar um framework. Não quero me adaptar à estrutura de pastas que outra pessoa decidiu. Não quero depender de um ecossistema que pode mudar de direção ou ser abandonado.

O que eu quero é simples: pegar arquivos Markdown e transformar em HTML. É isso.

## O papel do Claude Code

Aqui a história fica mais honesta. Eu tenho mais de uma década de proximidade com programação, mas sou vice-presidente de uma empresa. Meu dia a dia não é escrever código. Sei o suficiente pra ler, revisar e testar, mas construir um gerador de site inteiro sozinho seria um investimento de tempo que provavelmente me faria desistir.

O Claude Code tornou isso viável. Não só pela capacidade, mas pela energia: quando a barreira entre ideia e execução cai o suficiente, você realmente faz a coisa. O gerador inteiro (o script de build, os templates, o CSS customizado) foi construído com ele. Eu definia o que queria, revisava o que ele produzia, testava, pedia ajustes. O resultado é um script Python de cerca de 1200 linhas que faz exatamente o que eu preciso e nada mais.

Mas o mais interessante não foi economizar tempo. Foi aprender. Construir um gerador do zero, mesmo com assistência de IA, me ensinou como essas ferramentas funcionam por baixo dos panos. Parsear frontmatter, converter Markdown pra HTML, aplicar templates, gerar feeds Atom. Eu entendia tudo isso superficialmente e agora entendo de verdade.

## Tufte

A escolha visual não é acidental. Eu conheci o Edward Tufte lendo *The Visual Display of Quantitative Information* na faculdade. Aquele livro mudou como eu penso sobre dados e comunicação. As ideias dele (densidade informacional, minimizar o supérfluo, deixar os dados falarem) foram fundamentais na minha carreira como cientista de dados e, depois, quando assumi a gestão da disciplina de design na empresa em que trabalho.

O Tufte CSS traduz parte dessa filosofia pra web. Sidenotes e margin notes aparecem no campo visual sem interromper o fluxo de leitura.{mn}Notas de rodapé forçam uma decisão: vale a pena interromper a leitura? Sidenotes tiram essa fricção. A informação está ali se você quiser.{/mn} É uma escolha que reflete como eu acho que texto deveria ser consumido.

## Por que bilíngue

Português é minha língua nativa, mas eu vejo pouco conteúdo de qualidade em português brasileiro sobre os temas que me interessam. Ao mesmo tempo, queria que o que eu escrevesse fosse lido tanto por pessoas da minha organização, a Arco Educação, quanto por quem não fala português.

Dá mais trabalho, sim. Mas escrever nos dois idiomas me força a pensar com mais cuidado sobre o que estou dizendo. Quando uma frase não traduz bem, geralmente é porque a ideia não está clara o suficiente.

## Velocidade importa

O site tem que ser rápido. Não "rápido para um blog". Rápido de verdade. Páginas que carregam instantaneamente. Sem JavaScript desnecessário. Sem requests externos bloqueando renderização.

Um site lento desrespeita o tempo de quem está lendo. E um site pessoal, que não tem a desculpa de complexidade de produto, não tem motivo nenhum pra ser lento.

## O resultado

Me orgulho do que saiu. É simples. É bonito. Tem dark mode. É bilíngue. Carrega instantaneamente. E eu entendo cada parte do código que o gera.

É exatamente o que eu queria.
