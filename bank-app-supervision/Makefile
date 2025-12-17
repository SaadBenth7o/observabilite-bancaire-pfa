SHELL := /bin/bash
.RECIPEPREFIX = >

up:
> docker compose up -d

down:
> docker compose down

logs:
> docker compose logs -f --tail=200

ps:
> docker compose ps

seed:
> docker compose exec -T flask_app python -m app.seeds

test:
> docker compose exec -T flask_app pytest -q

clean:
> docker compose down -v || true
> rm -rf volumes/esdata volumes/grafana volumes/postgres logs/app/*.log || true
