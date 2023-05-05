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
    BBB_URL = "http://107.115.17.17:5000"

    INSTRUCTIONS_URL = f"{BBB_URL}/instructions"
    WATER_URL = f"{BBB_URL}/water-plant"
