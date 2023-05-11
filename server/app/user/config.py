class UserConfig:
    # Routes
    MY_DATA_SAMPLES_ROUTE = "/my-data-records"
    SERVE_DATA_SAMPLES_ROUTE = "/api/serve-data-records"
    SERVE_GRAPH_DATA_ROUTE = "/api/serve-graph-data-records"
    ENV_ROUTE = "/environment"
    CURRENT_ENV_DATA_ROUTE = "/current-environment"
    BUTTONS_ROUTE = "/buttons"
    CHARTS_ROUTE = "/charts"

    # URL for the BBB
    IP = "172.20.10.5"
    BBB_URL = f"http://{IP}:5000"

    INSTRUCTIONS_URL = f"{BBB_URL}/instructions"
    BUTTONS_URL = f"{BBB_URL}/buttons"
    SHUTDOWN_URL = f"{BBB_URL}/shutdown"
