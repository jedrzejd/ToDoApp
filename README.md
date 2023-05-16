# Django TODOAPP

This is a TODO app built with Django. It allows users to create, update, and delete tasks in a user-friendly interface.

## Features

- User registration and authentication: Users can create an account and log in to manage their tasks.
- Task management: Users can create, view, update, and delete tasks.
- Task status tracking: Users can mark tasks as completed.
- Task list creation: Users can create lists to organize their tasks and add tasks to specific lists.


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/jedrzejd/ToDoApp.git

2. Navigate to the project directory:
   ```bash
   cd ToDoApp

3. Create a virtual environment:
   - On macOS and Linux: 
     ```bash
     python -m venv venv
   - On Windows:
     ```bash
     py -m venv venv

4. Activate the virtual environment:
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
   - On Windows:
    ```bash
    venv\Scripts\activate

5. Install the dependencies:
    ```bash
    pip install -r requirements.txt

6. Perform database migrations:
    ```bash
    python manage.py migrate

7. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser

8. Run the development server:
    ```bash
   python manage.py runserver

9. Open your browser and navigate to http://localhost:8000 to access the application.

## Configuration

The project uses the default Django settings. However, if you need to modify the configuration, you can update the settings.py file in the todoapp directory.

## Contributing

Contributions are welcome! If you find any issues or want to enhance the application, feel free to open a pull request.

## License

The project is licensed under the MIT License. You can find the license details in the LICENSE file.

## Acknowledgements

This project was inspired by the need for a simple and efficient TODO app.
Thanks to the Django community for their excellent documentation and resources.

## Contact

If you have any questions or suggestions, feel free to contact me at jedrzej012@gmail.com.

Happy task management with Django TODOAPP!
