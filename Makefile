setup:
	pipenv install

run:
	pipenv run python -m server_tic_tac_toe.core.server

run_client:
	pipenv run python -m server_tic_tac_toe.core.client