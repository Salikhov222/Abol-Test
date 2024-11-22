.DEFAULT_GOAL := help

HOST ?= 0.0.0.0
PORT ?= 8000

run:	# Run the application using uvicorn with provided arguments or defaults
	uvicorn main:app --host  $(HOST) --port $(PORT) --reload --env-file .env

install: 	# Install library
	pip3 install --proxy http://akhmed@gu-ito-ws05:S@likh0v@proxy.giop.local:3128 $(LIBRARY)

migrate-create:		# Create a new revision migration
	alembic revision --autogenerate -m "$(MIGRATE)"

migrate-apply:		# Run migration
	alembic upgrade head

help:	# Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?# .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?# "}; {printf "  %-20s %s\n", $$1, $$2}'