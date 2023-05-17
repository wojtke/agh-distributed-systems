## REST API

---

### Lab - Polls REST API

A simple interface for creating and voting on polls - completed during the lab.

### Project - Cooking Assistant

#### Setup

REST API for cooking recipes (Spooncular API) and some AI help (OpenAI API) in case you get stuck. Fun project, not quite finished. No frontend. No guarantee that it works.

```bash
pip install -r requirements.txt
```

You need .env file with the following api keys:

```
OPENAI_API_KEY=...
SPOONACULAR_API_KEY=...
```

#### Run

```bash
python main.py
```

There is basic authentication implemented with the following credentials:
    
```
username: johndoe
password: secret
```

#### Walkthrough of the API

1. Authentication - **GET** `/auth/login`
2. Add some ingredients - **POST** `/ingredients`
3. Get recipes - **GET** `/recipes`
4. Start cooking - **POST** `/cookings`
5. Move to step - **POST** `/cookings/step/{stepNumber}`
6. Ask AI for help - **POST** `/cookings/issues`

Refer to [`http://localhost:8989/docs`](http://localhost:8989/docs) for more details.




