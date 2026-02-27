---
title: "EM e PM em times de produto: quem puxa o quê"
date: 2026-02-27
excerpt: "Quando a PM precisa perguntar \"vai sair quando?\" o tempo todo, isso é sintoma de disfunção."
---

## A gestão das entregas é responsabilidade da EM

Em um time multidisciplinar de desenvolvimento de produto, a Engineering Manager (EM) tem três responsabilidades primárias. Não são as suas únicas contribuições relevantes para o time, mas são aquilo por que ela responde fundamentalmente.

A primeira é a tomada de decisão técnica. Devemos usar filas, tópicos, ou ambos? Comunicação síncrona ou assíncrona? Quantos serviços, organizados de quais formas? Mesmo quando as recomendações sobre essas decisões vêm de pessoas contribuidoras individuais, a EM ainda é responsável pela qualidade das decisões finais. Ela pode delegar parte do trabalho necessário para chegar à decisão, ou até a maior parte dele, mas não pode delegar a responsabilidade pela decisão em si.

A segunda é a gestão do processo de entrega. Vamos entregar aquilo com que nos comprometemos, na velocidade imaginada e na qualidade esperada? Se parece que vamos atrasar alguma entrega, existe algo que podemos fazer para evitar esse atraso? Se o atraso em si é inevitável, quais trade-offs isso força em outras entregas? Como podemos reduzir o cycle time e aumentar o throughput? Existe algum gargalo no processo de code review? A EM deveria estar bem posicionada para lidar com esses problemas, por definição, afinal ela gere os contribuidores individuais que fazem as entregas.

A terceira é a liderança e desenvolvimento de pessoas. Tenho o time que preciso, com as pessoas certas nos papéis certos? Como cada pessoa do time pode crescer? Como assegurar, ao mesmo tempo, desafio constante e segurança psicológica? A EM é responsável por garantir que o time tenha as competências necessárias para executar bem, e por desenvolver essas competências ao longo do tempo. Isso inclui decisões difíceis: identificar quem está pronto para assumir mais responsabilidade, quem precisa de mais suporte, e quem talvez não esteja no lugar certo. Essa é uma atribuição difícil, mas crítica.

Essas são as principais responsabilidades de uma EM, mas não as únicas. Por exemplo, a capacidade de influenciar o roadmap de produto é frequentemente o que distingue boas vs. ótimas Engineering Managers. A EM é a pessoa mais bem posicionada para ter um conhecimento atualizado e profundo do estoque de dívida técnica do time, dos gargalos de arquitetura, e das limitações de developer experience que afetam a capacidade de entrega. Se os serviços são fragmentados demais ou os testes em CI são lentos, entregar fica mais difícil independentemente de quão bem o time é gerido no dia a dia. Essa visão precisa alimentar as decisões de roadmap. Um planejamento que ignora dívida técnica está fadado a acumular problemas para o futuro, e a EM tem a obrigação de tornar isso visível.

## Se a PM cobra prazo, algo está errado

Essa divisão de responsabilidades tem implicações sobre o papel de Product Manager (PM).

Em times fortes, a PM não precisa se envolver muito no dia a dia operacional do time para garantir as entregas, justamente porque a EM dá conta. Isso libera a PM para se concentrar naquilo que ela está mais bem posicionada para fazer: entender profundamente o problema da perspectiva dos clientes e da empresa, definir prioridades em um horizonte de vários meses, e olhar para fora do time. Como podemos aumentar a adoção do produto sem precisar de um esforço high-touch? Quais adaptações no produto seriam necessárias para entrar em um novo segmento? Como podemos trabalhar junto com Operações e Product Marketing para viabilizar o sucesso das iniciativas?

Em times mais fracos, acontece algo diferente. A PM acaba assumindo a gestão do processo de entregas: sinalizando atrasos, imprimindo cadência, cobrando prazos, montando status reports. Quando a PM precisa perguntar "vai sair quando?" o tempo todo, algo está errado. Isso não é Product Management. Isso é gestão de projetos, e deveria estar com a EM.

Esse padrão normalmente está associado a dois fatores. O primeiro são EMs que não têm as habilidades para exercer plenamente o seu papel em delivery. O segundo são PMs que não são seniores ou estratégicas o suficiente para ocupar o espaço que deveriam ocupar. O resultado é que ninguém faz bem uma coisa nem outra. A PM preenche um vácuo, mas deixa de fazer o trabalho olhando para frente e para fora do time. A EM perde ownership e se acomoda em um papel menor. Esse problema pesa sobre os produtos, os clientes, e o negócio.

Se eu tivesse que escolher um único ponto de alavancagem para melhorar a maioria dos times de produto que eu já vi, seria a maturidade da liderança de Software Engineering. Não porque Product Management não tenha problemas. Mas porque quando a EM é forte, a PM consegue finalmente fazer o trabalho que deveria estar fazendo desde o início. (E, se não consegue, isso fica exposto de uma forma que antes não era necessariamente possível perceber.)

## Isso não significa que a PM deveria ser hands-off

Existe uma distinção que eu quero deixar clara: nada disso significa que a PM pode ignorar os detalhes da execução.

Saber o que está acontecendo é esperado de todas as lideranças, de todas as disciplinas. Não é porque a gestão da entrega é responsabilidade de Software Engineering que PMs podem se dar ao luxo de não entender o que está sendo construído, de não questionar decisões, de não se envolver nas discussões. Nunca o nível de conhecimento de uma PM sobre uma iniciativa importante do time dela deveria ser "só sei que está em dev".

Pense em uma funcionalidade crítica do seu produto que esteja lenta, tenha problemas de usabilidade importantes, ou gere reclamações frequentes dos usuários por outros motivos. Quem tem que saber qual é o diagnóstico, qual é o plano de ação, e como o time vem avançando? Todas as lideranças têm que saber. A EM tem que saber, a PM tem que saber.

A distinção é entre quem puxa e quem acompanha. A EM puxa a gestão da entrega. A PM acompanha, questiona e contribui. Se a PM precisa puxar, como é comum em times pouco maduros, isso é sintoma de disfunção. O primeiro passo para corrigir o problema é quase sempre o mesmo: fortalecer a EM e esperar mais dela.
