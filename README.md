
# Epicbase

A Discord integrated app designed to manage consumer reviews of Epic Games support employees, providing valuable insights to aid in social engineering attempts.
## Installation

Clone the repository
```bash
  git clone https://github.com/nitl0l/epicbase.git
  cd epicbase
```

Setup your virtual environment
```bash
  python3 -m venv .venv
  source .venv/bin/activate    
```

Install requirements
```bash
  pip install -r requirements.txt
```

Create .env file
```bash
  touch .env
  nano .env
```

Your .env file should follow this format
```env
  DISCORD_TOKEN = YOUR_DISCORD_BOT_TOKEN # https://discord.com/developers
```

Deploy the bot
```bash
  python3 src/epicbase.py
```
## Authors

- [@nitl0l](https://www.github.com/nitl0l)

