FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Copy application code
COPY . .

# Install Python dependencies
RUN uv sync --frozen

# Run the bot
CMD ["uv", "run", "meme-bot"] 