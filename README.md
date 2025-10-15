# log-prompt

A simple Python utility to format prompt templates with variables and store them in a SQLite database from your AI apps. Useful for logging prompt and user input for reproducibility or analysis.

Use https://github.com/alroborol/tune-prompt to tune the saved prompts with the recorded input.

## Features
- Format a template string with variables.
- Store prompt templates and their variables in a SQLite database.
- Avoid duplicate storage by checking for existing templates, variables, and tags.
- Optional tagging of prompts for organization.

## Usage
Replace the LLM prompt with the following function to log.

### Function

```python
format_and_save_prompt(template, db_path='log-prompt.db', tag=None, **variables)
```

- `template`: The prompt template string, using Python's `.format()` syntax.
- `db_path`: Path to the SQLite database file (default: `log-prompt.db`).
- `tag`: Optional string tag to categorize or identify the prompt.
- `**variables`: Keyword arguments for variables to fill into the template.

### Example

```python
from log-prompt import format_and_save_prompt

rendered = format_and_save_prompt(
    "Hello, {name}! Your score is {score}.",
    db_path="my_prompts.db",
    tag="greeting",
    name="Alice",
    score=95
)
print(rendered)  # Output: Hello, Alice! Your score is 95.
```

## Database Schema
- `prompts` table: Stores the template and tag.
- `prompt_variables` table: Stores variable names and values linked to a prompt.

## Requirements
- Python 3.x
- Standard library only (uses `sqlite3` and `json`)
