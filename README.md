# Expense Tracker

Expense Tracker is an open-source expense tracking and visualization program developed using [Streamlit](https://streamlit.io/). The data is supplied by a user specified Google Sheet. Visualizations generated in this app are created using [Plotly](https://plotly.com/python/).

## Usage

A sample Google Sheet compatible with this application can be found here:
[Test Expense Tracker](https://docs.google.com/spreadsheets/d/1QGq30uszyxQzAoARVy4pZE0LElwIuXXMbFc5g4ftjVk)

The connection to Google Sheets is powered by [gsheets-connection](https://github.com/streamlit/gsheets-connection). Follow instructions in the repo to connect the desired Google Sheet.

This application supports tracking for expense trackers that involve multiple individuals. Transaction owners can be specified as shown in the example file: [.streamlit/expense_tracker_config.toml](.streamlit/expense_tracker_config.toml).

### Running locally

Dependencies can be installed using the following command:

```shell
$ pip install -r requirements.txt
```

Run the following command to start a local instance of this using the Streamlit engine:
```shell
$ streamlit run app.py
```

### Deployment

Follow the official [Streamlit deployment guide](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app) to host this on the Streamlit Community Cloud.

A Docker image can also be built and deployed for users who prefer alternate hosting solutions. The official Docker installation guide can be found [here](https://docs.docker.com/installation/). Run the following commands to build and run the Docker image.

```shell
$ docker build -t expense-tracker .
$ docker run -p 8501:8501 expense-tracker
```
