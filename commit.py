import os
from InquirerPy import prompt


COMMIT_TYPES = [
    {
        "name": "✨ feat",
        "value": "✨ feat"
    },
    {
        "name": "🐛 fix",
        "value": "🐛 fix"
    },
    {
        "name": "♻ refac",
        "value": "♻ refac"
    },
    {
        "name": "📄 docs",
        "value": "📄 docs"
    },
    {
        "name": "🧪 test",
        "value": "🧪 test"
    }
]

CONFIRM = [
    {
        "name": "Sim",
        "value": True
    },
    {
        "name": "Não",
        "value": False
    }
]

PROMPTS = [
    {
        "type": "list",
        "name": "commit_type",
        "message": "Escolha o tipo de commit:",
        "choices": COMMIT_TYPES
    },
    {
        "type": "input",
        "name": "commit_message",
        "message": "Digite a mensagem do commit:"
    },
    {
        "type": "list",
        "name": "can_commit",
        "message": "Deseja commitar a mensagem?",
        "choices": CONFIRM
    },
]

try:
    while True:
        OPTIONS = prompt(PROMPTS)

        if not OPTIONS['commit_message']:
            print("\nA mensagem do commit não pode estar vazia, tente novamente!\n")
            continue
        
        commit = f"{OPTIONS['commit_type']}: {OPTIONS['commit_message']}"
        print(f"\n\n{commit}\n\n")

        if OPTIONS['can_commit']:
            print("Commitando")
            os.system(f'git commit -m "{commit}"')

        break

except KeyboardInterrupt:
    print("\nFinalizando processo...")
