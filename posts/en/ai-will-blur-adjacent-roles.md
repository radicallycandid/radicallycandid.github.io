---
title: "AI Will Blur Adjacent Roles, Not Dissolve All of Them"
date: 2026-03-01
excerpt: The "Product Builder" narrative gets it half right. AI does enable people to take on broader responsibilities. But the roles won't collapse into one.
draft: true
---

## The Product Builder narrative

There's a growing narrative in tech that AI will dissolve the boundaries between product development roles entirely. Product Managers, Software Engineers, Product Designers, Data Scientists — in this view, all of these are on their way to merging into a single role, often called the "Product Builder." Brian Balfour has written about how AI could restore the magic of early-stage startups, where everyone does a bit of everything. Microsoft's LinkedIn famously restructured around "full stack builders." The idea is seductive: AI lowers the barriers to entry in every discipline, so why not have everyone do everything?

This narrative gets something right. AI does make it possible for individuals to stretch into areas that were previously out of reach. A Product Manager can now prototype a working interface. A designer can generate functional code. An engineer can analyze data without deep SQL expertise. The barriers are genuinely lower than they've ever been.

But the conclusion that all roles will converge into one doesn't follow. It overestimates how far people can stretch, and it underestimates the depth required to do any of these jobs well.

## Specialization, coordination, and where the equilibrium shifts

The degree of role specialization in any organization is not arbitrary. It's the result of a tension between two forces. On one side, specialization creates value: a dedicated Back-End Engineer knows things about distributed systems that a generalist never will, and a Product Designer understands interaction patterns that an engineer shouldn't be expected to master. Deeper expertise means better decisions.

On the other side, specialization carries a cost: coordination between people. Every time a responsibility is split across two people, you introduce handoffs, misunderstandings, meetings, and delays. In a small startup, the cost of this coordination often exceeds the benefit of having specialists, which is why early-stage teams naturally tend toward generalism.

AI changes the balance of this tension. By lowering the barrier to competence in adjacent skills, AI makes it viable for one person to take on work that previously required two. When one person can do the work that previously required two to coordinate, organizations may choose to have fewer, broader roles — not because specialization has lost its value, but because the coordination cost of maintaining fine-grained specialization is no longer worth paying in every case.

This is a real shift, but it's a shift at the margins. It pushes people toward being somewhat more generalist, not toward being fully generalist. The "Product Builder" narrative takes a real observation — the barriers are lower — and extrapolates it to an unrealistic conclusion: that the barriers will disappear.

They won't. People have natural dispositions, cognitive styles, and professional identities that make them better suited to some roles than others. The depth required to excel at Product Management is fundamentally different from the depth required to excel at Software Engineering. AI can help you become passable at an adjacent discipline. It cannot make you world-class at everything.

## The adjacent roles graph

Instead of the "Product Builder" model, I want to propose a more realistic framework for thinking about how AI will reshape professional roles in the short term — over the next few months to a few years.

Consider the different specializations that exist in a modern product development organization. These roles are not all equally close to one another. A Front-End Engineer and a Product Designer work in overlapping territories every day. A Front-End Engineer and a Data Platform Engineer almost never do. The distance between roles matters.

<div class="graph-embed">
  <iframe src="/static/embeds/professions-graph-en.html?embed" title="Professions adjacency graph"></iframe>
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

This is what I call the adjacent roles graph. Each node represents a role that exists in many organizations today. The edges connect roles that are naturally close to one another — roles where the knowledge, skills, and daily work overlap significantly.

My thesis is simple: AI will gradually blur the boundaries between adjacent roles in this graph, without eliminating the roles themselves. The blurring will happen along the edges, not everywhere at once. A Product Designer will find it easier to take on Front-End Engineering work. An Analytics Engineer will absorb some of what Business Analysts do today. But a Product Designer will not suddenly become a Data Platform Engineer. The distance is too great.

## What this means for your career

If you currently occupy a single node in this graph, you face a real risk — with some exceptions, typically tied to very specific business contexts (like credit risk) or to very senior individuals whose depth of expertise is itself irreplaceable. For most professionals, staying in a single node means that someone who can do your job *and* part of an adjacent one will be more valuable to employers.

My strong recommendation is to extend your skills toward an adjacent node. Not a distant one. Not three at once. Pick the neighbor that interests you most and that complements your current strengths, and build genuine competence there.

If you're already consolidated across two adjacent nodes, it is viable to reach for a third — but I'd caution that this is genuinely hard. The skills and even the psychological makeup required across three nodes are often quite different. Those who manage it will be exceptionally valuable, but it will remain rare.

I would not recommend aiming for four or more, and I would specifically advise against jumping to distant nodes. Traverse the graph along its edges. The value comes from combining adjacent skills, where the overlap creates something greater than the sum of the parts.

## Combinations that already have names

Some of these adjacent-role combinations are already well established, and it's worth looking at them as examples of what this graph predicts.

**Software Engineer** (Front End + Back End). This is perhaps the most mature example. The "full stack" engineer has existed for years, and the trend is that this will simply become the default meaning of "Software Engineer." Some already call this a Product Engineer.

**Design Engineer** (Product Designer + Front-End Engineer). This is a role that's gaining real traction. Someone who can both design an interface and build it, closing the gap between design intent and implementation.

**Data Engineer** (Data Platform Engineer + Analytics Engineer). Someone who can both build the infrastructure for data at scale and model the data for consumption. The combination eliminates a handoff that has historically been a source of friction.

**Decision Scientist** (Data Scientist + Business Analyst). Someone who combines statistical and machine learning expertise with business context and communication skills. Less focused on model building for its own sake, more on driving decisions.

**Analytics Engineer** of the future (Analytics Engineer + Business Analyst). As the tools for data modeling become more accessible, the Analytics Engineer naturally absorbs the analyst's role of making data ready for decision-making.

**Data Scientist** of the future (Data Scientist + Analytics Engineer). A Data Scientist who also owns the data transformation and modeling layer, rather than depending on a separate team to prepare the data.

Not every combination has a name yet, and that's fine. A Product Manager who absorbs the Business Analyst's depth is still a Product Manager — just a more analytically grounded one. The combination of Product Manager and Engineering Manager is one of the most interesting mergers that could emerge, though I'm honestly not sure what to call it. It's also one of the hardest, because the profiles and dispositions of people who gravitate toward these two roles tend to be quite different.

For Engineering Managers, the trend toward smaller teams means less people-management overhead and more room for hands-on technical contribution. The "hands-on Engineering Manager" or Tech Lead who codes alongside the team is a natural expression of this shift — and one I see very favorably, because staying close to the code makes the EM better at the rest of her job too.

## The edges, not the center

The "Product Builder" narrative imagines a future where all roles collapse into the center of the graph. I think what will actually happen is more interesting and more realistic: the edges will get thicker. Adjacent roles will increasingly overlap. People will stretch, selectively and deliberately, toward the nodes next to them.

This isn't the story of specialization dying. It's the story of specialization becoming a little less narrow, one edge at a time.
