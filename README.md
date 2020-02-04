# GroupCeleryFLask

- run `docker run -d -p 1234:6379 redis` to redis container

- run `celery -A flask_celery.celery worker --loglevel=info` to start celery

- run `python flask_celery` to run python server at 127.0.0.1:5000

- visit `127.0.0.1:5000/group` to create group (`returns group_id`)

- visit `127.0.0.1:9090/get_childs_group/<group_id>` to get all childs in `group_id`

