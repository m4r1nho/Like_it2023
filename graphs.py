import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)

def pie_graph():
    values = [] # list 
    likes = 0 # like counter  
    dislikes = 0 # dislike counter
    neutral = 0

    df = pd.read_csv('file_google.csv') # a dataframe of file.csv
    scores = df['Score'].to_list() # scores list

    # were defined based on the score value
    for i in scores: 
        if i < -0.1:
            dislikes += 1
        elif i > 0.2: 
            likes += 1
        else:
            neutral +=1

    values.append(likes)
    values.append(neutral)
    values.append(dislikes)

    data = pd.DataFrame({'Categoria': ['Positivo +', 'Neutro o', 'Negativo -'], 'Valores': values}) # dataframe to graph

    colors = ['#00FA9A','gray', '#FF7F50'] 

    fig = px.pie(data, names='Categoria', values='Valores', width = 470, height = 420) # fig 

    fig.update_traces(marker=dict(colors=colors)) # define colors 


# Update the layout of a Plotly figure:
    fig.update_layout(
        paper_bgcolor='rgba(12, 138, 196, 0)',  # Set the background color of the plot to transparent

        # Add an annotation to the figure, which is the title
        annotations=[
            dict(
                text="<b> Grafico de Pizza",   # text to be displayed, with HTML formatting (bold)
                showarrow=False,        # don't show an arrow pointer
                xref="paper",           # relative to the entire plot area
                yref="paper",           # relative to the entire plot area
                x=0.5,                  # X-coordinate (0.5 means the center of the plot)
                y=1.0,                  # Y-coordinate (1.0 means the top of the plot)
                yanchor="bottom",       # anchor point for the y-coordinate 
                xanchor="center",       # anchor point for the x-coordinate 
                font=dict(size=20)      # font size 
                )
                    ]
                    )


    fig.update_layout(margin=dict(t=100)) # adjust the top margin of the Plotly figure by 100 units

    x = html.Div(
        children=[
            dcc.Graph(figure=fig)
                 ],
        style={'display': 'justify-content'}
                )
    
    return x

def bar_chart(values):

    emotions = ['Amor', 'Alegria','Surpresa', 'Medo', 'Tristeza', 'Raiva']
    
    colors = ['#FFFF00', '#9370DB', '#556B2F', '#2F4F4F', '#4169E1', '#FF4500']
    
    
    total = sum(values)
    
    percentages = [(v / total) * 100 for v in values]
    percentages = [f'{p:.2f}%' for p in percentages]  
    
    data = {'Nomes': emotions, 'Valores': values, 'Porcentagens': percentages}
    df = pd.DataFrame(data)

    # Criar a figura com Plotly Express
    fig = px.bar(df, x = 'Valores', y = 'Nomes', color = 'Nomes', orientation = 'h', title = "Grafico de Emoções", 
                 barmode = 'relative', color_discrete_sequence = colors, text = 'Porcentagens')

    
    fig.update_traces(marker_line_width=2, marker_line_color='white')

    # remove showticklabels  and showgrids
    fig.update_xaxes(showticklabels=False, showgrid=False, title_text='')
    fig.update_yaxes(showticklabels=False, showgrid=False, title_text='')

    # transparent backgroud
    fig.update_layout({
        
        'plot_bgcolor' :  'rgba(0, 0, 0, 0)',
        'paper_bgcolor':  'rgba(255, 255, 255, 0.25)',
        'legend': {'bgcolor': 'rgba(255, 255, 255, 0.75)'},
        'title_x': 0.5,
        'title_font': {'size': 30}
                      })

    fig.update_yaxes(showline=False, linewidth=0) # transparent Y axis line
    
    x = html.Div(
        children=[
            dcc.Graph(figure=fig)
        ],
        className='classe_barra'
                )
    
    return x



