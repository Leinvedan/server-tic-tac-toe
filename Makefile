setup:
	pipenv install

run:
	pipenv run python -m server_tic_tac_toe.server.main

run_client:
	pipenv run python -m server_tic_tac_toe.client.main

lint:
	pipenv run python -m pylama