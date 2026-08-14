FROM python:3.13

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv

RUN uv sync --no-dev

COPY . .

EXPOSE 8501

CMD sh -c "uv run python main.py && uv run streamlit run dashboard/app.py --server.address=0.0.0.0 --server.port=8501"