name: Publish to Telegram Channel

on:
  schedule:
    # Публикация с 02:00 до 15:00 по UTC (с 09:00 до 22:00 по Новосибирску, UTC+7)
    - cron: '0 2-15 * * *'
  workflow_dispatch:

concurrency:
  group: telegram-publisher
  cancel-in-progress: false

permissions:
  contents: write

jobs:
  send-post:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install requests

      - name: Publish post to Telegram
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_TO: "@master_3d_workshop"
        run: python publish.py

      - name: Commit updated state
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add state.json
          git diff --staged --quiet || git commit -m "chore: rotate post index"
          git push
