# What I Learned About AI This Week

## Big Idea

This week, I started turning my AI learning into something more practical: a first AI-native workflow system. Instead of just experimenting with AI in small ways, I’m now building a system that can capture what I learn, organize it, summarize it, and share it in a simple way that family can understand.

What makes this exciting is that it combines several skills I already have, like PowerAutomate, JSON, workflow orchestration, and systems thinking, with newer AI ideas like structured outputs, memory systems, and AI-assisted publishing. In other words, I’m not just learning about AI — I’m learning how to build with it.

## What I Explored

I explored two connected ideas this week:

First, I thought about building a personal AI workflow that can take a learning note and turn it into a clear summary. This would help me track my progress and make it easier to share updates regularly. It’s a simple idea, but it’s also a strong foundation for learning AI orchestration and automation.

Second, I worked through how to build a more structured AI learning and research system. That included:
- using markdown files as input,
- generating summaries in JSON,
- storing memory in a timeline file,
- and monitoring outside sources like Microsoft articles with RSS feeds.

I also learned that AI summaries become much more useful when the input is richer and the output is structured. For example, if I want a summary to be useful for IT professionals, the prompt should ask for enterprise impact, architecture, governance, integration points, and operational concerns — not just a general recap.

Another useful lesson: if the watcher says “no new article found,” that probably means it already saw the latest URL and stored it in `seen_articles.json`. That kind of memory makes the system smarter and prevents repeated work.

## Simple Explanation

I’m building a smart helper that can collect what I learn, turn it into easy-to-read summaries, and share those updates with my family.

It can also keep track of articles I’ve already seen, so it doesn’t repeat itself. Think of it like a helpful digital assistant that reads, remembers, organizes, and explains things for me.

## Why This Matters

This matters because it’s helping me move from casually using AI to actually designing AI systems.

Instead of asking AI one question at a time, I’m learning how to create workflows that can:
- follow a process,
- remember past information,
- pull in new data automatically,
- and produce consistent, useful results.

That’s a big step toward real AI literacy and practical AI building. It also helps me improve my ability to think in systems, which is useful far beyond AI.

## Real-World Use Case

A real-world version of this could help an IT professional monitor Microsoft blogs automatically.

The system could:
- detect when a new article appears,
- fetch the article text,
- summarize it with an enterprise focus,
- store both markdown and JSON versions,
- and optionally publish the result to a knowledge site or team journal.

That means less manual reading and note-taking, and more time spent on understanding what actually matters.

## What I’m Trying Next

Next, I want to improve the workflow so it can be tested more easily and run on demand when needed.

My next steps are:
- add a test or force mode to the watcher,
- make it possible to reprocess articles manually,
- and eventually schedule it so it runs automatically.

That will help me keep building a system that is both useful and reliable.