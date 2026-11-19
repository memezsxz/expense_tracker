.PHONY: run check

run:
	uv run streamlit run app/streamlit_app.py

check:
	uv run --project . python -c "import sys; print(sys.executable)"