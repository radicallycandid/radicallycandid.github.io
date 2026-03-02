---
title: "A IA vai diluir as fronteiras entre papéis adjacentes, não eliminar todos eles"
date: 2026-03-01
excerpt: A narrativa do "Product Builder" está parcialmente correta: a IA de fato permite que as pessoas assumam responsabilidades mais amplas. Mas os papéis não vão colapsar em um só.
---

## A narrativa do Product Builder

Vem ganhando força no mundo de tecnologia a narrativa de que a inteligência artificial vai dissolver por completo as fronteiras entre os papéis de desenvolvimento de produto. Nessa visão, Product Managers, Software Engineers, Product Designers, e outros papéis vão se fundir em um só, frequentemente chamado de "Product Builder". Para quem trabalha em empresas de tecnologia e tem usado ferramentas como o Claude Code para ir muito além do que teria conseguido antes, essa previsão parece, ao mesmo tempo, empolgante e óbvia. Movimentos concretos de empresas como o [LinkedIn](https://www.youtube.com/watch?v=R-zCfLQD_84) reforçam a tese, o termo já tem um [manifesto próprio](https://productbuilder.community), e a ideia de que a divisão entre "quem entende o problema", "quem desenha a interface" e "quem escreve o código" representa overhead desnecessário está sendo [articulada explicitamente](https://labs.adaline.ai/p/redesigning-product-work-for-the-ai-era-in-2026).

Essa narrativa acerta em algo importante e transformador. A IA realmente torna possível que as pessoas se estendam para áreas que antes estavam fora do seu alcance. Uma Product Manager hoje consegue prototipar uma interface funcional. Uma Product Designer consegue gerar código que funciona fora do Figma. Pessoas de diferentes disciplinas conseguem analisar dados mesmo sem um domínio profundo de SQL. Para quem tem curiosidade e iniciativa, as barreiras são mais baixas, e as fronteiras, mais fluidas.

Mesmo assim, eu acredito que a conclusão de que, em empresas grandes e maduras, todos os papéis vão convergir para um só não se sustenta. Ela superestima a capacidade de adaptação cognitiva e psicológica das pessoas e subestima a profundidade necessária para desempenhar qualquer um desses papéis bem em um contexto profissional.

## Por que diferentes papéis existem

O grau de especialização dos papéis em uma organização não é arbitrário. Na verdade, ele é o resultado de uma tensão entre duas forças. De um lado, a especialização gera valor: uma Software Engineer especializada em back end sabe resolver problemas em sistemas distribuídos que dariam dor de cabeça para alguém sem esse foco, e uma Product Designer entende padrões de interação de forma que não seria razoável esperar de uma Software Engineer. Mais profundidade leva a decisões melhores e produtos melhores.

Do outro lado, a especialização tem um custo importante: a coordenação entre pessoas. Toda vez que uma responsabilidade é dividida entre duas pessoas, aparecem handoffs, ruídos de comunicação, reuniões e atrasos. Em uma startup pequena, o custo dessa coordenação frequentemente supera o benefício de ter especialistas, e é por isso que times mais early-stage tendem a privilegiar um perfil mais generalista. Isso inclusive tem a ver com as razões pelas quais algumas pessoas que se dão bem em startups pequenas às vezes sofrem com o crescimento dessas empresas.

Ferramentas de IA e agentes cada vez mais capazes podem deslocar o ponto ótimo desse trade-off. Reduzindo a barreira de competência em habilidades adjacentes e facilitando o aprendizado autodirigido, eles tornam viável que uma pessoa assuma trabalhos que antes exigiam duas. Quando uma única pessoa consegue fazer o que antes demandava coordenação em um pequeno grupo, as empresas podem optar por papéis mais amplos e menos numerosos. Quando isso acontece, não é porque a especialização se tornou inútil, mas porque o custo de coordenação de manter uma divisão de papéis muito granular deixou de valer a pena.

Essa mudança me parece real e muito relevante para a nossa carreira, mas, pelo menos no curto prazo (digamos, menos de 2 anos), eu prevejo uma transformação menos drástica do que a narrativa do "Product Builder" propõe. Em outras palavras, em 2026 e 2027, eu ainda acredito que vamos falar de Software Engineers, Product Designers, etc. Quem prevê uma fusão completa das disciplinas parece ignorar que as pessoas têm inclinações naturais, características cognitivas e identidades profissionais que as tornam mais adequadas para alguns papéis que para outros.

## O grafo dos papéis adjacentes

Em vez do modelo do "Product Builder", quero propor um framework mais realista para pensar sobre como a IA vai remodelar os papéis profissionais nos próximos meses ou poucos anos.

<label for="mn-agi" class="margin-toggle">&#8853;</label>
<input type="checkbox" id="mn-agi" class="margin-toggle"/>
<span class="marginnote">Minhas previsões não se aplicam a um mundo pós-AGI. Essa talvez seja a melhor crítica ao que eu proponho neste texto, afinal as capacidades dos modelos de IA vêm progredindo impressionantemente rápido. Por outro lado, essa fraqueza não é só minha: quais previsões sobre o mundo atual são robustas e válidas pós-AGI?</span>

Vamos considerar alguns papéis diferentes que existem em uma organização moderna de desenvolvimento de produto. Esses papéis não são todos igualmente próximos entre si. Uma Software Engineer focada em front end e uma Product Designer trabalham em territórios que se sobrepõem todos os dias. Essa Product Designer, por outro lado, tem pouco em comum com uma Data Platform Engineer em termos de atribuições e habilidades. A distância entre os papéis importa.

O grafo a seguir mostra papéis comuns e suas adjacências mais relevantes na minha opinião. Ele é propositalmente simples e não exaustivo, priorizando o uso no argumento que vem a seguir. A inclusão de vários papéis ligados a Dados (Data Platform Engineer, Analytics Engineer, Data Scientist, Business Analyst) tem a ver com a minha bagagem pessoal e também com o fato de que a conversa com um amigo que inspirou este texto começou justamente questionando esses papéis como existem hoje.

<div class="graph-embed">
  <iframe src="/static/embeds/professions-graph-pt.html?embed" title="Grafo de adjacência de profissões"></iframe>
</div>
<script>
// Sync theme changes with embedded graph
(function() {
  var iframe = document.querySelector('.graph-embed iframe');
  var observer = new MutationObserver(function() {
    var theme = document.documentElement.getAttribute('data-theme');
    if (iframe.contentWindow) {
      iframe.contentWindow.postMessage({ type: 'theme-change', theme: theme }, '*');
    }
  });
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
})();
</script>

<label for="mn-depth" class="margin-toggle">&#8853;</label>
<input type="checkbox" id="mn-depth" class="margin-toggle"/>
<span class="marginnote">A IA também tem o efeito de comprimir a profundidade necessária para cada especialidade, não só as barreiras entre elas. Mas essa compressão é assimétrica, porque os agentes automatizam a execução muito mais que substituem julgamento. É nesse julgamento de saber o que (não) construir e o que está errado mesmo parecendo certo que a diferença entre os papéis realmente mora.</span>

Minha tese é simples: a IA vai gradualmente diluir as fronteiras entre papéis adjacentes nesse grafo, sem eliminar os papéis em si. A diluição vai acontecer ao longo das arestas, não em todos os lugares ao mesmo tempo. Uma Product Designer vai achar mais fácil assumir trabalhos de Software Engineering ligados a front end. Uma Analytics Engineer vai absorver parte do que Business Analysts fazem hoje, ou vice-versa. Por outro lado, não prevejo a ascensão de profissionais que fazem, ao mesmo tempo, uma grande coleção de papéis distantes nesse grafo.

## O que isso significa para a sua carreira

Vou ser completamente sincero, sabendo que algumas pessoas que trabalham na organização sob a minha liderança vão ler este texto. Se você hoje ocupa um único nó nesse grafo, eu acredito que você esteja, sim, sujeito a um risco profissional real. (Existem algumas exceções, normalmente ligadas a contextos de negócio muito específicos, como Crédito, ou a pessoas muito seniores, com uma profundidade dificilmente substituível.) Para a maioria dos profissionais, permanecer em um único nó significa que alguém que consegue fazer o seu trabalho e pelo menos parte de um trabalho adjacente vai ser mais valioso para as empresas. Embora isso já fosse verdade antes, esse fenômeno é drasticamente acentuado por IA.

Minha recomendação forte é que você estenda as suas habilidades na direção de um nó adjacente. Escolha o nó vizinho que mais te interessa ou que melhor complementa os seus pontos fortes atuais, e procure se tornar profissionalmente competente nesse conjunto de habilidades o quanto antes.

Se você já está consolidado em dois nós adjacentes, é viável mirar em um terceiro, mas eu alertaria que isso é genuinamente difícil. As habilidades e até o perfil psicológico exigido ao longo de três nós são frequentemente bem diferentes entre si. Quem conseguir ocupar essa extensão vai ser excepcionalmente valioso, mas isso vai continuar sendo raro.

Eu não recomendaria mirar em quatro ou mais nós, e aconselharia especificamente contra pular para nós distantes. Procure percorrer o grafo ao longo das suas arestas. O maior valor está em combinar habilidades adjacentes, cuja sobreposição gera algo maior que a soma das partes.

## Combinações de papéis na prática

Algumas dessas combinações de papéis adjacentes já existem, e vale a pena olhar para elas como exemplos do que esse grafo prevê.

**Full Stack Software Engineer** (FE + BE). Esse talvez seja o exemplo mais maduro. É um papel que já existe há anos, e a tendência é que isso se torne simplesmente o significado padrão de Software Engineer, ou então de [Product Engineer](https://posthog.com/blog/what-is-a-product-engineer).

**Design Engineer** (FE + PD). Esse é um papel interessante e muito mais recente, que tem ganhado tração em algumas das empresas mais inovadoras do mundo, incluindo [Cursor](https://cursor.com/careers/design-engineer) e [Vercel](https://vercel.com/careers/design-engineer-us-5709080004). Representa alguém que consegue tanto conceber uma experiência quanto transformá-la em código em produção, fechando a lacuna entre intenção de design e implementação e eliminando um handoff frequentemente problemático.

**Data Engineer** (DP + AE). Essa posição híbrida representa algo que era o padrão até poucos anos atrás, quando o mundo de Dados passou a se distinguir entre "pessoas que amam Kafka e Airflow" vs. "pessoas que amam dbt", ou então entre "pessoas que entendem muito de Python e um pouco de SQL" vs. "pessoas que entendem muito de SQL e um pouco de Python". É alguém que consegue tanto construir a infraestrutura para dados em escala quanto modelar os dados para consumo.

Outros papéis híbridos não vão necessariamente ter novos termos associados. Por exemplo, a combinação PM + BA pode manter o título Product Manager, enquanto a combinação AE + BA pode manter o título Analytics Engineer ou assumir outro já existente, dependendo da empresa.

A combinação possível de Product Manager e Engineering Manager (PM + EM) é uma das fusões mais interessantes que podem surgir, embora eu honestamente não saiba qual deveria ser o nome dela. Na prática, é uma junção menos óbvia do que pode parecer, porque o perfil e as disposições das pessoas que gravitam em direção a esses dois papéis tendem a ser bem diferentes. Mesmo assim, nos casos bem-sucedidos, é uma das possibilidades que parecem levar à maior produção de valor para empresas.

Falando em Engineering Managers, a tendência de times mais enxutos significa menos overhead de gestão de pessoas e mais espaço para contribuição técnica direta. A Engineering Manager "hands-on" (p. ex., EM + FE ou EM + BE), que frequentemente programa junto com o time como parte da sua rotina, é uma expressão natural dessa mudança. Isso é algo que eu vejo com bons olhos nos casos em que é possível, porque ter mais profundidade sobre o código e sobre a experiência de programar em um certo contexto (repositório, domínio, etc.) facilita que a EM desempenhe melhor os outros aspectos do seu trabalho.

## As arestas, não o centro

A narrativa do "Product Builder" imagina um futuro em que todos os papéis colapsam no centro do grafo. Eu acho que o que vai realmente acontecer é menos dramático, mas mais interessante: as arestas vão ficar mais "grossas" e os papéis adjacentes vão se sobrepor cada vez mais. As pessoas vão poder (e vão enfrentar uma pressão competitiva para) se estender na direção dos nós adjacentes e se tornar profissionais mais híbridas. O trade-off entre especialização e coordenação não deixa de existir em um mundo com IA cada vez mais capaz, mas os pontos de equilíbrio se deslocam, sem dúvida, no sentido de favorecer profissionais mais versáteis.

Quem ocupa uma posição de liderança em uma organização de desenvolvimento de produto tem uma responsabilidade dupla diante das mudanças descritas acima. A primeira é ser honesto sobre a direção em que o mundo (ou, no mínimo, a empresa específica em questão) está caminhando. É isso que este texto tenta fazer. A segunda é criar as condições para que as pessoas realmente consigam se expandir. Isso inclui, por exemplo, investir em aprendizado e capacitação do time, e repensar como se contratam e se promovem pessoas. Dizer "sejam mais versáteis" e deixar cada um se virar sozinho não é suficiente. Se a versatilidade é o que vai gerar mais valor profissional (e eu acredito firmemente que é sim), então processos seletivos que exigem cinco anos de experiência em uma linguagem específica e avaliações de desempenho que só medem competências de forma muito estreita são contraproducentes e danosos.