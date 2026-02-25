---
title: "Engineering Management and Product Management: who drives what"
date: 2026-02-25
excerpt: "In product teams, delivery management is the EM's responsibility. When the PM has to drive it, that's a symptom, not a solution."
---

## Delivery management is the EM's responsibility

In product teams, Software Engineering leadership has three primary responsibilities.

The first is technical decision-making. Should we use queues or topics? Synchronous or asynchronous communication? How many services, organized in what ways? Even when recommendations on these decisions come from individual contributors, Software Engineering leadership is still responsible for the quality of the final decisions. It can delegate part of the work needed to reach a decision, or even most of it, but it cannot delegate the responsibility for the decision itself.

The second is delivery process management. Are we going to deliver what we committed to, at the expected pace and quality? If it looks like a delivery will be late, is there anything we can do to prevent the delay? If the delay itself is unavoidable, what trade-offs does it force on other deliveries? How can we reduce cycle time and increase throughput? Software Engineering leadership should be well positioned to handle these problems by definition, since it manages the individual contributors who do the delivering.

The third is people leadership and development. Do I have the team I need? Are the right people in the right roles? How can each person on the team grow? Software Engineering leadership is responsible for ensuring the team has the competencies needed to execute well, and for developing those competencies over time. This includes difficult decisions: identifying who is ready to take on more responsibility, who needs more support, and who may not be in the right role. Teams that deliver consistently almost always have a strong EM in this dimension. That's not a coincidence.

These are the primary responsibilities. But there are other contributions expected of an EM, even if they're not exclusively hers. The most important one is probably influence over the roadmap. The EM is the person best positioned to have up-to-date, deep knowledge of the team's tech debt inventory, architectural bottlenecks, and infrastructure limitations that affect delivery capacity. If the architecture is in bad shape or CI/CD is broken, delivering gets harder regardless of how well the team is managed day to day. This perspective needs to feed into roadmap decisions. A roadmap that ignores tech debt is a roadmap that's accumulating problems for the future, and the EM has an obligation to make that visible.

## If the PM is chasing deadlines, something went wrong

What does this division of responsibilities mean for Product Management leadership?

In strong companies, the PM has little involvement in the team's day-to-day operations, precisely because the EM handles it. This frees the PM to focus on what only Product Management can do: deeply understanding the problem, setting priorities on a quarterly and yearly horizon, and looking outside the team. How do we expand product adoption? How do we enter a new segment? What's the right competitive positioning?

In weaker companies, something different happens. The PM ends up taking on delivery process management: flagging delays, driving cadence, chasing deadlines, putting together status reports. When the PM is the one asking "when will it ship?", something went wrong. That's not Product Management. That's project management, and it should sit with the EM.

This pattern is typically associated with two factors. The first is EMs who aren't fully stepping into their role when it comes to delivery. The second is PMs who aren't senior or strategic enough to fill the space they should be filling. The result is that nobody does either thing well. The PM covers for the EM and neglects the strategic work. The EM loses ownership and gets comfortable. And no matter how hard the PM tries to compensate, it doesn't fix the underlying problem. In the end, the answer is almost always to strengthen the EM, not to ask more of the PM.

If I had to pick a single leverage point to improve most product teams I've seen, it would be the maturity of Software Engineering leadership. Not because Product Management doesn't have its own problems. But because when the EM is strong, the PM can finally do the work she should have been doing all along.

## Staying informed is not the same as being hands-off

There's a distinction I want to make clear: none of this means the PM can ignore the details of execution.

From an information standpoint — knowing what's happening, keeping up with the state of things — that's expected of all leaders, across all disciplines. Just because delivery management is Software Engineering's responsibility doesn't mean PMs can afford not to understand what's being built, not to question decisions, not to be involved in discussions. A PM's level of knowledge about an important initiative on her team should never be "all I know is it's in dev."

Think about a critical feature in your product that's slow, has usability issues, and generates frequent user complaints. Who needs to know the diagnosis, the action plan, and where we are in the plan? All leaders. The EM needs to know. The PM needs to know. The designer needs to know.

The distinction is between who drives and who stays informed. The EM drives delivery management. The PM stays informed, questions, and contributes. But if the PM has to drive it, that's a symptom, not a solution.
