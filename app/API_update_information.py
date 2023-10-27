import numpy as np
import os
import pandas as pd
import cv2
import plotly.express as px
import dash
import plotly.graph_objects as go # or plotly.express as px
from plotly.subplots import make_subplots
from dash import Dash, html, dcc, callback, Input, Output, State, callback, ctx
from IPython.display import display,HTML
import dash_auth
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload
import io



def load_imgs(p1):

    IMG1 = cv2.imread(p1)
    
    IMG1 = cv2.resize(IMG1, (1074, 612),interpolation=cv2.INTER_CUBIC)  # set to 256x256
    return IMG1

INVTYPE = ["yes", "no", "not sure"]
SHAPE = ["ill_defined",  "well_defined", "spiculated", "other", "indiscriminable"]
SYMMETRY = ["yes", "no", "not sure"]
Mass = ["yes", "no", "not sure"]




SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "/app/gdrive_key.json"

VALID_USERNAME_PASSWORD_PAIRS = {
    "cory": "zZ27^j8)[}YXC3q6Cf;rNQ",
    "reyer": "W8ah72F`k&`m43!,,gu<Y",
    "erika": "tAQ201)5+=0esiJ>9#k9~"
}

EXCEL_PATH = "/app/Optimum_Malignant_cases_with_prescreen.xlsx"


data = pd.read_excel(EXCEL_PATH)
app = dash.Dash(__name__)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)



app.layout = html.Div([
    html.H1('Update Lesion Information Dashboard', style={'text-align':'center'}),
    html.Button('Save', id='btn-nclicks-3', n_clicks=0, style={'font-size': '16px', 'width': '240px', 'display': 'inline-block', 'margin-bottom': '10px', 'margin-right': '5px', 'height':'50px'}),
    html.Button('', id='btn-nclicks-4', n_clicks=0, style={'font-size': '16px', 'width': '240px', 'display': 'inline-block', 'margin-bottom': '10px', 'margin-right': '5px', 'height':'50px'}),
    html.Button('Previous', id='btn-nclicks-1', n_clicks=0, style={'font-size': '16px', 'width': '240px', 'display': 'inline-block', 'margin-bottom': '10px', 'margin-right': '5px', 'height':'50px'}),
    html.Button('Next', id='btn-nclicks-2', n_clicks=0, style={'font-size': '16px', 'width': '240px', 'display': 'inline-block', 'margin-bottom': '10px', 'margin-right': '5px', 'height':'50px'}),
    
    html.Div(children = [html.Div(id='container-button-timestamp'),html.Div(id='save_stamp')]),
    html.Div(dcc.Graph(id='EXAMPLE', style={'display': 'inline-block', 'height':'100%', 'width':'100%'})),
    html.Div(children = ["Are there Calcifications?",dcc.Dropdown(id='Invisive_dropdown', options = [{"label": i, "value": i} for i in INVTYPE], value = [], clearable=True), html.Div(id='INVTYPE_UPDATE')]),
    html.Div(children = ["Lesion shape",dcc.Dropdown(id='Shape_dropdown', options = [{"label": i, "value": i} for i in SHAPE], value = [], clearable=True), html.Div(id='SHAPE_UPDATE')]),
    html.Div(children = ["Is there a Symmetry?",dcc.Dropdown(id='Symmetry_dropdown', options = [{"label": i, "value": i} for i in SYMMETRY], value = [], clearable=True), html.Div(id='SYMMETRY_UPDATE')]),
    html.Div(children = ["Is there a Mass",dcc.Dropdown(id='Mass_dropdown', options = [{"label": i, "value": i} for i in Mass], value = [], clearable=True), html.Div(id='MASS_UPDATE')]),
    ])


@app.callback(Output('EXAMPLE','figure'),
    Output('container-button-timestamp', 'children'),#
    Output('Invisive_dropdown', 'value'),
    Output('Shape_dropdown', 'value'),
    Output('Symmetry_dropdown', 'value'),
    Output('Mass_dropdown', 'value'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),)


def update_example(btn1, btn2):
    bt = btn2 - btn1
    if bt < 0 or bt > data.shape[0]:
        msg = "Image index {}".format(0)
        IMG_NAME1 = data["CaseID"].iloc[0]
        P1 = os.path.join("/app/Segs", "{}.png".format(IMG_NAME1))
        
        IMG = load_imgs(P1)
        DISPLAY = px.imshow(IMG)
        
        DISPLAY.update_layout(coloraxis_showscale=False)
        DISPLAY.update_xaxes(showticklabels=False)
        DISPLAY.update_yaxes(showticklabels=False)
        
        return DISPLAY, html.Div(msg, style={'font-size': '20px'}), data["Calcifications"].iloc[0], data["MassClassification"].iloc[0], data["ArchitecturalDistortion"].iloc[0], data["Mass"].iloc[0]
       
    else:
        msg = "Image index {}".format(bt)
        IMG_NAME1 = data["CaseID"].iloc[bt]
        P1 = os.path.join("/app/Segs", "{}.png".format(IMG_NAME1))
        
        IMG = load_imgs(P1)
        DISPLAY = px.imshow(IMG)
        
        DISPLAY.update_layout(coloraxis_showscale=False)
        DISPLAY.update_xaxes(showticklabels=False)
        DISPLAY.update_yaxes(showticklabels=False)
        
        return DISPLAY, html.Div(msg, style={'font-size': '20px'}), data["Calcifications"].iloc[bt], data["MassClassification"].iloc[bt], data["ArchitecturalDistortion"].iloc[bt], data["Mass"].iloc[bt]

@app.callback(Output('INVTYPE_UPDATE', 'children'),
    Output('SHAPE_UPDATE', 'children'),
    Output('SYMMETRY_UPDATE', 'children'),
    Output('MASS_UPDATE', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('Invisive_dropdown', 'value'),
    Input('Shape_dropdown', 'value'),
    Input('Symmetry_dropdown', 'value'),
    Input('Mass_dropdown', 'value'),
    )
    
def update_frame(btn1, btn2, vIn, vSh, vSy, vMa):
    bt = btn2 - btn1
    if bt >= 0:
        bIN = data["Calcifications"].iloc[bt]
        bSH = data["MassClassification"].iloc[bt]
        bSY = data["ArchitecturalDistortion"].iloc[bt]
        bMA = data["Mass"].iloc[bt]
        if bIN != vIn or bSH != vSh or bSY != vSy or bMA != vMa:
            msg = "Updated"
            msg2 = "No_Update"
            if bIN != vIn:
                data["Calcifications"].iloc[bt] = vIn
 
                return html.Div(msg, style={'font-size': '10px'}), html.Div(msg2, style={'font-size': '10px'}),html.Div(msg2, style={'font-size': '10px'}),html.Div(msg2, style={'font-size': '10px'})
            elif bSH != vSh:
                data["MassClassification"].iloc[bt] = vSh

                return html.Div(msg2, style={'font-size': '10px'}), html.Div(msg, style={'font-size': '10px'}),html.Div(msg2, style={'font-size': '10px'}),html.Div(msg2, style={'font-size': '10px'})
            elif bSY != vSy:
                data["ArchitecturalDistortion"].iloc[bt] = vSy

                return html.Div(msg2, style={'font-size': '10px'}), html.Div(msg2, style={'font-size': '10px'}),html.Div(msg, style={'font-size': '10px'}),html.Div(msg2, style={'font-size': '10px'})
            elif bMA != vMa:
                data["Mass"].iloc[bt] = vMa

                return html.Div(msg2, style={'font-size': '10px'}), html.Div(msg2, style={'font-size': '10px'}),html.Div(msg2, style={'font-size': '10px'}),html.Div(msg, style={'font-size': '10px'})
            
    msg = "No-Updated"
    return html.Div(msg, style={'font-size': '10px'}),html.Div(msg, style={'font-size': '10px'}), html.Div(msg, style={'font-size': '10px'}), html.Div(msg, style={'font-size': '10px'})

@app.callback(Output('save_stamp', 'children'),
    Input('btn-nclicks-3', 'n_clicks'),)

def upload_file(btn3):
    if btn3 < 1:
        msg = "File not saved"
        return html.Div(msg, style={'font-size': '10px'})
    else:
        msg = "File saved"
        
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)
        s_buf = io.BytesIO()
        data.to_excel(s_buf)
        file_metadata = {'name': 'Excel Report','mimeType': 'application/vnd.google-apps.spreadsheet'}
        media = MediaIoBaseUpload(s_buf, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', resumable=True)
        service.files().create(body=file_metadata, media_body=media,fields='id').execute()

        return html.Div(msg, style={'font-size': '10px'})


if __name__ == '__main__':
    app.run_server(debug=True,  host='0.0.0.0', port=8050, use_reloader=False)
        

       
    