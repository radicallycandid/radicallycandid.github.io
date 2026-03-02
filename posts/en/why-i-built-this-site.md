---
title: "Why I Built This Site from Scratch"
date: 2026-03-01
draft: true
excerpt: I wanted the simplest, most durable personal site I could build. So I wrote my own generator with the help of Claude Code.
---

## The Question

I've been asking myself this for a while: what's the simplest, most elegant, and most durable way to have a personal site?

When I look at personal sites I admire, like Paul Graham's and Gwern's, what stands out is what's absent. No JavaScript framework. No CMS. No build pipeline with fifteen dependencies. Just pages that load instantly and will keep working ten years from now.

## Why Not Use an Existing Generator

Hugo, Jekyll, Gatsby, Next.js. These tools exist and they work. I could have picked any of them. But every time I sat down to evaluate one, I ran into the same feeling: it's more complexity than I need.

I don't want to learn how to configure a framework. I don't want to adapt to a folder structure someone else decided. I don't want to depend on an ecosystem that might change direction or get abandoned.

What I want is simple: take Markdown files and turn them into HTML. That's it.

## Claude Code's Role

This is where the story gets more honest. I've been close to programming for over a decade, but I'm a VP at a company. My day-to-day is not writing code. I know enough to read, review, and test, but building an entire site generator on my own would have been a time investment that would probably have made me give up.

Claude Code made it viable. Not just through capability, but through energy: when the barrier between an idea and its execution drops far enough, you actually do the thing. The entire generator (the build script, the templates, the custom CSS) was built with it. I'd define what I wanted, review what it produced, test it, ask for adjustments. The result is a Python script of about 1,200 lines that does exactly what I need and nothing more.

But the most interesting part wasn't saving time. It was learning. Building a generator from scratch, even with AI assistance, taught me how these tools actually work under the hood. Parsing frontmatter, converting Markdown to HTML, applying templates, generating Atom feeds. I understood all of this superficially before and now understand it for real.

## Tufte

The visual choice is not accidental. I first encountered Edward Tufte reading *The Visual Display of Quantitative Information* in college. That book changed how I think about data and communication. His ideas (information density, minimizing chart junk, letting the data speak) were foundational to my career as a data scientist, and later, when I took on design leadership at the company where I work.

Tufte CSS translates part of that philosophy to the web. Sidenotes and margin notes appear in your field of vision without interrupting the reading flow.{mn}Footnotes force a decision: is this worth breaking my reading flow? Sidenotes remove that friction. The information is there if you want it.{/mn} It's a choice that reflects how I think text should be consumed.

## Why Bilingual

Portuguese is my native language, but I see very little quality content in Brazilian Portuguese about the topics I care about. At the same time, I wanted what I wrote to be read by people in my own organization, Arco Educação, and also be accessible to those who don't speak Portuguese.

It's more work, yes. But writing in both languages forces me to think more carefully about what I'm saying. When a sentence doesn't translate well, it's usually because the idea isn't clear enough.

## Speed Matters

The site has to be fast. Not "fast for a blog". Actually fast. Pages that load instantly. No unnecessary JavaScript. No external requests blocking rendering.

A slow site disrespects the reader's time. And a personal site, which doesn't have the excuse of product complexity, has no reason to be slow.

## The Result

I'm proud of what came out. It's simple. It's beautiful. It has dark mode. It's bilingual. It loads instantly. And I understand every part of the code that generates it.

It's exactly what I wanted.
