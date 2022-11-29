# инструкция по работе с файлом "Makefile" – https://bytes.usc.edu/cs104/wiki/makefile/

# обновление сборки Docker-контейнера
build:
	docker compose build

# запуск форматирования кода
format:
	docker compose run --workdir / app /bin/bash -c "black src; isort --profile black src"

# запуск статического анализа кода (выявление ошибок типов и форматирования кода)
lint:
	docker compose run --workdir / app /bin/bash -c "pylint src; flake8 src; mypy src; black --check src"

# запуск всех функций поддержки качества кода
all: format lint
