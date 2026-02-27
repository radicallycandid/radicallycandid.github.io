---
title: "EM and PM in product teams: who drives what"
date: 2026-02-27
excerpt: "When the PM has to keep asking 'when will it ship?', that's a symptom of dysfunction."
---

## Delivery management is the EM's responsibility

In a cross-functional product development team, the Engineering Manager (EM) has three primary responsibilities. These are not her only relevant contributions to the team, but they are what she is ultimately accountable for.

The first is technical decision-making. Should we use queues, topics, or both? Synchronous or asynchronous communication? How many services, organized in what ways? Even when recommendations on these decisions come from individual contributors, the EM is still responsible for the quality of the final decisions. She can delegate part of the work needed to reach a decision, or even most of it, but she cannot delegate the responsibility for the decision itself.

The second is delivery process management. Are we going to deliver what we committed to, at the expected pace and quality? If it looks like we'll miss a deadline, is there anything we can do to prevent the delay? If the delay itself is unavoidable, what trade-offs does it force on other deliveries? How can we reduce cycle time and increase throughput? Is there a bottleneck in the code review process? The EM should be well positioned to handle these problems by definition, since she manages the individual contributors who do the actual work.

The third is people leadership and development. Do I have the team I need, with the right people in the right roles? How can each person on the team grow? How do you ensure the right level of challenge and psychological safety at the same time? The EM is responsible for ensuring the team has the competencies needed to execute well, and for developing those competencies over time. This includes difficult decisions: identifying who is ready to take on more responsibility, who needs more support, and who may not be in the right place. This is a difficult but critical part of the job.

These are the EM's main responsibilities, but not the only ones. For example, the ability to influence the product roadmap is often what distinguishes good vs. great Engineering Managers. The EM is the person best positioned to have up-to-date, deep knowledge of the team's tech debt inventory, architectural bottlenecks, and developer experience limitations that affect delivery capacity. If services are too fragmented or CI tests are slow, delivery gets harder regardless of how well the team is managed day to day. This perspective needs to feed into roadmap decisions. A plan that ignores tech debt is bound to accumulate problems down the line, and the EM has an obligation to make that visible.

## If the PM is chasing deadlines, something is wrong

This division of responsibilities has implications for the Product Manager (PM) role.

In strong teams, the PM doesn't need to be heavily involved in the team's day-to-day operations to ensure delivery, precisely because the EM handles it. This frees the PM to focus on what she is best positioned to do: understanding the problem deeply from the perspective of customers and the business, defining priorities several months out, and looking outside the team. How can we increase product adoption without requiring a high-touch effort? What product changes would be needed to enter a new segment? How can we work with Operations and Product Marketing to make initiatives succeed?

In weaker teams, something different happens. The PM ends up taking on delivery process management: flagging delays, driving cadence, chasing deadlines, putting together status reports. When the PM has to keep asking "when will it ship?", something is wrong. That's not Product Management. That's project management, and it should sit with the EM.

This pattern is typically associated with two factors. The first is EMs who lack the skills to fully own their delivery role. The second is PMs who aren't senior or strategic enough to fill the space they should be filling. The result is that nobody does either thing well. The PM fills a vacuum, but stops doing the work of looking ahead and outside the team. The EM loses ownership and settles into a smaller role. This problem hurts the products, the customers, and the business.

If I had to pick a single leverage point to improve most product teams I've seen, it would be the maturity of Software Engineering leadership. Not because Product Management doesn't have its own problems. But because when the EM is strong, the PM can finally do the work she should have been doing all along. (And if she can't, that gets exposed in a way that wasn't necessarily visible before.)

## This doesn't mean the PM should be hands-off

There's a distinction I want to make clear: none of this means the PM can ignore the details of execution.

Knowing what's happening is expected of all leaders, across all disciplines. Just because delivery management is Software Engineering's responsibility doesn't mean PMs can afford not to understand what's being built, not to question decisions, not to be involved in discussions. A PM's level of knowledge about an important initiative on her team should never be "all I know is it's in dev."

Think about a critical feature in your product that's slow, has significant usability issues, or regularly generates user complaints. Who needs to know the diagnosis, the action plan, and how the team is progressing? All leaders need to know. The EM needs to know, the PM needs to know.

The distinction is between who drives and who stays informed. The EM drives delivery management. The PM stays informed, questions, and contributes. If the PM has to drive it, as is common in less mature teams, that's a symptom of dysfunction. The first step toward fixing the problem is almost always the same: strengthen the EM and expect more from her.
