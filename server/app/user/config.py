class UserConfig:
    # Routes
    MY_DATA_SAMPLES_ROUTE = "/my-data-records"
    SERVE_DATA_SAMPLES_ROUTE = "/api/serve-data-records"
    ENV_ROUTE = "/environment"
    CURRENT_ENV_DATA_ROUTE = "/current-environment"
    BUTTONS_ROUTE = "/buttons"

    # URL for the BBB
    BBB_URL = "http://10.0.0.111:5000"

    INSTRUCTIONS_URL = f"{BBB_URL}/instructions"
    WATER_URL = f"{BBB_URL}/water-plant"
