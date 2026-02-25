---
title: "Engineering Management e Product Management: quem puxa o quê"
date: 2026-02-25
excerpt: "Em times de produto, a gestão das entregas é responsabilidade da EM. Quando a PM precisa puxar, é sintoma, não solução."
---

## A gestão das entregas é responsabilidade da EM

Em times de produto, a liderança de Software Engineering tem três responsabilidades primárias.

A primeira é a tomada de decisão técnica. Devemos usar filas ou tópicos? Comunicação síncrona ou assíncrona? Quantos serviços, organizados de quais formas? Mesmo quando as recomendações sobre essas decisões vêm de pessoas contribuidoras individuais, a liderança de Software Engineering ainda é responsável pela qualidade das decisões finais. Ela pode delegar parte do trabalho necessário para chegar à decisão, ou até a maior parte dele, mas não pode delegar a responsabilidade pela decisão em si.

A segunda é a gestão do processo de entrega. Vamos entregar aquilo com que nos comprometemos, na velocidade imaginada e na qualidade esperada? Se parece que vamos atrasar alguma entrega, existe algo que podemos fazer para evitar esse atraso? Se o atraso em si é inevitável, quais trade-offs isso força em outras entregas? Como podemos reduzir o cycle time e aumentar o throughput? A liderança de Software Engineering deveria estar bem posicionada para lidar com esses problemas, por definição, afinal ela gere os contribuidores individuais que fazem as entregas.

A terceira é a liderança e desenvolvimento de pessoas. Tenho o time que preciso? As pessoas certas estão nos papéis certos? Como cada pessoa do time pode crescer? A liderança de Software Engineering é responsável por garantir que o time tenha as competências necessárias para executar bem, e por desenvolver essas competências ao longo do tempo. Isso inclui decisões difíceis: identificar quem está pronta para assumir mais responsabilidade, quem precisa de mais suporte, e quem talvez não esteja no papel certo. Times que entregam consistentemente quase sempre têm uma EM forte nessa dimensão. Não é coincidência.

Essas são as responsabilidades primárias. Mas existem outras contribuições que são esperadas de uma EM, mesmo não sendo sua responsabilidade exclusiva. A mais importante, provavelmente, é a influência sobre o roadmap. A EM é a pessoa mais bem posicionada para ter um conhecimento atualizado e profundo do estoque de dívida técnica do time, dos gargalos arquiteturais, e das limitações de infraestrutura que afetam a capacidade de entrega. Se a arquitetura está ruim ou o CI/CD está quebrado, entregar fica mais difícil independentemente de quão bem o time é gerido no dia a dia. Essa visão precisa alimentar as decisões de roadmap. Um roadmap que ignora dívida técnica é um roadmap que está acumulando problemas para o futuro, e a EM tem a obrigação de tornar isso visível.

## Se a PM cobra prazo, algo deu errado

O que essa divisão de responsabilidades implica para a liderança de Product Management?

Em empresas fortes, a PM tem pouco envolvimento no dia a dia operacional do time, justamente porque a EM dá conta. Isso libera a PM para se concentrar naquilo que só Product Management pode fazer: entender profundamente o problema, definir prioridades no horizonte de quarters e anos, e olhar para fora do time. Como expandimos a adoção do produto? Como entramos em um novo segmento? Qual é o posicionamento competitivo certo?

Em empresas mais fracas, acontece algo diferente. A PM acaba assumindo a gestão do processo de entregas: sinalizando atrasos, imprimindo cadência, cobrando prazos, montando status reports. Quando a PM é quem pergunta "vai sair quando?", algo deu errado. Isso não é Product Management. Isso é gestão de projeto, e deveria estar com a EM.

Esse padrão normalmente está associado a dois fatores. O primeiro são EMs que não exercem plenamente seu papel no que diz respeito a delivery. O segundo são PMs que não são seniores ou estratégicas o suficiente para ocupar o espaço que deveriam ocupar. O resultado é que ninguém faz bem nem uma coisa nem outra. A PM tapa buraco da EM e deixa de fazer o trabalho estratégico. A EM perde ownership e se acomoda. E, por mais que a PM tente compensar, isso não resolve o problema de fundo. No final, a resposta quase sempre é fortalecer a EM, não pedir mais da PM.

Se eu tivesse que escolher um único ponto de alavancagem para melhorar a maioria dos times de produto que já vi, seria a maturidade da liderança de Software Engineering. Não porque Product Management não tenha problemas. Mas porque quando a EM é forte, a PM consegue finalmente fazer o trabalho que deveria estar fazendo desde o início.

## Acompanhar não é o mesmo que ser hands-off

Existe uma distinção que eu quero deixar clara: nada disso significa que a PM pode ignorar os detalhes da execução.

Do ponto de vista de informação, de saber o que está acontecendo, de acompanhar o estado das coisas, isso é esperado de todas as lideranças, de todas as disciplinas. Não é porque a gestão da entrega é responsabilidade de Software Engineering que PMs podem se dar ao luxo de não entender o que está sendo construído, de não questionar decisões, de não se envolver nas discussões. Nunca o nível de conhecimento de uma PM sobre uma iniciativa importante do time dela deveria ser "só sei que está em dev".

Pense em uma funcionalidade crítica do seu produto que está lenta, tem problemas de usabilidade e gera reclamações frequentes dos usuários. Quem tem que saber qual é o diagnóstico, qual é o plano de ação e onde estamos no plano? Todas as lideranças. A EM tem que saber. A PM tem que saber. A designer tem que saber.

A distinção é entre quem puxa e quem acompanha. A EM puxa a gestão da entrega. A PM acompanha, questiona e contribui. Mas se a PM precisa puxar, é sintoma, não solução.
