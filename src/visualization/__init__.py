import matplotlib.pyplot as plt
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import confusion_matrix
from sklearn import decomposition

import numpy as np
import pandas as pd

from IPython.display import display, Markdown, Latex,HTML


def plot_pca_spectrum(data):
	pca = decomposition.PCA()
	pca.fit(data)
	plt.figure(1, figsize=(12, 9))
	plt.clf()
	plt.axes([.2, .2, .7, .7])
	plt.plot(pca.explained_variance_, linewidth=2)
	np.savetxt("matrix.csv", pca.explained_variance_)
	plt.axis('tight')
	plt.xlabel('n_components')
	plt.ylabel('explained_variance_')
	plt.show()

def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    #classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    #print(cm)

    fig, ax = plt.subplots( figsize=(8, 8))
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax



week_day = ["Segunda-feira","Terça-feira","Quarta-feira","Quinta-feira","Sexta-feira","Sábado","Domingo"]
def plot_motivo(motivo,dias=[0,1,2,3,4,5,6],variable_name = "SKY Motivo Contato",colors=[],color_auto_generate=False):
    if isinstance(dias,list) or isinstance(dias,np.ndarray):   
        print(variable_name) 
        title = "Quantidade de "+str(variable_name)+" do(s) dia(s): " + week_day[int(dias[0])]
        for dia in dias[1:]:
            title = title +  ", " + week_day[int(dia)]
    else:
        title = "Quantidade de "+str(variable_name)+" do(s) dia(s): " + week_day[int(dias)]
    
    plot(motivo,title,variable_name,colors,color_auto_generate)
    
def plot(motivo,title,variable_name = "SKY Motivo Contato",colors=[], color_auto_generate=False):
    
    fig, ax = plt.subplots(figsize=(12, 6), subplot_kw=dict(aspect="equal"))
    if(colors.__len__() > 0):
        wedges, texts,_ = ax.pie(motivo["Quantidade"].values,   textprops=dict(color="w"), autopct=lambda pct: define_text(pct, motivo["Quantidade"].values),colors=colors)
    else:        
        if 'cores' in motivo.columns and not color_auto_generate:
            wedges, texts,_ = ax.pie(motivo["Quantidade"].values,   textprops=dict(color="w"), autopct=lambda pct: define_text(pct, motivo["Quantidade"].values),colors=motivo["cores"].values)
          
        else:            
            wedges, texts,_ = ax.pie(motivo["Quantidade"].values,   textprops=dict(color="w"), autopct=lambda pct: define_text(pct, motivo["Quantidade"].values))

    string_legend = [""+ str(qtd)  for qtd in motivo[variable_name].values]
    ax.legend(wedges, string_legend,
            title=variable_name,
            loc="center left",
            bbox_to_anchor=(1.5, 0.1, 0.1, 1))
    ax.set_title(title)

    plt.show()


def define_text(pct, allvals):  
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d} )".format(pct, absolute)



def plot_crm_criador_dia(__crm__):
    crm_group_criador = __crm__.groupby(["Usuario Criador","dia semana"]).size().reset_index().sort_values(by=[0],ascending=False)
    crm_group_criador.rename(columns={0:'Quantidade'}, inplace=True)

    criador_e = crm_group_criador[crm_group_criador["Usuario Criador"].str.contains('E2')]
    criador_e =  pd.concat([criador_e,crm_group_criador[crm_group_criador["Usuario Criador"].str.contains('E6')]])

    criador_c = crm_group_criador[crm_group_criador["Usuario Criador"].str.contains('C0')]

    for dia in __crm__["dia semana"].unique(): 
        criador_e_dia = criador_e[criador_e["dia semana"] == dia]
        criador_c_dia = criador_c[criador_c["dia semana"] == dia]
        criador_e_c = pd.DataFrame(data={"Usuario Criador": ["Criador E2...", "Criador C0..."],"Quantidade": [criador_e_dia.sum()["Quantidade"], criador_c_dia.sum()["Quantidade"]],"dia semana":[dia,dia]})

        criador_not_e = crm_group_criador[~crm_group_criador["Usuario Criador"].str.contains('E2')]
        criador_not_e = criador_not_e[~criador_not_e["Usuario Criador"].str.contains('E6')]
        criador_not_ec = criador_not_e[~criador_not_e["Usuario Criador"].str.contains('C0')]
        criador_not_ec = criador_not_ec[criador_not_ec["dia semana"] == dia]

        criador_grouped = pd.concat([criador_e_c,criador_not_ec],sort=False)

        plot_motivo(criador_grouped,[dia],variable_name="Usuario Criador")

colors = ["#ff7f0e","#2ca02c","#4286f4","purple","indianred","peru","gold","royalblue","crimson","deeppink","olive","teal","lime","slategray"]
def generate_colors_for_array(color_keys):    
    if(colors.__len__() < color_keys.__len__()):
        multiply_constant = int(color_keys.__len__() / colors.__len__())
        colors_to_sum = colors.copy()
        [colors.extend(colors_to_sum) for i in range(multiply_constant)]
        
    return dict(zip(color_keys, colors[:color_keys.__len__()]))

def generate_colors(size):  
    while(colors.__len__() < size):       
        colors_to_sum = colors.copy()
        colors.extend(colors_to_sum) 
    return colors[:size]

def plot_clusters(sms_input_output):

    sms_input_output_grouped = sms_input_output.groupby(["cluster_id_output","cluster_id_input"]).size().reset_index()
    for cluster in sms_input_output_grouped["cluster_id_input"].unique():
        sms_filtered_grouped = sms_input_output_grouped[sms_input_output_grouped["cluster_id_input"] == cluster]
        sms_filtered_grouped.sort_values(by=[0],ascending=False)   
        sms_filtered_grouped.rename(columns={0:'Quantidade'}, inplace=True)
        sms_filtered_grouped = sms_filtered_grouped.head(10)

        plot(sms_filtered_grouped,"Plot Clusterizado.",["cluster_id_input","cluster_id_output"])

        print("Exemplo de Input clusterizado: ")
        print("------------")       
        print(sms_input_output[sms_input_output["cluster_id_input"] == cluster].head(1)["DES_InputText"].values[0])
        print(sms_input_output[sms_input_output["cluster_id_input"] == cluster].head(2)["DES_InputText"].values[1])
        print(sms_input_output[sms_input_output["cluster_id_input"] == cluster].head(3)["DES_InputText"].values[2])
        print(sms_input_output[sms_input_output["cluster_id_input"] == cluster].head(4)["DES_InputText"].values[3])
        
        print("------------")
        
        cluster_output_values = sms_input_output_grouped[sms_input_output_grouped["cluster_id_input"] == cluster].sort_values(by=[0],ascending=False).head(1)["cluster_id_output"].values
        if(cluster_output_values.__len__() > 0):
            print("Exemplo de Output clusterizado, do maior cluster")
            print("------------")
            cluster_id_output = cluster_output_values[0]
            print(sms_input_output[sms_input_output["cluster_id_output"] == cluster_id_output].head(4)["DES_OutputText"].values[0:5])
            print("------------")