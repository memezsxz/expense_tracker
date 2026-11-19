.PHONY: run init check

init:
	#uv init
	uv add streamlit
	uv add pandas
	uv add plotly
	uv add watchdog
	uv run streamlit skills

run:
	uv run streamlit run app/streamlit_app.py

check:
	uv run --project . python -c "import sys; print(sys.executable)"