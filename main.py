from base10 import convert_base10_to_n,convert_n_to_base10
from binarybases import convert_base2_to_n,convert_base_n_to_2,convert_base_n_to_n



def convert(number,base,target_base,animate=True,show_table=True):
    if base == 10:
        return convert_base10_to_n(number,target_base,animation=animate)
       
    if target_base == 10:
       return convert_n_to_base10(number,base,animation=animate)
        
    
    if base==2:
        return convert_base2_to_n(number,target_base,animation=animate,show_table=show_table)

    if target_base==2:
        return convert_base_n_to_2(number,base,animation=animate,show_table=show_table)

    if base in [2,4,8,16] and target_base in [2,4,8,16]:
        return convert_base_n_to_n(number,base,target_base,animation=animate,show_table=show_table)

    raise ValueError("conversion between the specified bases is not supported.")
