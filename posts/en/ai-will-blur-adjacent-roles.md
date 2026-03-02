---
title: "AI Will Blur Adjacent Roles, Not Dissolve All of Them"
date: 2026-03-01
excerpt: The "Product Builder" narrative gets it half right. AI does enable people to take on broader responsibilities. But the roles won't collapse into one.
---

## The Product Builder Narrative

There's a growing narrative in tech that AI will dissolve the boundaries between product development roles entirely. In this view, Product Managers, Software Engineers, Product Designers, and other roles are all converging into one, often called the "Product Builder." If you work in tech and have been using tools like Claude Code to accomplish far more than you could before, this prediction feels both exciting and obvious. Concrete steps by companies like [LinkedIn](https://www.youtube.com/watch?v=R-zCfLQD_84) reinforce the thesis, the term already has its own [manifesto](https://productbuilder.community), and the idea that the division between "who understands the problem," "who designs the interface," and "who writes the code" is unnecessary overhead is being [articulated explicitly](https://labs.adaline.ai/p/redesigning-product-work-for-the-ai-era-in-2026).

This narrative gets something important right. AI really does make it possible for people to stretch into areas that were previously out of reach. A Product Manager can now prototype a working interface. A Product Designer can generate functional code outside of Figma. People across disciplines can analyze data without deep SQL expertise. For anyone with curiosity and initiative, the barriers are lower and the boundaries more fluid than they've ever been.

Still, I don't think it follows that all roles will converge into one, at least not in large, mature companies. This view overestimates people's capacity for cognitive and psychological adaptation, and underestimates the depth required to do any of these jobs well in a professional context.

## Why Different Roles Exist

The degree of role specialization in any organization isn't arbitrary. It's actually the result of a tension between two forces. On one side, specialization creates value: a Back-End Engineer knows how to solve distributed systems problems that would give a generalist serious headaches, and a Product Designer understands interaction patterns in ways you can't reasonably expect from an engineer. Greater depth leads to better decisions and better products.

On the other side, specialization has an important cost: coordination between people. Every time a responsibility is split across two people, you get handoffs, miscommunication, meetings, and delays. In a small startup, the cost of that coordination often exceeds the benefit of having specialists, which is why early-stage teams naturally lean toward generalist profiles. This is also part of why some people who thrive in small startups sometimes struggle as those companies grow.

Increasingly capable AI tools and agents can shift where the sweet spot of this trade-off lies. By lowering the barrier to competence in adjacent skills and making self-directed learning easier, they make it viable for one person to take on work that previously required two. When a single person can do what used to demand coordination across a small group, companies may opt for broader, fewer roles. When that happens, it's not because specialization has become useless. It's because the coordination cost of maintaining a very fine-grained division of roles is no longer worth it.

This shift feels real to me, and highly relevant to our careers. But in the short term (say, less than two years), I expect a less dramatic transformation than the "Product Builder" narrative suggests. In other words, in 2026 and 2027, I still believe we'll be talking about Software Engineers, Product Designers, and so on. People who predict a complete merger of disciplines seem to miss that people have natural inclinations, cognitive profiles, and professional identities that make them better suited to some roles than others.

## The Adjacent Roles Graph

Instead of the "Product Builder" model, I want to propose a more realistic framework for thinking about how AI will reshape professional roles over the next few months to a few years.

<label for="mn-agi" class="margin-toggle">&#8853;</label>
<input type="checkbox" id="mn-agi" class="margin-toggle"/>
<span class="marginnote">My predictions don't apply to a post-AGI world. That's probably the best criticism of what I'm proposing here: after all, AI capabilities have been advancing impressively fast. Then again, this weakness isn't unique to me: which predictions about the current world are robust enough to survive AGI?</span>

Consider the different roles that exist in a modern product development organization. These roles are not all equally close to one another. A Front-End Engineer and a Product Designer work in overlapping territory every day. That same Product Designer, on the other hand, has little in common with a Data Platform Engineer in terms of responsibilities and skills. The distance between roles matters.

The graph below shows common roles and what I consider their most relevant adjacencies. It's intentionally simple and not exhaustive, prioritizing usefulness for the argument that follows.{mn}For instance, the graph doesn't include Site Reliability Engineer (SRE), which would be a node connected to SW Engineer (Back End), or the emerging and increasingly relevant role of AI Engineer, which could connect to both Data Scientist and SW Engineer (Back End).{/mn} The inclusion of several data-related roles (Data Platform Engineer, Analytics Engineer, Data Scientist, Business Analyst) reflects both my personal background and the fact that the conversation with a friend that inspired this post started by questioning how these roles are divided today.

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

<label for="mn-depth" class="margin-toggle">&#8853;</label>
<input type="checkbox" id="mn-depth" class="margin-toggle"/>
<span class="marginnote">AI also compresses the depth required within each specialty, not just the barriers between them. But this compression is asymmetric: agents automate execution far more than they replace judgment. The real difference between roles lives in the judgment of knowing what (not) to build and what's wrong even when it looks right.</span>

My argument is simple: AI will gradually blur the boundaries between adjacent roles in this graph, without eliminating the roles themselves. The blurring will happen along the edges, not everywhere at once. A Product Designer will find it easier to take on Front-End Engineering work. An Analytics Engineer will absorb some of what Business Analysts do today, or vice versa. What I don't foresee is the rise of professionals who simultaneously perform a large collection of distant roles in this graph.

## What This Means for Your Career

I'll be completely honest, knowing that some people who work in the organization I lead will read this. If you currently occupy a single node in this graph, I believe you face a real professional risk. (There are some exceptions, usually tied to very specific business contexts, like credit risk, or to very senior individuals whose depth of expertise is itself hard to replace.) For most professionals, staying in a single node means that someone who can do your job *and* at least part of an adjacent one will be more valuable to employers. While this was already true before, it's dramatically amplified by AI.

I strongly recommend extending your skills toward an adjacent node. Pick the neighbor that interests you most or best complements your current strengths, and build genuine professional competence there as soon as you can.

If you're already established across two adjacent nodes, it's viable to aim for a third, but I'd warn that this is genuinely hard. The skills and even the psychological profile required across three nodes are often quite different from one another. Those who manage it will be exceptionally valuable, but it will remain rare.

I wouldn't recommend aiming for four or more, and I'd specifically advise against jumping to distant nodes. Traverse the graph along its edges. The greatest value comes from combining adjacent skills, where the overlap creates something greater than the sum of the parts.

## Role Combinations in Practice

Some of these adjacent-role combinations already exist, and they're worth examining as examples of what this graph predicts.

**Full Stack Software Engineer** (FE + BE). This is probably the most mature example. The role has existed for years, and it's trending toward simply becoming the default meaning of "Software Engineer" (or, alternatively, [Product Engineer](https://posthog.com/blog/what-is-a-product-engineer)).

**Design Engineer** (FE + PD). This is a more recent and increasingly interesting role that's gaining traction at some of the most innovative companies in the world, including [Cursor](https://cursor.com/careers/design-engineer) and [Vercel](https://vercel.com/careers/design-engineer-us-5709080004). It's someone who can both conceive an experience and turn it into production code, closing the gap between design intent and implementation and eliminating a handoff that's often problematic.

**Data Engineer** (DP + AE). This hybrid role actually represents what used to be the default until a few years ago, when the data world split into "people who love Kafka and Airflow" vs. "people who love dbt." Or, "people who know a lot of Python and a little SQL" vs. "people who know a lot of SQL and a little Python." It's someone who can both build data infrastructure at scale and model data for consumption.

Other hybrid roles won't necessarily get new names. For example, the PM + BA combination may keep the title Product Manager, while the AE + BA combination may keep the title Analytics Engineer or adopt another existing one, depending on the company.

The possible combination of Product Manager and Engineering Manager (PM + EM) is one of the most interesting mergers that could emerge, though I honestly don't know what it should be called. In practice, it's a less obvious pairing than it might seem, because the profiles and dispositions of people who gravitate toward these two roles tend to be quite different. Still, when it works, it appears to be one of the combinations that generate the most value for companies.

Speaking of Engineering Managers: the trend toward leaner teams means less people-management overhead and more room for hands-on technical contribution. The "hands-on Engineering Manager" (e.g., EM + FE or EM + BE), who regularly codes alongside the team as part of their routine, is a natural expression of this shift. I see this as a positive in the cases where it's possible, because staying close to the code and experiencing what it's like to develop in a particular context (codebase, domain, etc.) makes the EM better at the rest of their job too.

## The Edges, Not the Center

The "Product Builder" narrative imagines a future where all roles collapse into the center of the graph. I think what will actually happen is less dramatic but more interesting: the edges will get thicker, and adjacent roles will increasingly overlap. People will be able to (and will face competitive pressure to) stretch toward adjacent nodes and become more hybrid professionals. The trade-off between specialization and coordination doesn't disappear in a world with increasingly capable AI, but the equilibrium points undoubtedly shift toward favoring more versatile professionals.

Those who hold leadership positions in product development organizations have a dual responsibility in the face of these changes. The first is to be honest about where things are headed, whether at their specific company or in the broader industry. That's what this post is trying to do. The second is to create the conditions for people to actually expand. That means, for example, investing in your team's learning and development, and rethinking how you hire and promote people. Telling people to "be more versatile" and leaving them to figure it out on their own isn't enough. If versatility is what will generate the most professional value going forward (and I firmly believe it is), then hiring processes that demand five years of experience in a specific language and performance reviews that only measure competencies in very narrow terms are counterproductive and harmful.
