FROM focker.ir/python:3.12-alpine
WORKDIR /app
COPY ./ /app/
RUN apk add --update --no-cache gcc musl-dev && pip install pipenv && pipenv install --system --ignore-pipfile
CMD ["sh"]
