.PHONY: install test notebook clean

install:
	pip install -e ../routes-pricing-shared
	pip install -e ".[dev]"

test:
	pytest -q

notebook:
	jupytext --to ipynb notebooks/01_street_routing.py
	jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=uber-venv --ExecutePreprocessor.timeout=900 notebooks/01_street_routing.ipynb

clean:
	rm -rf .pytest_cache notebooks/.ipynb_checkpoints
