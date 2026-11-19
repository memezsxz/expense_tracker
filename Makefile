.PHONY: run check

run:
	uv run python -m streamlit run app/streamlit_app.py

check:
	uv run --project . python -c "import sys; print(sys.executable)"