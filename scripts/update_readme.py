"""Rebuilds the project table in README.md from your live GitHub repos."""
import json, os, re, urllib.request

USER = "assassin-cloud"
README = "README.md"

# Curated descriptions (used first). New repos fall back to their GitHub
# description, then to a placeholder. Add a line here to customise any repo.
DESCRIPTIONS = {
    "c-calculator": "A simple calculator built with C++",
    "Bulk-calculator": "Lets you calculate in bulk",
    "Love-calculator": "A just-for-fun compatibility meter that turns two names into a love %",
    "Temperature-converter": "Convert between temperature units",
    "basic-number-statistic": "A simple number analyzer for basic stats on your inputs",
    "Array-creator": "Pick a size, enter the values, get your array back (dynamic memory)",
    "shape-generator": "Generates shapes in the console",
    "MyContacts": "A console contact manager",
    "TODO": "Command-line task manager: add, view, complete/undo and delete tasks",
    "TIC-TAC-TOE": "Two-player game with win/draw detection, custom names and a scoreboard",
    "ATM_SIMULATOR": "Multi-account ATM: PIN login, deposits, withdrawals and transfers",
    "atm-machine": "The first, PIN-protected ATM: balance, withdraw and deposit",
}

ICONS = [
    ("calc", "🧮"), ("love", "💘"), ("temp", "🌡️"), ("stat", "📊"), ("array", "🧱"),
    ("shape", "🔷"), ("contact", "📇"), ("todo", "✅"), ("tic", "❌⭕"),
    ("atm", "🏧"), ("game", "🎮"), ("bank", "🏦"),
]


def icon(name):
    n = name.lower()
    return next((i for k, i in ICONS if k in n), "📁")


def fetch_repos():
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "readme-updater"}
    if os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    url = f"https://api.github.com/users/{USER}/repos?per_page=100&sort=updated"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def build_table(repos):
    rows = ["| | Project | What it does | Lang | ⭐ |", "|:-:|:--|:--|:-:|:-:|"]
    for r in repos:
        if r["name"].lower() == USER.lower() or r["fork"] or r["archived"]:
            continue
        desc = DESCRIPTIONS.get(r["name"]) or r["description"] or "Coming soon"
        rows.append(
            f"| {icon(r['name'])} | [**{r['name']}**]({r['html_url']}) | {desc} "
            f"| {r['language'] or '-'} | {r['stargazers_count']} |"
        )
    return "\n".join(rows)


def main():
    table = build_table(fetch_repos())
    text = open(README, encoding="utf-8").read()
    pattern = re.compile(r"(<!--PROJECTS:START-->).*?(<!--PROJECTS:END-->)", re.S)
    new = pattern.sub(lambda m: f"{m.group(1)}\n{table}\n{m.group(2)}", text)
    if new != text:
        open(README, "w", encoding="utf-8").write(new)
        print("README updated")
    else:
        print("No changes")


if __name__ == "__main__":
    main()
    
