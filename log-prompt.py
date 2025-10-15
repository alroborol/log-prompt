import sqlite3
import json

def format_and_save_prompt(template, db_path='log-prompt.db', tag=None, **variables):
    """
    Formats the template with variables, saves template to 'prompts' table,
    and each variable as a row in 'prompt_variables' table linked by prompt_id.
    Only stores if the same template, variables, and tag do not already exist.
    Returns the rendered string.
    """
    rendered = template.format(**variables)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Create prompts table with tag (no rendered column)
    c.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY,
            template TEXT,
            tag TEXT
        )
    ''')
    # Create prompt_variables table
    c.execute('''
        CREATE TABLE IF NOT EXISTS prompt_variables (
            id INTEGER PRIMARY KEY,
            prompt_id INTEGER,
            var_name TEXT,
            var_value TEXT,
            FOREIGN KEY(prompt_id) REFERENCES prompts(id)
        )
    ''')
    # Check for existing prompt with same template and tag
    if tag is not None:
        c.execute('SELECT id FROM prompts WHERE template = ? AND tag = ?', (template, tag))
    else:
        c.execute('SELECT id FROM prompts WHERE template = ? AND tag IS NULL', (template,))
    prompt_ids = [row[0] for row in c.fetchall()]
    found = False
    for pid in prompt_ids:
        c.execute('SELECT var_name, var_value FROM prompt_variables WHERE prompt_id = ?', (pid,))
        db_vars = {row[0]: row[1] for row in c.fetchall()}
        # Compare variable keys and values (as JSON strings)
        if set(db_vars.keys()) == set(variables.keys()):
            match = True
            for k, v in variables.items():
                if db_vars[k] != json.dumps(v):
                    match = False
                    break
            if match:
                found = True
                break
    if not found:
        # Insert into prompts (no rendered)
        c.execute('INSERT INTO prompts (template, tag) VALUES (?, ?)', (template, tag))
        prompt_id = c.lastrowid
        # Insert each variable
        for k, v in variables.items():
            c.execute('INSERT INTO prompt_variables (prompt_id, var_name, var_value) VALUES (?, ?, ?)',
                      (prompt_id, k, json.dumps(v)))
        conn.commit()
    conn.close()
    return rendered
