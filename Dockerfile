FROM ghcr.io/astral-sh/uv:python3.10-alpine

WORKDIR /app

# Copy application code
COPY . .

# Install Python dependencies
RUN uv sync --frozen

# Run the bot
CMD ["uv", "run", "bot.py"] 