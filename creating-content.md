---
title: Guidelines for creating content
author: Jason Lowe-Power
---

This file describes how to create content for the bootcamp.

## Requirements

- Use markdownlint. We can ignore MD013 (line length) and MD026 (punctuation at end of headers).
- Install pre-commit and use that when using git.
- Use yaml frontmatter for title and always include an author

## Suggestions for creating content

- Keep code snippets short
  - Each snippet should fit on a slide
  - A good rule of thumb is about 10 lines at most
  - You can have an example that spans multiple snippets
  - Talk about each code snippet on its own
- Keep the theory part short
- Think about ways to keep things interactive

Inspiration:

- [Learning gem5](https://www.gem5.org/documentation/learning_gem5/introduction/) and the [old version](http://learning.gem5.org/).
- [Standard library docs](https://www.gem5.org/documentation/gem5-stdlib/overview)

## How to provide/use code

- We are planning on using google codespaces.
  - We will provide the template repo to work on soon.
- Put boilerplate in the template repo.

## Things that were effective at teaching

- Lots of template code and just leave empty the main point that you were trying to learn.
- Copying code from a book into the terminal and make minor modifications to see what happens.
- Small short code snippets to write.
- It's helpful to have a site map for the directory structure.
- Youtube videos writing the code live line-by-line and explaining things.
- Having a big project with a specific goal in mind which touches the things you want to learn.
- Listening to someone else's thought process while they are working on the problem
- Take working code and then break it to see what errors happen.
- Someone provides a library with APIs and you have to implement the APIs and it's tested heavily outside.
- Extend someone else's (simple) code with some specific goal in mind.
- Code under very specific constraints so that you don't get lost in the forest.
- Pair programming
- Taking the code and then pulling out the state machine / structure.
  - Build your own callgraphs
  - Use gdb in a working example
- The socratic method. Have them try something and then help them move toward the "best" solution.
- Make sure to point out how gem5 differs from real hardware. Gap between theory and model.
- Keywords: repeat many times and have a glossary.
- Focus on one module. Ignore the others except for the interfaces. **Write detailed comments/notes**
- Make sure that c-scope/c-tags are enabled.
- Practice and do "it" yourself.
