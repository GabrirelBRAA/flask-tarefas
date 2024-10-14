# Endpoints
https://ec2-3-145-148-0.us-east-2.compute.amazonaws.com
------
Health check

https://ec2-3-145-148-0.us-east-2.compute.amazonaws.com/task/list
------

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
headers:

    ```Authorization Bearer Token```


resposta:

`204 NO CONTENT`