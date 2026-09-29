# Working with the OpenAI API

> Study notes based on the three supplied DataCamp chapter PDFs. The course teaches the Chat Completions endpoint. The final section adds current API context so the examples are easier to apply in new projects.

## Learning goals

After these chapters, you should be able to:

- Explain what an API request and response are.
- Send text to an OpenAI model from Python and read the returned text.
- Use a model for transformation, summarization, generation, and classification.
- Guide outputs with instructions and examples.
- Keep conversation history for follow-up questions.
- Reason about token limits, usage, cost, and API-key handling.

## 1. What an API does

An API (Application Programming Interface) is a contract that lets one program request a service from another program. The client sends a request; the service processes it and returns a response. For the OpenAI API, a request typically identifies a model and includes input plus optional parameters. The response contains generated output and metadata such as usage.

A web interface such as ChatGPT is ready to use by a person. An API lets a developer call a model from code and connect it to an application or workflow.

### The basic request cycle

1. Create an API key in the OpenAI Platform.
2. Install and initialize the official SDK.
3. Choose an endpoint and model.
4. Send input and any supported options.
5. Read the generated output and inspect metadata when needed.

The course's Chat Completions example:

```python
from openai import OpenAI

client = OpenAI()  # Reads OPENAI_API_KEY from the environment.

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is an API?"}],
)

print(response.choices[0].message.content)
```

`messages` is a list of dictionaries. Each dictionary has a `role` and `content`. The SDK returns a structured object; for Chat Completions, `choices[0].message.content` is the first generated message's text.

### Protect the API key

Treat an API key like a password. Do not paste it into source code, commit it to Git, or expose it in browser-side code. Store it in an environment variable or a secrets manager. The Python SDK can read `OPENAI_API_KEY` automatically when creating `OpenAI()`.

## 2. Tasks you can ask a model to perform

The second chapter applies the same request pattern to common language tasks:

- **Question answering:** respond to a question using the supplied input.
- **Text transformation:** rewrite text while preserving specified facts, such as changing a person's name or job title.
- **Summarization:** compress a transcript or document to a requested length or format.
- **Generation:** create a tagline, product description, or other new text.
- **Classification:** assign labels, such as a sentiment score or category.

The quality of the result depends on the clarity of the instructions and the information provided. For transformations, state what may change and what must stay the same. For summaries, give the desired number of bullets or sentences. For classifications, define the label set and what each label means.

Example of a narrowly specified transformation:

```python
prompt = """Rewrite the text for a professional audience.
Keep all dates and product specifications unchanged.
Return only the rewritten text.

Text: {text}
""".format(text=source_text)
```

## 3. Tokens, output limits, and cost

A **token** is a unit used to represent text for a model. A token may be a whole word, part of a word, punctuation, or other text. Token counts are not the same as word counts. The prompt and generated output both use tokens.

A generation limit such as `max_completion_tokens` places an upper bound on generated tokens for Chat Completions. If the limit is too low, the answer may stop mid-sentence. A limit is a cap, not a guarantee that the model will use that many tokens.

API pricing depends on the model and usage categories. Input and output tokens can have different prices, and some models or features may have additional pricing rules. Prices change, so check the live pricing page before estimating a real project's cost.

For Chat Completions, the response includes actual usage. The course's cost example uses the requested maximum output limit as `output_tokens`; for an after-the-fact estimate, use the actual usage returned by the API instead:

```python
usage = response.usage
input_tokens = usage.prompt_tokens
output_tokens = usage.completion_tokens

estimated_cost = (
    input_tokens * input_price_per_token
    + output_tokens * output_price_per_token
)
```

`input_price_per_token` and `output_price_per_token` must match the selected model's current prices and units. The usage values describe what the request actually consumed; a maximum output setting only limits what it could generate.

## 4. Randomness and prompt examples

Model output is not guaranteed to be identical on every run. Where a model supports it, `temperature` adjusts sampling: lower values generally make output more focused, while higher values generally allow more variation. It is not a factuality control. Follow the selected model and endpoint's parameter support; some models do not accept every sampling option.

**Shot prompting** means including examples in the input:

- **Zero-shot:** instructions without examples.
- **One-shot:** one example.
- **Few-shot:** multiple examples.

Examples are useful when you need consistent labels, tone, or formatting. Keep examples correct and representative. A model can imitate mistakes or unwanted patterns in the examples.

## 5. Roles and instruction hierarchy

In the course's Chat Completions examples:

- `system` gives broad behavior or constraints.
- `user` provides the task and task-specific context.
- `assistant` represents prior model output; it can also be used to provide example turns.

For instance, a system instruction can ask for concise Python tutoring, while a user message asks one concrete programming question. An assistant example can demonstrate the desired answer style before the real question. This is a structured way to show examples instead of embedding all examples in one long user prompt.

Instructions are guidance, not a complete safety mechanism. Validate model outputs before using them in consequential workflows. Do not assume that a system message alone prevents misuse or guarantees correct answers.

## 6. Multi-turn conversations

The API does not automatically know the full history of separate requests unless conversation state is managed for the application. In the course's Chat Completions pattern, the client keeps a `messages` list and sends the relevant history again on each turn:

1. Append the user's new message.
2. Send the conversation messages.
3. Read the assistant's reply.
4. Append that reply to the history before the next turn.

```python
messages = [
    {"role": "system", "content": "You are a concise data science tutor."}
]

messages.append({"role": "user", "content": "Why is Python popular?"})
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)
assistant_text = response.choices[0].message.content
messages.append({"role": "assistant", "content": assistant_text})

messages.append({"role": "user", "content": "Summarize that in one sentence."})
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)
print(response.choices[0].message.content)
```

Conversation history consumes input tokens on later turns. Applications should decide how much history to retain, and should avoid sending irrelevant or sensitive information.

## 7. Applying the course to current projects

The PDFs use Chat Completions, which is valuable for learning the request/response pattern and message roles. OpenAI's current quickstart uses the **Responses API** for a basic text-generation request. The Python SDK pattern looks like this:

```python
from openai import OpenAI

client = OpenAI()  # Reads OPENAI_API_KEY from the environment.

response = client.responses.create(
    model="gpt-6-astra",
    input="Explain what an API is in one sentence.",
)

print(response.output_text)
```

The ideas still transfer: select a model, provide input, optionally provide instructions or other supported settings, then inspect the response. The endpoint's request shape and output accessors differ. Use the documentation for the chosen endpoint and model rather than copying an example parameter blindly. Chat Completions remains useful for understanding this course and for projects that specifically use that endpoint; consult the migration guide when moving an existing integration to Responses.

## Key takeaways

- The API is a programmable request/response interface to models.
- Prompts should specify the task, context, constraints, and desired output shape.
- Read the structured response using the endpoint's documented fields.
- Token limits cap output; actual usage comes from response metadata.
- Examples and message roles can guide format and behavior, but outputs still need validation.
- Keep conversation state deliberately and protect secrets such as API keys.
- Learn the course using Chat Completions, then use current endpoint documentation when building new applications.

## Sources

### Course material

- [Chapter 1 PDF](../pdfs/chapter-01.pdf)
- [Chapter 2 PDF](../pdfs/chapter-02.pdf)
- [Chapter 3 PDF](../pdfs/chapter-03.pdf)

### Current OpenAI documentation

- [Developer quickstart](https://developers.openai.com/api/docs/quickstart)
- [Responses API guide](https://developers.openai.com/api/docs/guides/text)
- [Migrate to the Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses)
- [API pricing](https://openai.com/api/pricing/)
- [Chat Completions API reference](https://developers.openai.com/api/reference/resources/chat)
