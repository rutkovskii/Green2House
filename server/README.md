Links:

1. https://stackoverflow.com/questions/14415500/common-folder-file-structure-in-flask-app

Feature Resources:

1. https://testdriven.io/blog/flask-async/

To-Do:

1. Serve Data functions from DataSamples
   1. Fix Serving of data
2. Create html for DataSamples
   1. Correct Headers
   2. Create links from / page
3. https://stackoverflow.com/questions/18807322/sqlalchemy-foreign-key-relationship-attributes

Folder Structure:

# server

- [app/](./server/app)
  - [admin/](./server/app/admin)
    - [**init**.py](./server/app/admin/__init__.py)
    - [config.py](./server/app/admin/config.py)
    - [decorators.py](./server/app/admin/decorators.py)
    - [views.py](./server/app/admin/views.py)
  - [auth/](./server/app/auth)
    - [auth.py](./server/app/auth/auth.py)
    - [forms.py](./server/app/auth/forms.py)
  - [database/](./server/app/database)
    - [database.py](./server/app/database/database.py)
    - [database_prefills.py](./server/app/database/database_prefills.py)
    - [models.py](./server/app/database/models.py)
  - [flask_content/](./server/app/flask_content)
    - [HTML/](./server/app/flask_content/HTML)
      - [admin_data_records_table.html](./server/app/flask_content/HTML/admin_data_records_table.html)
      - [admin_page_main.html](./server/app/flask_content/HTML/admin_page_main.html)
      - [admin_signedin_base.html](./server/app/flask_content/HTML/admin_signedin_base.html)
      - [admin_table_base.html](./server/app/flask_content/HTML/admin_table_base.html)
      - [admin_users_table.html](./server/app/flask_content/HTML/admin_users_table.html)
      - [index.html](./server/app/flask_content/HTML/index.html)
      - [signedout_base.html](./server/app/flask_content/HTML/signedout_base.html)
      - [signin.html](./server/app/flask_content/HTML/signin.html)
      - [signup.html](./server/app/flask_content/HTML/signup.html)
      - [user_current_env_data_page.html](./server/app/flask_content/HTML/user_current_env_data_page.html)
      - [user_data_records_table.html](./server/app/flask_content/HTML/user_data_records_table.html)
      - [user_env_page.html](./server/app/flask_content/HTML/user_env_page.html)
      - [user_home_page.html](./server/app/flask_content/HTML/user_home_page.html)
      - [user_signedin_base.html](./server/app/flask_content/HTML/user_signedin_base.html)
      - [user_table_base.html](./server/app/flask_content/HTML/user_table_base.html)
      - [water.html](./server/app/flask_content/HTML/water.html)
  - [user/](./server/app/user)
    - [**init**.py](./server/app/user/__init__.py)
    - [config.py](./server/app/user/config.py)
    - [current_env_data_page.py](./server/app/user/current_env_data_page.py)
    - [datasample_page.py](./server/app/user/datasample_page.py)
    - [env_page.py](./server/app/user/env_page.py)
    - [get_data.py](./server/app/user/get_data.py)
    - [home_page.py](./server/app/user/home_page.py)
    - [vegetables.py](./server/app/user/vegetables.py)
  - [**init**.py](./server/app/__init__.py)
  - [create_flask_app.py](./server/app/create_flask_app.py)
  - [index.py](./server/app/index.py)
  - [utils.py](./server/app/utils.py)
- [configs/](./server/configs)
  - [env.txt](./server/configs/env.txt)
- [docker/](./server/docker)
- [.env](./server/.env)
- [README.md](./server/README.md)
- [**init**.py](./server/__init__.py)
- [config.py](./server/config.py)
- [requirements_server.txt](./server/requirements_server.txt)
- [run.py](./server/run.py)

server/
│ .env
│ README.md
│ **init**.py
│ config.py
│ requirements_server.txt
│ run.py
│
├───app/
│ │ **init**.py
│ │ create_flask_app.py
│ │ index.py
│ │ utils.py
│ │
│ ├───admin/
│ │ │ **init**.py
│ │ │ config.py
│ │ │ decorators.py
│ │ │ views.py
│ │
│ ├───auth/
│ │ │ auth.py
│ │ │ forms.py
│ │
│ ├───database/
│ │ │ database.py
│ │ │ database_prefills.py
│ │ │ models.py
│ │
│ ├───flask_content/
│ │ └───HTML/
│ │ │ admin_data_records_table.html
│ │ │ admin_page_main.html
│ │ │ admin_signedin_base.html
│ │ │ admin_table_base.html
│ │ │ admin_users_table.html
│ │ │ index.html
│ │ │ signedout_base.html
│ │ │ signin.html
│ │ │ signup.html
│ │ │ user_current_env_data_page.html
│ │ │ user_data_records_table.html
│ │ │ user_env_page.html
│ │ │ user_home_page.html
│ │ │ user_signedin_base.html
│ │ │ user_table_base.html
│ │ │ water.html
│ │
│ └───user/
│ │ **init**.py
│ │ config.py
│ │ current_env_data_page.py
│ │ datasample_page.py
│ │ env_page.py
│ │ get_data.py
│ │ home_page.py
│ │ vegetables.py
│
├───configs/
│ env.txt
│
└───docker/
