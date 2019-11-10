setup:
	pipenv install

run:
	pipenv run python -m server_tic_tac_toe.server.server

run_client:
	pipenv run python -m server_tic_tac_toe.client.client