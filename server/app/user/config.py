import os
from dotenv import load_dotenv

load_dotenv()

class UserConfig:
    # Routes
    MY_DATA_SAMPLES_ROUTE = "/my-data-records"
    SERVE_DATA_SAMPLES_ROUTE = "/api/serve-data-records"
    SERVE_GRAPH_DATA_ROUTE = "/api/serve-graph-data-records"
    ENV_ROUTE = "/environment"
    CURRENT_ENV_DATA_ROUTE = "/current-environment"
    BUTTONS_ROUTE = "/controls"
    CHARTS_ROUTE = "/charts"

    # URL for the BBB
    # IP = os.getenv("BBB_IP")
    # BBB_URL = f"http://{IP}:5000"
    IP = os.getenv("DOMAIN")
    BBB_URL = f"https://{IP}"

    INSTRUCTIONS_URL = f"{BBB_URL}/instructions"
    BUTTONS_URL = f"{BBB_URL}/buttons"
    SHUTDOWN_URL = f"{BBB_URL}/shutdown"
