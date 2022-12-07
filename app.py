import os
from textwrap import dedent

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from PIL import Image
import openai


def Header(name, app):
    title = html.H1(name, style={"margin-top": 5})
    logo = html.Img(
        src=app.get_asset_url("logo.png"), style={"float": "right", "height": 60}
    )
    return dbc.Row([dbc.Col(title, md=8), dbc.Col(logo, md=4)])


def textbox(text, box="AI", name="Katonic"):
    text = text.replace(f"{name}:", "").replace("You:", "")
    style = {
        "max-width": "60%",
        "width": "max-content",
        "padding": "5px 10px",
        "border-radius": 25,
        "margin-bottom": 20,
    }

    if box == "user":
        style["margin-left"] = "auto"
        style["margin-right"] = 0

        return dbc.Card(text, style=style, body=True, color="primary", inverse=True)

    elif box == "AI":
        style["margin-left"] = 0
        style["margin-right"] = "auto"

        thumbnail = html.Img(
            src=app.get_asset_url("favicon.ico"),
            style={
                "border-radius": 50,
                "height": 36,
                "margin-right": 5,
                "float": "left",
            },
        )
        textbox = dbc.Card(text, style=style, body=True, color="light", inverse=False)

        return html.Div([thumbnail, textbox])

    else:
        raise ValueError("Incorrect option for `box`.")


# Authentication
openai.api_key = os.getenv("OPENAI_KEY")

# Define app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], url_base_pathname=os.getenv("ROUTE") or "/")
server = app.server
app.title = "GPT-3 Chatbot"

# Load images
IMAGES = {"Katonic": app.get_asset_url("favicon.ico")}


# Define Layout
conversation = html.Div(
    html.Div(id="display-conversation"),
    style={
        "overflow-y": "auto",
        "display": "flex",
        "height": "calc(90vh - 132px)",
        "flex-direction": "column-reverse",
    },
)

controls = dbc.InputGroup(
    children=[
        dbc.Input(id="user-input", placeholder="Write to the chatbot...", type="text",
                    style={'font-size': '15px', 
                            'width': '140px', 
                            'display': 'inline-block', 
                            'margin-bottom': '100px',
                            'margin-right': '50px', 
                            'height':'37px', 
                            'verticalAlign': 'top'}),
        dbc.Button("Submit", id="submit",
                    style={'font-size': '15px', 
                            'width': '140px', 
                            'display': 'inline-block', 
                            'margin-bottom': '100px',
                            'margin-right': '50px', 
                            'height':'37px', 
                            'verticalAlign': 'top'}
                       )
                    
    ])

app.layout = dbc.Container(
    fluid=False,
    children=[
        Header("GPT-3 Chatbot", app),
        html.Hr(),
        dcc.Store(id="store-conversation", data=""),
        conversation,
        controls,
        dbc.Spinner(html.Div(id="loading-component")),
    ],
)


@app.callback(
    Output("display-conversation", "children"), [Input("store-conversation", "data")]
)
def update_display(chat_history):
    return [
        textbox(x, box="user") if i % 2 == 0 else textbox(x, box="AI")
        for i, x in enumerate(chat_history.split("<split>")[:-1])
    ]


@app.callback(
    Output("user-input", "value"),
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
)
def clear_input(n_clicks, n_submit):
    return ""


@app.callback(
    [Output("store-conversation", "data"), Output("loading-component", "children")],
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
    [State("user-input", "value"), State("store-conversation", "data")],
)
def run_chatbot(n_clicks, n_submit, user_input, chat_history):
    if n_clicks == 0 and n_submit is None:
        return "", None

    if user_input is None or user_input == "":
        return chat_history, None

    name = "Katonic"

    prompt = dedent(
        f"""

    You: Hello {name}!
    {name}: Hello! Glad to be talking to you today.
    """
    )

    # First add the user input to the chat history
    chat_history += f"You: {user_input}<split>{name}:"

    model_input = prompt + chat_history.replace("<split>", "\n")

    response = openai.Completion.create(
        engine="davinci",
        prompt=model_input,
        max_tokens=250,
        stop=["You:"],
        temperature=0.9,
    )
    model_output = response.choices[0].text.strip()

    chat_history += f"{model_output}<split>"

    return chat_history, None


if __name__ == "__main__":
    app.run_server(debug=False,port=8050,host='0.0.0.0')
