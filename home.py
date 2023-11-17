import base64 # to use images
import os # to use os.system('cls')

# dash features
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

# import my files and their functions
from like_it_p01 import search
from fell_dash import to_create, analyze_google, create_cloud
from graphs import pie_graph, bar_chart
from hugging_face import hf_analysis

# to show the logo
image_filename = 'logo.png'
encoded_logo= base64.b64encode(open(image_filename, 'rb').read()).decode()


app = Dash(__name__) # initialize the Dash application

# the layout 
app.layout = html.Div(
    className ='div_layout',
    children = [
        # show the logo
        html.Img(src = 'data:image/png;base64,{}'.format(encoded_logo), width = '200px', className = 'logo_image'),
        html.Br(), # line break
        html.Div([
            html.Label('Digite o produto:' , className = 'centralized_title'), # show request
            html.Br(), # line break
            html.Br(), # line break
            dcc.Input(id = 'input-box', type = 'text', className = 'input_box'), # input box to insert the name product
            html.Button('🔎', id = 'search-button', n_clicks = 0, className ='round_button') # button to accion
        ], ),

        html.Br(), # line break

        html.Div(id='output-container') # output

    ],
)


def show_cloud(): # function created to use base64 and show the cloud
    encoded_cloud = base64.b64encode(open('nuvem.png', 'rb').read()).decode()
    return  html.Img(src='data:image/png;base64,{}'.format(encoded_cloud), width='400px')


def empty_div(width, height): # creates an empty div and can define width and height 
    return html.Div(style={'opacity': 0, 'width': width, 'height': height})


def comment_box(list): # return divs about comments
    formatted_text = '\n  -'.join(list) # single string with line breaks between values
    
    return html.Div([
        html.H2("Comentarios sobre:"),
        html.Div([
            html.Label(""),
            dcc.Textarea(
                id = 'texto-nao-editavel',
                value = formatted_text,
                readOnly = True,
                className = 'comments_box'  
                        ),
                ])
                    ])

# Define a callback function that updates the content of an HTML element.
@app.callback(
    Output('output-container', 'children'),  # Define the output element to be updated
    Input('search-button', 'n_clicks'),       # Define the input trigger, such as a button click
    State('input-box', 'value')               # Define the current value of an input box
)

def search_product(n_clicks, input_value): # execution 

    if n_clicks > 0:       
        if input_value is None or input_value == '': # no execution 
            return ['Digite algo!']
        
        else: # start 
            os.system('cls') # clear the terminal

            print('Step 1') 
            comments = search(input_value) # search with web scraping function
            
            print('Step 2')
            analyze = analyze_google(comments) # analyzes comments via Google Cloud
            
            print('Step 3')
            to_create(comments, analyze) # creates a csv

            print('Step 4') 
            hf_analysis(comments, 'pt')
            values = hf_analysis(comments, 'pt')
            
            
            print('Step 5') 
            #list with the product name and common words that do not attribute usefulness to cloud
            words = [input_value.lower(), input_value.upper(), input_value, 'Produto', 'produto', 'compra',
                      'comprei', 'comprado', 'comprou', 'compramos', 'compraram', 'qualidade', 'usei', 'ate']
            
            create_cloud(comments, words)           
            print('Steps Completed')
            
            # output interface and calls
            x = html.Div([
                        html.Div([empty_div(150,200), 
                                  pie_graph(),
                                  empty_div(100,200),    
                                  bar_chart(values)], 
                                  style={'display': 'flex'} ),

                        html.Div(show_cloud(),
                                 className= 'show_cloud'),

                        html.Div(comment_box(comments), 
                                 className= 'div_comments')
                    ])                                        
            return x
    return ['']

if __name__ == '__main__': # run server
    app.run_server(debug=False)
