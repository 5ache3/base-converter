from manimlib import *
from matplotlib.table import table

def get_label_string(bin):
    n=len(bin)
    s=0
    for i in range(n):
        s+=int(bin[n-1-i])*(2**i)
    if s>10:
        return hex(s)[2:].upper()
    return str(s)

def get_char_value(c):
    d={'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,
       'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}
    return d[c]

def binaryrep(num,base):
    b=str(bin(num))[2:]
    l=3 if base==8 else 4 if base == 16 else 2
    while len(b)<l:
        b='0'+b
    return b
class Frombase2(Scene):
    def __init__(self,number,base,animate=True,show_table=True,bg=None,**kwargs):
        self.number=number
        self.base=base
        self.animate=animate
        self.show_table=show_table
        super().__init__(
                   file_writer_config={"write_to_movie":True,"file_name":f"{number}-B2_to_B{base}"},
                   camera_config={"background_color":bg if bg else BLACK},
                   **kwargs)


    def construct(self):
        table=VGroup(
        Text("nombres en binaire :"),
        VGroup(Tex("0"),Tex("="),Tex("0000")).arrange(RIGHT*1.25),
        VGroup(Tex("1"),Tex("="),Tex("0001")).arrange(RIGHT*1.25),
        VGroup(Tex("2"),Tex("="),Tex("0010")).arrange(RIGHT*1.25),
        VGroup(Tex("3"),Tex("="),Tex("0011")).arrange(RIGHT*1.25),
        VGroup(Tex("4"),Tex("="),Tex("0100")).arrange(RIGHT*1.25),
        VGroup(Tex("5"),Tex("="),Tex("0101")).arrange(RIGHT*1.25),
        VGroup(Tex("6"),Tex("="),Tex("0110")).arrange(RIGHT*1.25),
        VGroup(Tex("7"),Tex("="),Tex("0111")).arrange(RIGHT*1.25),
        VGroup(Tex("8"),Tex("="),Tex("1000")).arrange(RIGHT*1.25),
        VGroup(Tex("9"),Tex("="),Tex("1001")).arrange(RIGHT*1.25),
        VGroup(Tex("A"),Tex("="),Tex("1010")).arrange(RIGHT*1.25),
        VGroup(Tex("B"),Tex("="),Tex("1011")).arrange(RIGHT*1.25),
        VGroup(Tex("C"),Tex("="),Tex("1100")).arrange(RIGHT*1.25),
        VGroup(Tex("D"),Tex("="),Tex("1101")).arrange(RIGHT*1.25),
        VGroup(Tex("E"),Tex("="),Tex("1110")).arrange(RIGHT*1.25),
        VGroup(Tex("F"),Tex("="),Tex("1111")).arrange(RIGHT*1.25),
    ).arrange(DOWN).to_corner(RIGHT).scale(.65).shift(RIGHT).set_opacity(.7)
        box=SurroundingRectangle(table,color=WHITE,stroke_opacity=.7)

        base=self.base
        number=self.number
        animate=self.animate
        show_table=self.show_table

        if animate or show_table:
            self.add(table,box)

        num_str=str(number)
        n=len(num_str)
        if base not in [2,4,8,16]:
            raise ValueError("Base must be one of 2,4,8,16")
        group_size={2:1,4:2,8:3,16:4}[base]

        bits=VGroup(*[Tex(num_str[i]) for i in range(n)]).arrange(RIGHT,buff=0.1).to_edge(UP).shift(LEFT+DOWN)


        grouped_bits=VGroup()
        for i in range(0,n,group_size):
            
            group=VGroup(*[bits[::-1][j].copy() for j in range(i,min(i+group_size,n))])
            grouped_bits.add(group)
        grouped_bits=grouped_bits[::-1]
        grouped_bits.arrange(RIGHT,buff=0.3).move_to(bits.get_center()).shift(DOWN*2)
        
        labels_group=VGroup(*[
                        Tex(
                            get_label_string(''.join([x.get_string() for x in bits[::-1][i*group_size:(i+1)*group_size]])[::-1])
                            ).move_to(grouped_bits[::-1][i].get_center()+DOWN*.75)
                            for i in range(len(grouped_bits))])
        labels_group=labels_group[::-1]

        result=VGroup(*[c.copy() for c in labels_group]).arrange(RIGHT).next_to(labels_group,DOWN*1.5)

        main_result=VGroup(
            VGroup(Tex("("),bits.copy(),Tex(")_{2}")).arrange(RIGHT,buff=.1)
            ,Tex("="),
            VGroup(Tex("("),result.copy(),Tex(f")_{{{base}}}")).arrange(RIGHT,buff=.1)
            ).arrange(RIGHT).move_to(ORIGIN).shift(DOWN*2.5+LEFT)
        
        if animate:
            self.play(Write(bits))
            self.play(
                *[TransformMatchingParts(bits[::-1][i*group_size:(i+1)*group_size],grouped_bits[::-1][i]) for i in range(len(grouped_bits))]
                )
        
            for i in range(len(grouped_bits)):
                val=get_char_value(labels_group[i].get_string())
                print(val)
                self.play(FadeIn(labels_group[i]),Indicate(grouped_bits[i]),Indicate(table[val+1][0]),Indicate(table[val+1][2]))
            self.play(TransformMatchingParts(labels_group.copy(),result))
            self.play(TransformMatchingParts(result,main_result[2][1]),FadeIn(VGroup(main_result[:2],main_result[2][0],main_result[2][2])))

            if not show_table:
                self.play(FadeOut(VGroup(table,box)))
                self.play(FadeOut(VGroup(grouped_bits,labels_group)),main_result.animate.move_to(ORIGIN))
            else:
                self.play(FadeOut(VGroup(grouped_bits,labels_group)),main_result.animate.move_to(ORIGIN+LEFT))

            
        else:
            self.add(grouped_bits)
            self.add(labels_group)
            self.add(main_result)
            self.wait()

def get_table_and_box():
    table=VGroup(
        Text("nombres en binaire :"),
        VGroup(Tex("0"),Tex("="),Tex("0000")).arrange(RIGHT*1.25),
        VGroup(Tex("1"),Tex("="),Tex("0001")).arrange(RIGHT*1.25),
        VGroup(Tex("2"),Tex("="),Tex("0010")).arrange(RIGHT*1.25),
        VGroup(Tex("3"),Tex("="),Tex("0011")).arrange(RIGHT*1.25),
        VGroup(Tex("4"),Tex("="),Tex("0100")).arrange(RIGHT*1.25),
        VGroup(Tex("5"),Tex("="),Tex("0101")).arrange(RIGHT*1.25),
        VGroup(Tex("6"),Tex("="),Tex("0110")).arrange(RIGHT*1.25),
        VGroup(Tex("7"),Tex("="),Tex("0111")).arrange(RIGHT*1.25),
        VGroup(Tex("8"),Tex("="),Tex("1000")).arrange(RIGHT*1.25),
        VGroup(Tex("9"),Tex("="),Tex("1001")).arrange(RIGHT*1.25),
        VGroup(Tex("A"),Tex("="),Tex("1010")).arrange(RIGHT*1.25),
        VGroup(Tex("B"),Tex("="),Tex("1011")).arrange(RIGHT*1.25),
        VGroup(Tex("C"),Tex("="),Tex("1100")).arrange(RIGHT*1.25),
        VGroup(Tex("D"),Tex("="),Tex("1101")).arrange(RIGHT*1.25),
        VGroup(Tex("E"),Tex("="),Tex("1110")).arrange(RIGHT*1.25),
        VGroup(Tex("F"),Tex("="),Tex("1111")).arrange(RIGHT*1.25),
    ).arrange(DOWN).to_corner(RIGHT).scale(.65).shift(RIGHT).set_opacity(.7)
    box=SurroundingRectangle(table,color=WHITE,stroke_opacity=.7)

    return table,box
class Tobase2(Scene):
    
    def __init__(self,number,base,animate=True,show_table=True,bg=None,**kwargs):
        self.number=number
        self.base=base
        self.animate=animate
        self.show_table=show_table
        super().__init__(
                   file_writer_config={"write_to_movie":True,"file_name":f"{number}-B{base}_to_B2"},
                   camera_config={"background_color":bg if bg else BLACK},
                   **kwargs)
        
    def construct(self):
        

        base=self.base
        number=self.number
        animate=self.animate
        show_table=self.show_table

        num_str=str(number)
        n=len(num_str)
        table,box=get_table_and_box()
        if base not in [2,4,8,16]:
            raise ValueError("Base must be one of 2,4,8,16")
        
        group_size={2:1,4:2,8:3,16:4}[base]

        if animate or show_table:
            self.add(table,box)
        
        number_tex=VGroup(*[Tex(c) for c in num_str]).arrange(RIGHT,buff=.1).to_edge(UP).shift(DOWN+LEFT*(animate or show_table))
        
        bf=.7 if base == 8 else .9 if base == 16 else .3
        buffed_num=VGroup(*[Tex(c) for c in num_str]).arrange(RIGHT,buff=bf).next_to(number_tex,DOWN*2)
        bin_num=VGroup(*[Tex(binaryrep(get_char_value(num_str[i]),base)).next_to(buffed_num[i],DOWN) for i in range(n)])
        result=VGroup(
                    VGroup(Tex("("),Tex(num_str),Tex(f")_{{{base}}}")).arrange(RIGHT,buff=.1),
                    Tex("="),
                    VGroup(Tex("("),VGroup(*[c.copy() for c in bin_num]).arrange(RIGHT,buff=.15),Tex(")_{2}")).arrange(RIGHT,buff=.1)
                    ).arrange(RIGHT).next_to(bin_num,DOWN*2)

        if animate:
            self.play(Write(number_tex))
            self.play(TransformMatchingParts(number_tex,buffed_num))
            for i in range(n):
                val=get_char_value(num_str[i])
                self.play(FadeIn(bin_num[i]),Indicate(buffed_num[i]),Indicate(table[val+1][0]),Indicate(table[val+1][2]))
            self.play(TransformMatchingParts(bin_num.copy(),result[2][1]),FadeIn(VGroup(result[:2],result[2][0],result[2][-1])))
            
            if not show_table:
                self.play(FadeOut(VGroup(table,box)))
                self.play(FadeOut(VGroup(buffed_num,bin_num)),result.animate.move_to(ORIGIN))
            else:
                self.play(FadeOut(VGroup(buffed_num,bin_num)))

        else:
            self.add(number_tex,buffed_num,bin_num,result)
            self.wait()


class InterBase2(Scene):

    # def __init__(self,number,str_base,end_base,animate=True,show_table=True,bg=None,**kwargs):
    #     self.number=number
    #     self.str_base=str_base
    #     self.end_base=end_base
    #     self.animate=animate
    #     self.show_table=show_table
    #     super().__init__(
    #                 file_writer_config={"write_to_movie":True,"file_name":f"{number}-B{str_base}_to_B{end_base}"},
    #                 camera_config={"background_color":bg if bg else BLACK},
    #                 **kwargs)
   
    def construct(self):
        number='62F21'
        str_base=16
        end_base=8
        animate=False
        show_table=False
        bf1=.7 if str_base == 8 else .9 if str_base == 16 else .3
        bf2=.7 if end_base == 8 else .9 if end_base == 16 else .3
        group_size1={2:1,4:2,8:3,16:4}[str_base]
        group_size2={2:1,4:2,8:3,16:4}[end_base]
        if str_base not in [2,4,8,16] or end_base not in [2,4,8,16]:
            raise ValueError("starting and ending bases must be powers of 2 (2,4,8,16)")
        
        str_num=str(number)
        n=len(str_num)
        num_tex=VGroup(*[Tex(c) for c in str_num]).arrange(RIGHT,buff=.1).to_edge(UP).shift(DOWN+LEFT*(animate or show_table))
        num_tex_sep=VGroup(*[Tex(c) for c in str_num]).arrange(RIGHT,buff=bf1).next_to(num_tex,DOWN*2)
        bits=VGroup(*[Tex(binaryrep(get_char_value(str_num[i]),str_base)).next_to(num_tex_sep[i],DOWN) for i in range(n)])
        bits2=VGroup(*[Tex(c) for c in ''.join([bit.get_string() for bit in bits])]).arrange(RIGHT,buff=.1).next_to(bits,DOWN*2)
        
        bits2_sep=VGroup(*[Tex(''.join([bit.get_string() for bit in bits2[::-1][i:i+group_size2]])[::-1]) for i in range(0,len(bits2),group_size2)])[::-1].arrange(RIGHT).move_to(bits2.get_center())
        
        target_group=VGroup(*[Tex(get_label_string(bits2_sep[i].get_string())).next_to(bits2_sep[i],DOWN) for i in range(len(bits2_sep))])
        
        target=Tex(''.join([c.get_string() for c in target_group]))
        result=VGroup(
            VGroup(Tex('('),num_tex.copy(),Tex(f")_{{{str_base}}}")).arrange(RIGHT,buff=.1),
            Tex("="),
            VGroup(Tex('('),VGroup(*[Tex(c.get_string()) for c in target_group]).arrange(RIGHT,buff=.1),Tex(f")_{{{end_base}}}")).arrange(RIGHT,buff=.1)
        ).arrange(RIGHT).next_to(target_group,DOWN*2)


        table,box=get_table_and_box()
        if show_table or animate:
            self.add(table,box)
        
        if animate :
            self.play(Write(num_tex))
            self.play(TransformMatchingShapes(num_tex,num_tex_sep))
            
            for i in range(len(num_tex_sep)):
                val=get_char_value(num_tex_sep[i].get_string())
                self.play(FadeIn(bits[i]),Indicate(num_tex_sep[i]),Indicate(table[val+1][0]),Indicate(table[val+1][2]))
            self.play(FadeTransform(bits.copy(),bits2_sep))
            for i in range(len(bits2_sep)):
                val=get_char_value(target_group[i].get_string())
                self.play(FadeIn(target_group[i]),Indicate(bits2_sep[i]),Indicate(table[val+1][0]),Indicate(table[val+1][2]))
            
            self.play(TransformMatchingShapes(target_group.copy(),result[2][1]),FadeIn(VGroup(result[:2],result[2][0],result[2][2])))
            if not show_table:
                self.play(FadeOut(VGroup(box,table)))
        else:
            self.add(num_tex,num_tex_sep,bits,bits2_sep,target_group,result)





def convert_base2_to_n(num,base,animation=True,show_table=True,bg=None):
    scene = Frombase2(num,base,animate=animation,show_table=show_table,bg=bg)
    scene.run()
    if not animation:
        import os
        if not os.path.exists("images"):
            os.makedirs("images")
        scene.get_image().save(f"images/{num}-B2_to_B{base}.png")

    
def convert_base_n_to_2(num,base,animation=True,show_table=True,bg=None):
    scene = Tobase2(num,base,animate=animation,show_table=show_table,bg=bg)
    scene.run()
    if not animation:
        import os
        if not os.path.exists("images"):
            os.makedirs("images")
        scene.get_image().save(f"images/{num}-B{base}_to_B2.png")


if __name__=="__main__":

    convert_base2_to_n(100001101,8,animation=True,show_table=False)
    convert_base_n_to_2("F501",16,show_table=False)