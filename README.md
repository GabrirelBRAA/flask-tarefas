# Sobre o projeto
Consegui fazer todo o backend com cache e hostear mas fiquei sem tempo. Faltou instalar o flake8 para seguir o PEP8 e também seria legal fazer ajustar o CORS junto com o front.

Falando em front, não o fiz pela falta de tempo.

Os endpoints hosteados estão abaixo. Como o certificado SSL é auto gerado, o browser vai reclamar, mas está tudo pegando.

# Build
- git clone
- docker-compose build
- docker-compose up
(pode ser que a sua maquina reclame por faltar algumas dependencias, o ec2 reclamou mas apontou para as que faltavam e foi só instalar usando yum.)

# Endpoints
https://ec2-3-145-148-0.us-east-2.compute.amazonaws.com
------
GET

Health check

https://ec2-3-145-148-0.us-east-2.compute.amazonaws.com/task/list
------
GET

resposta:

```
[
  {
    "description": "string",
    "id": number,
    "status": "pending | done"
  },
]
```
https://ec2-3-145-148-0.us-east-2.compute.amazonaws.com/user/create
------
POST

entrada:

```
{
  "name":"string",
  "password":"string"
}
```

resposta:

```
{
    "name": "string"
}
```
https://ec2-3-145-148-0.us-east-2.compute.amazonaws.com/user/login
------
POST

entrada:

```
{
  "name":"string",
  "password":"string"
}
```

resposta:

```
{
  "token": Token
}
```
https://ec2-3-145-148-0.us-east-2.compute.amazonaws.com/task/6/update
------
PATCH

headers:

    ```Authorization Bearer Token```

- entrada

```
{
  "status": "1 | 2" (1: pending, 2: done)
}
```

resposta:

```
{
  "description": "string",
  "id": number,
  "status": "pending | done"
}
```
https://ec2-3-145-148-0.us-east-2.compute.amazonaws.com/task/create
------
POST

headers:

    ```Authorization Bearer Token```

entrada:

```
{
  "description": "string"
}
```

resposta:

```
{
  "description": "string",
  "id": number,
  "status": "pending | done"
}
```

https://ec2-3-145-148-0.us-east-2.compute.amazonaws.com/task/1/delete
------
POST

headers:

    ```Authorization Bearer Token```


resposta:

`204 NO CONTENT`