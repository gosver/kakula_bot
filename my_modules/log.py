import os

from datetime import datetime

#log write

def write_log(message):
    
    #current dirrectory
    #cur_dir = os.path.join(os.getcwd(), os.path.dirname(__file__).parents[1])
    
    dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
    
    with open(dir+"/_log.txt", "a", encoding='utf-8') as file:
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        file.write(dt_string+' '+message+'\n')