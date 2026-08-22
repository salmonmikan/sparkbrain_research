.PHONY: install lint test demo benchmark validate all clean-artifacts

install:
	python -m pip install -e ".[dev]"

lint:
	python -m ruff check .

test:
	python -m pytest -q

demo:
	python scripts/run_demo.py

benchmark:
	python scripts/run_benchmark.py --episodes 40 --steps 30

validate:
	python scripts/validate_bundle.py

all: lint test demo benchmark validate

clean-artifacts:
	rm -rf artifacts/demo artifacts/benchmarks
