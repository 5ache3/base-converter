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

class Frombase2(Scene):
    # def __init__(self,number,base,animate=True,bg=None,**kwargs):
    #     self.number=number
    #     self.base=base
    #     self.animate=animate
    #     super().__init__(
    #                file_writer_config={"write_to_movie":True,"file_name":f"{number}-B2_to_B{base}"},
    #                camera_config={"background_color":bg if bg else BLACK},
    #                **kwargs)


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

        base=8
        number=1111101001001
        animate=False
        show_table=False

        if animate or show_table:
            self.add(table,box)

        num_str=str(number)
        n=len(num_str)

        bits=VGroup(*[Tex(num_str[i]) for i in range(n)]).arrange(RIGHT,buff=0.1).to_edge(UP).shift(LEFT+DOWN)

        if base not in [2,4,8,16]:
            raise ValueError("Base must be one of 2,4,8,16")
        group_size={2:1,4:2,8:3,16:4}[base]

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
            VGroup(Tex("("),bits.copy(),Tex(")_{2}")).arrange(RIGHT)
            ,Tex("="),
            VGroup(Tex("("),result.copy(),Tex(f")_{{{base}}}")).arrange(RIGHT)
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
            self.play(Write(main_result))
            if not show_table:
                self.play(FadeOut(VGroup(table,box)))
            self.wait(2)
            self.play(FadeOut(VGroup(grouped_bits,labels_group,result)),main_result.animate.move_to(ORIGIN+LEFT))

            
        else:
            self.add(grouped_bits)
            self.add(labels_group)
            self.add(main_result)
            self.wait()



