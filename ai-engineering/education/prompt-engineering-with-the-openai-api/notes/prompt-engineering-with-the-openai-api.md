# Prompt Engineering with the OpenAI API

> Study notes based on the four supplied DataCamp chapter PDFs. The course demonstrates Chat Completions. Current API notes are called out where newer features or guidance affect how to apply the concepts in a project.

## Learning goals

- Write clear prompts with an explicit task, context, constraints, and output requirements.
- Use delimiters to separate instructions from source text.
- Request structured, conditional, and multi-step outputs.
- Choose between zero-shot and example-based prompting.
- Improve prompts through iteration and representative examples.
- Apply these techniques to summarize, transform, analyze, and expand text, and to generate or explain code.
- Design chatbot instructions and provide relevant external context.

## 1. What prompt engineering is

Prompt engineering is the practice of shaping instructions and context so a model is more likely to produce a useful response. Think of it as specifying a task for a capable but literal collaborator: the model needs to know what to do, what information to use, what constraints matter, and what a successful answer looks like.

A reusable prompt often contains:

1. **Task:** a direct action verb such as summarize, classify, translate, extract, compare, or rewrite.
2. **Context:** relevant background, audience, or domain information.
3. **Input:** the text, code, or data to work on.
4. **Constraints:** what to preserve, avoid, or limit.
5. **Output requirements:** format, length, tone, and level of detail.

Example:

```text
Task: Summarize the customer review.
Focus: Product features and user experience.
Output: At most three bullets for a product manager.
Preserve: Do not add claims that are not present in the review.

<review>
The customer review goes here.
</review>
```

## 2. Be specific and delimit the input

Vague verbs such as “think about” leave the task open to interpretation. Use an action verb that describes the result you need. Replace “Tell me about dogs” with a bounded request such as “Compare Golden Retrievers and Labradors as family pets in one paragraph, covering temperament and exercise needs.”

Specify details that commonly change the result:

- Topic or question
- Audience and assumed background
- Scope and facts that must be retained
- Output length and format
- Tone or style
- What to do if information is missing or a condition is not met

Separate instructions from source material with clear delimiters such as Markdown headings, XML tags, or triple backticks. Tell the model what the delimiters contain. Python f-strings are a convenient way to insert variable text:

```python
prompt = f"""Summarize the source text in three bullets.
Do not infer facts that are not stated in the source.

<source_text>
{text}
</source_text>
"""
```

Delimiters make the prompt easier to read and help distinguish instructions from data. They are not a security boundary: source text may itself contain hostile or irrelevant instructions. Treat untrusted input as data, and enforce important restrictions in application logic as well.

### Length and format

A natural-language instruction such as “one sentence” expresses the desired shape. An API token limit is a hard ceiling, but a ceiling that is too small can truncate an answer. Use both when appropriate: describe the intended length in the prompt and set a reasonable output limit supported by the chosen model and endpoint.

A prompt can request a table, list, headings, or named fields. For a human-readable answer, this may be enough. For machine-readable output that must match a schema, use the API's Structured Outputs feature when supported instead of relying only on a prose instruction to return JSON.

## 3. Conditional prompts

A conditional prompt describes branches, similar to `if` / `else` logic:

```text
If the input is in English, summarize it in two bullets.
Otherwise, return the label "unsupported_language".
```

State the conditions and every expected outcome explicitly. For application behavior that must be dependable, implement deterministic checks in code where possible, then use the model for the language task. Do not rely only on a prompt for access control, policy enforcement, or other critical decisions.

## 4. Zero-shot, one-shot, and few-shot prompting

A **shot** is an example of the behavior you want:

- **Zero-shot:** instructions only. Start here for simple, well-defined tasks.
- **One-shot:** one example, often enough to demonstrate a desired format or style.
- **Few-shot:** several examples, useful when a task depends on a specific label scheme or nuanced pattern.

Use examples that are correct, representative, and consistent with the requested output. Include meaningful edge cases when the task has them. More examples are not automatically better: they use context and can introduce noise. Try a small set first, then add examples only when evaluation shows a gap.

For classification, define the label meanings and include borderline cases. Otherwise the model may apply a different interpretation of labels than your application expects.

## 5. Multi-step instructions and reasoning

A multi-step prompt decomposes the task into explicit stages. It is useful when the order matters, such as extracting facts, checking them against a source, then formatting a short report. This differs from few-shot prompting: steps state what to do; examples demonstrate what a good input-output mapping looks like.

The course also introduces chain-of-thought prompting and self-consistency, including asking for reasoning steps and comparing multiple answers. Treat those as course concepts, not a default production recipe. Current OpenAI guidance for reasoning models is to avoid asking them to “think step by step”; they reason internally. Ask for the deliverable you need, such as a concise answer, a short explanation, or a summary, and verify the result. If the task needs higher confidence, use independent checks, tests, or multiple evaluated samples rather than trusting a model-generated vote by itself.

## 6. Iterate and evaluate

A first prompt is a hypothesis. Improve it with a loop:

1. Write the simplest prompt that states the task and success criteria.
2. Try it on representative inputs, including edge cases.
3. Inspect failures: Was the task ambiguous? Was context missing? Did output shape drift?
4. Change one important thing at a time, such as instructions, examples, or format.
5. Compare results against expected outputs or evaluation criteria.
6. Keep the version that works reliably across the set, not just one appealing example.

Examples from the course show that a request for an “Excel sheet” may work better when reframed as a copyable table, and that a classifier may need an “unknown” category for non-weather uses of words like “stormy.”

## 7. Applying prompts to common tasks

### Summarization and expansion

For summaries, specify the focus, audience, length, and format. For expansion, provide the source ideas and specify what detail to add, along with tone and a length limit. Ask the model not to invent details when source fidelity matters.

### Text transformation

For translation, name the source and target languages. For proofreading, say whether to preserve the original structure or improve it. For tone changes, name the target audience and tone. When requesting several transformations, list them in order and say whether the output should show intermediate versions or only the final one.

### Text analysis

For sentiment or other classification, provide a closed list of labels and request the exact output shape. For entity extraction, name the fields to extract and specify how missing values should be represented. Validate extracted details against the source before using them in a workflow. When processing customer data, account for privacy, legal, and organizational requirements.

### Code generation and explanation

When asking for code, specify the problem, programming language, desired shape (function, class, or script), inputs, outputs, and relevant edge cases. Input-output examples can clarify behavior. Read and run generated code in a controlled environment before relying on it. When asking for an explanation, state the intended detail level and audience.

## 8. Chatbot instructions and roles

The fourth chapter uses a system message to define a chatbot's purpose, tone, audience, response guidelines, and topic boundaries. It also explores role-play prompts, such as asking for the style of a customer support agent, product manager, or sales engineer.

A role can shape presentation and emphasis, but it does not give the model real expertise, private knowledge, or authority. Pair persona instructions with explicit task boundaries and the actual reference information the chatbot is allowed to use. Review sensitive or consequential answers.

The course's sample system messages are written for Chat Completions. In current Responses API examples, use `instructions` or a `developer` message for application-level guidance, and use user input for the specific request. Consult the selected endpoint's docs because request shapes differ.

## 9. Supplying external context

A model may lack private, recent, or organization-specific information. Supply the relevant approved facts, documents, or conversation context with the task, and say what the model should do if the answer is not supported by that context. For larger collections, retrieval or file search can select relevant passages instead of placing everything in every prompt.

More context is not always better. Include the smallest relevant source, keep track of where facts came from, and make it possible to check the answer against the source. Context can ground a response, but it does not guarantee truth or freshness.

## Practical prompt template

```text
## Role
[Relevant perspective, if useful]

## Task
[One clear action]

## Context
[Only facts needed to do the task]

## Input
<source>
[Untrusted or task-specific input]
</source>

## Constraints
- [What to preserve or avoid]
- [How to handle missing or unsupported information]

## Output
[Format, length, tone, and audience]
```

Keep template fields only when they help this specific task. A shorter prompt is often better when it is already precise.

## Key takeaways

- Clear action verbs and concrete success criteria reduce ambiguity.
- Separate task instructions from input data and specify the output shape.
- Delimiters improve organization but do not neutralize malicious instructions inside untrusted input.
- Use zero-shot first; add accurate and diverse examples when needed.
- Multi-step prompts describe actions; few-shot prompts demonstrate examples.
- Iterate against a representative evaluation set instead of optimizing for one output.
- Use schema-constrained output for strict machine-readable formats when supported.
- Personas and instructions guide style; they do not ensure accuracy or enforce critical rules.
- Provide relevant external context, then verify outputs against it.

## Sources

### Course material

- [Chapter 1 PDF](../pdfs/chapter-01.pdf)
- [Chapter 2 PDF](../pdfs/chapter-02.pdf)
- [Chapter 3 PDF](../pdfs/chapter-03.pdf)
- [Chapter 4 PDF](../pdfs/chapter-04.pdf)

### Current OpenAI documentation

- [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)
- [Reasoning best practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices)
- [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [Safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
