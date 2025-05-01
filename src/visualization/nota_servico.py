import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from IPython.display import display, Markdown, Latex,HTML
from urllib.request import urlopen

import sys
sys.path.append("../../")

import pandas as pd
pd.options.display.max_columns = None
import numpy as np
from dateutil.parser import parse

import folium
from folium.plugins import HeatMap,HeatMapWithTime
import datetime

#Internal -- imports
from src.models import load_crm,split_users_bot_human,sms_clusterization
from src.visualization import *
from src.visualization.html_visualization import *
from src.data.nota_servico_dataset import *
from src.data.servico_dataset import *



def nprintRelacaoTempo(nota_servico_classe,nome=""):
    display(HTML("<span class='title'>"+nome+"</span>"))    
    nprint("Tempo medio :",nota_servico_classe[nota_servico_classe["Quantidade"] > 1]["Tempo Entre Reclamacao"].mean())
    nprint("Tempo medio Inicial e final para :",nota_servico_classe[nota_servico_classe["Quantidade"] > 1]["Tempo Entre Reclamacao Inicial Final"].mean())
    nprint("Quantidade Media de Nota Serviço por Serviço para :",nota_servico_classe[nota_servico_classe["Quantidade"] >1]["Quantidade"].mean())
    nprint("Tempo médio para Resolução do Serviço :",nota_servico_classe[nota_servico_classe["Quantidade"] >1]["Tempo Entre Reclamacao Inicial Fim Servico"].mean())
    display(Markdown("---"))
    display(HTML("<br>"))


def plotLineClasseSubClasse(dict_classe_sub_classe,atribute,with_std=False,limit=8):
    
    for key in dict_classe_sub_classe.keys():
        classe_subclasse = groupbyTempoQuantidade(dict_classe_sub_classe[key])
        means = [classe_subclasse[classe_subclasse["Quantidade"] >= x][atribute].mean().seconds / 60 for x in range(1,limit)]
        
        if(with_std):
            std = [classe_subclasse[classe_subclasse["Quantidade"] >= x][atribute].std().seconds / 60 for x in range(1,limit)]    
            plt.errorbar(np.arange(1,limit), means,yerr=std,  label=key)
        else:
            plt.errorbar(np.arange(1,limit), means, label=key)
    
    plt.legend(bbox_to_anchor=(1.1,1.0))


def __getDictDefault(dict,key):
    if(key in dict):
        return dict[key]
    else:
        return ""


def __conditionalLabel(pct):
    return ("%1.1f" % pct) if pct >= 3 else ''


def plotDistribuicao(nota_servico):

    labels_dict = {
        "[10.  1.]":"Residencial",
        "[40.  1.]":"Agropecuária Rural",
        "[10.  2.]":"Res Baixa Renda",
        "[30.  4.]":"Outros Serviços e Outras Ativ",
        "[30.  1.]":"Comercial",
        "[40.  9.]":"Residencial rural",
        "[20.  1.]":"Industrial",
        "[30.  3.]":"Serviços de Comunic. Telec",
        "[40. 25.]":"Irrig. Noturna D. Regiões",
        "[50.  5.]":"Poder Publico Municipal",
        "[40. 15.]":"Irrig. Noturna SUDENE/IDENE",
        "[30.  8.]":"Administração Condominial",
        "[70.  2.]":"Água Esgoto e Saneamento",
        "[30.  7.]":"Templos Religiosos",
        "[40.  4.]":"Não Existe no Dicionario",
    }
    total   = nota_servico.shape[0]
    grouped = nota_servico.groupby(["IND_CLASSE","IND_SUBCLASSE"]).size().reset_index().sort_values(0,ascending=False).head(10)
    labels  = [__getDictDefault(labels_dict,str(classe)) for classe in grouped[["IND_CLASSE","IND_SUBCLASSE"]].values]
    values  = grouped[0].values
                                                                                        
    labels = [n if  v >= total * 0.0285 else ''
              for n, v in zip(labels, values)]                       

 

    fig1, ax1 = plt.subplots()
    ax1.pie(values,labels=labels, autopct=__conditionalLabel,
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()
