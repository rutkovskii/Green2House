from multiprocessing import Manager, Process
from scripts.api import app as flask_app
from main_multiprocessing2 import main as main_func
from main_multiprocessing2 import waterSchedule


def create_app(latest_instructions):
    # Modify your Flask app to accept the shared dictionary as an argument
    # and use it instead of the global latest_instructions dictionary.
    app = flask_app(latest_instructions)
    return app


def create_main(latest_instructions):
    # Similarly, modify your main function to accept the shared dictionary as an argument
    # and use it instead of the global latest_instructions dictionary.
    main = main_func(latest_instructions)
    return main


if __name__ == "__main__":
    # Create a Manager
    manager = Manager()

    # Create a managed dictionary
    latest_instructions = manager.dict({
        "shutdown": False,
        "water": False,
        "mist": False,
        "lid": False,
        "fan": False,
        "heat": False,
        "min_temperature": None,
        "max_temperature": None,
        "min_humidity": None,
        "max_humidity": None,
        "watering_time": None,
        "watering_duration": None,
        "timestamp": None,
        "updated": False,
    })

    # Create your Flask app and the main function with the shared dictionary
    app = create_app(latest_instructions)
    main = create_main(latest_instructions)

    # Create the processes
    flask_process = Process(target=app.run, kwargs={"host": "0.0.0.0", "port": 5000, "debug": False})
    main_process = Process(target=main)
    schedule_process = Process(target=waterSchedule)

    # Start the processes
    flask_process.start()
    main_process.start()
    schedule_process.start()


    # Wait for the processes to finish
    flask_process.join()
    main_process.join()
    schedule_process.join()
