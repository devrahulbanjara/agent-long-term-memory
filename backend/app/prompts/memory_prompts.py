MEMORY_EXTRACTION_PROMPT = """Extract ONE fact ABOUT THE USER worth remembering long-term.

SAVE if user states:
- "I like/love/prefer X" → save as "likes X"
- "I am allergic to X" → save as "allergic to X"
- "I live in X" → save as "lives in X"
- "My name is X" → save as "name is X"

DO NOT SAVE:
- Instructions given by assistant
- General knowledge discussed
- Temporary requests
- Avoid duplicates

User: {user_msg}
Assistant: {ai_msg}

Return ONE fact in the array, or empty array if nothing to remember."""