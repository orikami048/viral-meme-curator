# 🚀 Viral Meme Curator Skill (for Antigravity AI Agent)

> An AGY (Antigravity) Skill that automatically curates trending content from **Reddit** and **Chinese X/Twitter**, translates and adapts it into authentic **American Gen-Z slang & U.S. viral meme templates**, and automatically publishes it to social platforms.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Skill](https://img.shields.io/badge/Antigravity-Skill-green.svg)

---

## 🌟 Features

* 🤖 **Cross-Platform Scraping**: Automatically fetches top viral memes from Reddit (`r/memes`, `r/dankmemes`, `r/wallstreetbets`, `r/AskReddit`) and Chinese Twitter/X hot topics.
* 🇺🇸 **U.S. Cultural Localization**: Transforms raw posts into native American Gen-Z/Zoomer internet humor (`no cap`, `let him cook`, `crash out`, `glaze`, `fr fr`, `main character energy`, `brainrot`, `skibidi`).
* 📝 **Viral Formatting**: Formats content into battle-tested viral X/Twitter structures (`POV:`, `Bro really thought...`, `Nobody:`, `My honest reaction: 🗿`).
* ⚡ **Dry-Run & Auto-Publishing**: Supports dry-run inspection before posting to Twitter/X or Reddit.

---

## 📁 Repository Structure

```text
viral-meme-curator/
├── SKILL.md                          # Main Skill specification for Antigravity Agent
├── README.md                         # Documentation
├── LICENSE                           # MIT License
├── requirements.txt                  # Python dependencies
├── config.example.json               # Config & API key template
├── scripts/
│   ├── fetch_reddit_trending.py      # Reddit scraper
│   ├── fetch_chinese_x_trending.py   # Chinese X scraper
│   ├── meme_rewriter.py              # U.S. slang & meme rewriter
│   └── auto_publisher.py             # Multi-platform auto-publisher
└── references/
    ├── us_slang_dictionary.md        # American Gen-Z slang & meme dictionary
    └── viral_tweet_templates.md     # Viral tweet formatting patterns
```

---

## 🛠️ Installation & Setup

### 1. Install as an Antigravity Workspace Skill

Copy this repository folder into your workspace `.agents/skills/` or global skills folder:

```bash
mkdir -p ~/.gemini/config/skills/
cp -r viral-meme-curator ~/.gemini/config/skills/
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Credentials

Copy `config.example.json` to `config.json` and fill in your keys:

```json
{
  "openai_api_key": "YOUR_OPENAI_KEY",
  "twitter_api_key": "YOUR_TWITTER_API_KEY",
  "twitter_api_secret": "YOUR_TWITTER_API_SECRET",
  "twitter_access_token": "YOUR_TWITTER_ACCESS_TOKEN",
  "twitter_access_token_secret": "YOUR_TWITTER_ACCESS_TOKEN_SECRET"
}
```

---

## 🚀 Quickstart Usage

### Run full pipeline via Antigravity Agent:

Simply prompt your Antigravity agent:
> *"Use the `viral-meme-curator` skill to fetch 5 hot memes from Reddit r/dankmemes, rewrite them into U.S. Zoomer slang, and preview the tweets."*

### Run manually via CLI:

```bash
# 1. Fetch Reddit Memes
python scripts/fetch_reddit_trending.py --subreddit memes --limit 5

# 2. Rewrite into American Gen-Z humor
python scripts/meme_rewriter.py --input-file temp/reddit_trending.json

# 3. Dry-run preview
python scripts/auto_publisher.py --dry-run
```

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
