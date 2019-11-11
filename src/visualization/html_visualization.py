from IPython.display import display, Markdown, Latex,HTML

def html_print_key_value(title_key = "",title_value = "",key = "",value = ""):
    return display(HTML("<span class='title'>"+title_key+":</span> <span class='values'>" + str(key) + "</span><br>" + 
     "<span class='title'>"+title_value+":</span> <span class='value'>" + str(value) + "</span>"))


def nprint(a,b=[]):
     if(b == []):
          display(HTML("<span class='nprint'>"+str(a)+"</span>"))
     else:
          display(HTML("<span class='title'>"+a+"</span> <span class='values'>" + str(b)))

