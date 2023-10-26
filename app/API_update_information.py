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

def load_imgs(p1, p2):
    g = 100
    IMG1 = cv2.imread(p1)
    IMG2 = cv2.imread(p2)
    IMG1 = cv2.resize(IMG1, (512, 512),interpolation=cv2.INTER_CUBIC)  # set to 256x256
    IMG2 = cv2.resize(IMG2, (512, 512),interpolation=cv2.INTER_CUBIC)  # set to 256x256
    diff = int(round((IMG1.shape[1]/2)-80, 0))
    Top_Block = np.zeros((g, IMG1.shape[1], 3))
    Top_Block[:,:,:] = 255
    IMG1 = np.concatenate((Top_Block, IMG1), axis=0)
    IMG2 = np.concatenate((Top_Block, IMG2), axis=0)
    IMG1 = cv2.putText(IMG1,'MLO',(diff,70), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 0), 2, cv2.LINE_AA)
    IMG2 = cv2.putText(IMG2,'CC',(diff,70), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 0), 2, cv2.LINE_AA)
    Gap = np.zeros((IMG1.shape[0], 50, 3))
    Gap[:,:,:] = 255
    joined = np.concatenate((IMG1, Gap, IMG2), axis=1)
    return joined

INVTYPE = ["yes", "no"]
SHAPE = ["ill_defined",  "well_defined", "spiculated", "other", "indiscriminable"]
SYMMETRY = ["yes", "no"]
Mass = ["yes", "no"]
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
    html.Button('Previous', id='btn-nclicks-1', n_clicks=0, style={'font-size': '16px', 'width': '240px', 'display': 'inline-block', 'margin-bottom': '10px', 'margin-right': '5px', 'height':'50px'}),
    html.Button('Next', id='btn-nclicks-2', n_clicks=0, style={'font-size': '16px', 'width': '240px', 'display': 'inline-block', 'margin-bottom': '10px', 'margin-right': '5px', 'height':'50px'}),
    html.Div(id='container-button-timestamp'),
    
    html.Div(dcc.Graph(id='EXAMPLE', style={'display': 'inline-block', 'height':'100%', 'width':'100%'})),
    html.Div(children = ["Are there Calcifications?",dcc.Dropdown(id='Invisive_dropdown', options = [{"label": i, "value": i} for i in INVTYPE], value = [], clearable=True), html.Div(id='INVTYPE_UPDATE')]),
    html.Div(children = ["Lesion shape",dcc.Dropdown(id='Shape_dropdown', options = [{"label": i, "value": i} for i in SHAPE], value = [], clearable=True), html.Div(id='SHAPE_UPDATE')]),
    html.Div(children = ["Symmetry",dcc.Dropdown(id='Symmetry_dropdown', options = [{"label": i, "value": i} for i in SYMMETRY], value = [], clearable=True), html.Div(id='SYMMETRY_UPDATE')]),
    html.Div(children = ["Is there a Mass",dcc.Dropdown(id='Mass_dropdown', options = [{"label": i, "value": i} for i in Mass], value = [], clearable=True), html.Div(id='MASS_UPDATE')]),
    ])


@app.callback(Output('EXAMPLE','figure'),
    Output('container-button-timestamp', 'children'),
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
        IMG_NAME1 = data["MLO_C"].iloc[0]
        P1 = os.path.join("/app/Segs", "{}.png".format(IMG_NAME1))
        IMG_NAME2 = data["CC_C"].iloc[0]
        P2 = os.path.join("/app/Segs", "{}.png".format(IMG_NAME2))
        IMG = load_imgs(P1, P2)
        DISPLAY = px.imshow(IMG)
        
        DISPLAY.update_layout(coloraxis_showscale=False)
        DISPLAY.update_xaxes(showticklabels=False)
        DISPLAY.update_yaxes(showticklabels=False)
        
        return DISPLAY, html.Div(msg, style={'font-size': '20px'}), data["MalignancyType"].iloc[0], data["MassClassification"].iloc[0], data["SYMMETRY"].iloc[0], data["Mass"].iloc[0]
       
    else:
        msg = "Image index {}".format(bt)
        IMG_NAME1 = data["C_MLO"].iloc[bt]
        P1 = os.path.join("/app/Segs", "{}.png".format(IMG_NAME1))
        IMG_NAME2 = data["C_CC"].iloc[bt]
        P2 = os.path.join("/app/Segs", "{}.png".format(IMG_NAME2))
        IMG = load_imgs(P1, P2)
        DISPLAY = px.imshow(IMG)
        
        DISPLAY.update_layout(coloraxis_showscale=False)
        DISPLAY.update_xaxes(showticklabels=False)
        DISPLAY.update_yaxes(showticklabels=False)
        
        return DISPLAY, html.Div(msg, style={'font-size': '20px'}), data["Calcifications"].iloc[bt], data["MassClassification"].iloc[bt], data["SYMMETRY"].iloc[bt], data["Mass"].iloc[bt]

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
        bSY = data["SYMMETRY"].iloc[bt]
        bMA = data["Mass"].iloc[bt]
        if bIN != vIn or bSH != vSh or bSY != vSy or bMA != vMa:
            msg = "Updated"
            msg2 = "No_Update"
            if bIN != vIn:
                data["Calcifications"].iloc[bt] = vIn
                #data.to_excel(EXCEL_PATH)
                return html.Div(msg, style={'font-size': '10px'}), html.Div(msg2, style={'font-size': '10px'}),html.Div(msg2, style={'font-size': '10px'}),html.Div(msg2, style={'font-size': '10px'})
            elif bSH != vSh:
                data["MassClassification"].iloc[bt] = vSh
                #data.to_excel(EXCEL_PATH)
                return html.Div(msg2, style={'font-size': '10px'}), html.Div(msg, style={'font-size': '10px'}),html.Div(msg2, style={'font-size': '10px'}),html.Div(msg2, style={'font-size': '10px'})
            elif bSH != vSh:
                data["SYMMETRY"].iloc[bt] = vSy
                #data.to_excel(EXCEL_PATH)
                return html.Div(msg2, style={'font-size': '10px'}), html.Div(msg2, style={'font-size': '10px'}),html.Div(msg, style={'font-size': '10px'}),html.Div(msg2, style={'font-size': '10px'})
            elif bMA != vMa:
                data["Mass"].iloc[bt] = vMa
                #data.to_excel(EXCEL_PATH)
                return html.Div(msg2, style={'font-size': '10px'}), html.Div(msg2, style={'font-size': '10px'}),html.Div(msg2, style={'font-size': '10px'}),html.Div(msg, style={'font-size': '10px'})
            
    msg = "No-Updated"
    return html.Div(msg, style={'font-size': '10px'}),html.Div(msg, style={'font-size': '10px'}), html.Div(msg, style={'font-size': '10px'}), html.Div(msg, style={'font-size': '10px'})

if __name__ == '__main__':
    app.run_server(debug=True,  host='0.0.0.0', port=8050)
        

       
    