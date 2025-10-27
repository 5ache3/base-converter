from manimlib import *
def get_char_value(c):
    d={'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,
       'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}
    
    return d[c]


def create_truth_table(headers, rows, title_text=None, position=ORIGIN):
    """
    Creates a stylized truth table as a VGroup for ManimGL scenes.

    Args:
        headers (list[str]): Column headers.
        rows (list[list[str]]): Each sublist is a row of strings.
        title_text (str): Optional title above the table.
        position (np.array): Position to move the table to.

    Returns:
        VGroup: (title, table)
    """

    # === CONFIG ===
    cell_w, cell_h = 1.2, 0.6
    font_size = 32
    header_color = BLACK
    row_fill_1 = BLACK
    row_fill_2 = BLACK

    border_color = GREY

    table = VGroup()

    # === HEADER ===
    header_group = VGroup()
    for j, h in enumerate(headers):
        rect = Rectangle(width=cell_w, height=cell_h,
                         color=border_color, fill_opacity=1, fill_color=header_color)
        text = Tex(h, color=WHITE, font_size=font_size)
        text.move_to(rect.get_center())
        cell = VGroup(rect, text).move_to(j * cell_w * RIGHT)
        header_group.add(cell)
    header_group.arrange(RIGHT, buff=0)
    table.add(header_group)

    # === ROWS ===
    for i, row in enumerate(rows):
        row_group = VGroup()
        for j, val in enumerate(row):
            rect = Rectangle(width=cell_w, height=cell_h, color=border_color,
                             fill_opacity=1, fill_color=row_fill_1 if i % 2 == 0 else row_fill_2)
            text = Tex(val, color=WHITE, font_size=font_size)
            text.move_to(rect.get_center())
            cell = VGroup(rect, text).move_to(j * cell_w * RIGHT)
            row_group.add(cell)
        row_group.arrange(RIGHT, buff=0)
        table.add(row_group)

    # === LAYOUT ===
    table.arrange(DOWN, buff=0)
    table.move_to(position)

    # === OPTIONAL TITLE ===
    title = None
    if title_text:
        title = Tex(title_text, color=YELLOW).scale(1)
        title.next_to(table, UP, buff=0.5)

    return VGroup(title, table) if title else table


def binary_to_base(num,base):
    s=0
    for i in range(len(num)):
        s += int(num[len(num)-i-1])*(2**i)
    if base== 10:
        return str(s)
    if base == 16:
        return str(hex(s))[2:].upper()
    if base == 8:
        return str(oct(s))[2:].upper()

def get_binary(num,base=10):
    if base==10:
        return str(bin(int(num)))[2:]
    
    s=0
    for i in range(len(num)):
        s+= get_char_value(num[len(num)-1-i])* (base**i)

    return str(bin(s))[2:]
    

class AND(Scene):
    def __init__(self, number1, number2, base=10, animate=False,show_table=True):
        self.number1=number1
        self.number2=number2
        self.base=base
        self.animate=animate
        self.show_table=show_table

        super().__init__(
                   file_writer_config={"write_to_movie":animate,"file_name":f"AND-{number1}-{number2}-B{base}"},
                   camera_config={"background_color":BLACK},
                   )
    def construct(self):
        base=self.base
        animate=self.animate
        num1=self.number1
        num2=self.number2
        show_table=self.show_table

        table=create_truth_table(headers=['A','B','A \land B'],rows=[['0','0','0'],['0','1','0'],['1','0','0'],['1','1','1']]).to_edge(DR+UP*1)
        indecies={'00':1,'01':2,'10':3,'11':4}
        if animate or show_table:
            self.add(table)

        bin1=get_binary(num1,base)
        bin2=get_binary(num2,base)
        
        while len(bin1)<len(bin2):
            bin1='0'+bin1
        while len(bin2)<len(bin1):
            bin2='0'+bin2

        if base !=2:
            main_tex=Tex(f'({num1})_{{{base}}} \oplus ({num2})_{{{base}}}').to_edge(UP)
            self.add(main_tex)
        len_1 = len(str(num1)+str(base))+2
        len_2 = len(str(num2)+str(base))+2


        bin1_tex=VGroup(*[Tex(c) for c in bin1]).arrange(RIGHT,buff=.1)
        bin2_tex=VGroup(*[Tex(c) for c in bin2]).arrange(RIGHT,buff=.1).next_to(bin1_tex,DOWN*2)

        if base !=2:
            equ=VGroup(
                VGroup(main_tex[:len_1].copy(),Tex('='),bin1_tex.copy()).arrange(RIGHT),
                VGroup(main_tex[-len_2:].copy(),Tex('='),bin2_tex.copy()).arrange(RIGHT),
            ).arrange(RIGHT*2).next_to(main_tex,DOWN*2).scale(.85)
            
        et_char=Text("ET").next_to(bin1_tex,LEFT+DOWN*.7).scale(.7)
        line=Line(bin2_tex.get_right()+DOWN*.45,bin2_tex.get_left()+DOWN*.45,)
        result=VGroup(*[Tex(str(int(bin1[i]) and int(bin2[i]))) for i in range(len(bin2))]).arrange(RIGHT,buff=.1).next_to(bin2_tex,DOWN*2)
        bin_result=''.join([c.get_string() for c in result])
        
        if base !=2:
            result_in_base=Tex(f'({binary_to_base(bin_result,base)})_{{{base}}}').next_to(result,DOWN*2)
        
        
        if animate:
            if base !=2:
                self.play(
                    TransformMatchingParts(main_tex[:len_1].copy(),equ[0][0]),
                    TransformMatchingParts(main_tex[-len_2:].copy(),equ[1][0]),
                    )
                self.play(FadeIn(equ[0][1:]))
                self.play(FadeIn(equ[1][1:]))
                self.play(TransformMatchingShapes(equ[0][-1].copy(),bin1_tex),TransformMatchingShapes(equ[1][-1].copy(),bin2_tex),FadeIn(et_char))
            else:
                self.play(FadeIn(bin1_tex),FadeIn(bin2_tex),FadeIn(et_char))

            self.play(Write(line))

            for i in range(len(bin1_tex))[::-1]:
                self.play(
                    Indicate(bin1_tex[i]),
                    Indicate(bin2_tex[i]),
                    FadeIn(result[i]),
                    Indicate(table[indecies[f'{bin1_tex[i].get_string()}{bin2_tex[i].get_string()}']][0][1]),
                    Indicate(table[indecies[f'{bin1_tex[i].get_string()}{bin2_tex[i].get_string()}']][1][1]),
                    Indicate(table[indecies[f'{bin1_tex[i].get_string()}{bin2_tex[i].get_string()}']][2][1]),
                    )
            if base !=2:
                self.play(Write(result_in_base))

            if not show_table:
                self.play(FadeOut(table))
            
        else:
            if base !=2:
                self.add(main_tex,equ,bin1_tex,bin2_tex,et_char,line,result,result_in_base)
            else:
                self.add(bin1_tex,bin2_tex,et_char,line,result)

            self.wait()


class OR(Scene):
    def __init__(self, number1, number2, base=10, animate=False,show_table=True):
        self.number1=number1
        self.number2=number2
        self.base=base
        self.animate=animate
        self.show_table=show_table
        
        super().__init__(
                   file_writer_config={"write_to_movie":animate,"file_name":f"OR_{number1}_{number2}_B{base}"},
                   camera_config={"background_color":BLACK},
                   )
    def construct(self):
        base=self.base
        animate=self.animate
        num1=self.number1
        num2=self.number2
        bin1=get_binary(num1,base)
        bin2=get_binary(num2,base)
        show_table=self.show_table
        table=create_truth_table(headers=['A','B','A \lor B'],rows=[['0','0','0'],['0','1','1'],['1','0','1'],['1','1','1']]).to_edge(DR+UP*1)
        indecies={'00':1,'01':2,'10':3,'11':4}
        if show_table or animate:
            self.add(table)
        while len(bin1)<len(bin2):
            bin1='0'+bin1
        while len(bin2)<len(bin1):
            bin2='0'+bin2

        if base !=2:
            main_tex=Tex(f'({num1})_{{{base}}} \oplus ({num2})_{{{base}}}').to_edge(UP)
            self.add(main_tex)
        len_1 = len(str(num1)+str(base))+2
        len_2 = len(str(num2)+str(base))+2


        bin1_tex=VGroup(*[Tex(c) for c in bin1]).arrange(RIGHT,buff=.1)
        bin2_tex=VGroup(*[Tex(c) for c in bin2]).arrange(RIGHT,buff=.1).next_to(bin1_tex,DOWN*2)

        if base !=2:
            equ=VGroup(
                VGroup(main_tex[:len_1].copy(),Tex('='),bin1_tex.copy()).arrange(RIGHT),
                VGroup(main_tex[-len_2:].copy(),Tex('='),bin2_tex.copy()).arrange(RIGHT),
            ).arrange(RIGHT*2).next_to(main_tex,DOWN*2).scale(.85)
            
        et_char=Text("OU").next_to(bin1_tex,LEFT+DOWN*.7).scale(.7)
        line=Line(bin2_tex.get_right()+DOWN*.45,bin2_tex.get_left()+DOWN*.45,)
        result=VGroup(*[Tex(str(int(bin1[i]) or int(bin2[i]))) for i in range(len(bin2))]).arrange(RIGHT,buff=.1).next_to(bin2_tex,DOWN*2)
        bin_result=''.join([c.get_string() for c in result])
        if base !=2:
            result_in_base=Tex(f'({binary_to_base(bin_result,base)})_{{{base}}}').next_to(result,DOWN*2)
        
        
        if animate:
            if base !=2:
                self.play(
                    TransformMatchingParts(main_tex[:len_1].copy(),equ[0][0]),
                    TransformMatchingParts(main_tex[-len_2:].copy(),equ[1][0]),
                    )
                self.play(FadeIn(equ[0][1:]))
                self.play(FadeIn(equ[1][1:]))
                self.play(TransformMatchingShapes(equ[0][-1].copy(),bin1_tex),TransformMatchingShapes(equ[1][-1].copy(),bin2_tex),FadeIn(et_char))
            else:
                self.play(FadeIn(bin1_tex),FadeIn(bin2_tex),FadeIn(et_char))

            self.play(Write(line))

            for i in range(len(bin1_tex))[::-1]:
                self.play(
                    Indicate(bin1_tex[i]),
                    Indicate(bin2_tex[i]),
                    FadeIn(result[i]),
                    Indicate(table[indecies[f'{bin1_tex[i].get_string()}{bin2_tex[i].get_string()}']][0][1]),
                    Indicate(table[indecies[f'{bin1_tex[i].get_string()}{bin2_tex[i].get_string()}']][1][1]),
                    Indicate(table[indecies[f'{bin1_tex[i].get_string()}{bin2_tex[i].get_string()}']][2][1]),
                    )
            if base !=2:
                self.play(Write(result_in_base))

            if not show_table:
                self.play(FadeOut(table))
            
        else:
            if base !=2:
                self.add(main_tex,equ,bin1_tex,bin2_tex,et_char,line,result,result_in_base)
            else:
                self.add(bin1_tex,bin2_tex,et_char,line,result)

            self.wait()

def xor(b1,b2):
    b1=int(b1)
    b2=int(b2)
    return str(int((b1 and not b2) or (not b1 and b2)))

from manimlib import *

def create_truth_table(headers, rows, title_text=None, position=ORIGIN):
    """
    Creates a stylized truth table as a VGroup for ManimGL scenes.

    Args:
        headers (list[str]): Column headers.
        rows (list[list[str]]): Each sublist is a row of strings.
        title_text (str): Optional title above the table.
        position (np.array): Position to move the table to.

    Returns:
        VGroup: (title, table)
    """

    # === CONFIG ===
    cell_w, cell_h = 1.2, 0.6
    font_size = 32
    header_color = BLACK
    row_fill_1 = BLACK
    row_fill_2 = BLACK

    border_color = GREY

    table = VGroup()

    # === HEADER ===
    header_group = VGroup()
    for j, h in enumerate(headers):
        rect = Rectangle(width=cell_w, height=cell_h,
                         color=border_color, fill_opacity=1, fill_color=header_color)
        text = Tex(h, color=WHITE, font_size=font_size)
        text.move_to(rect.get_center())
        cell = VGroup(rect, text).move_to(j * cell_w * RIGHT)
        header_group.add(cell)
    header_group.arrange(RIGHT, buff=0)
    table.add(header_group)

    # === ROWS ===
    for i, row in enumerate(rows):
        row_group = VGroup()
        for j, val in enumerate(row):
            rect = Rectangle(width=cell_w, height=cell_h, color=border_color,
                             fill_opacity=1, fill_color=row_fill_1 if i % 2 == 0 else row_fill_2)
            text = Tex(val, color=WHITE, font_size=font_size)
            text.move_to(rect.get_center())
            cell = VGroup(rect, text).move_to(j * cell_w * RIGHT)
            row_group.add(cell)
        row_group.arrange(RIGHT, buff=0)
        table.add(row_group)

    # === LAYOUT ===
    table.arrange(DOWN, buff=0)
    table.move_to(position)

    # === OPTIONAL TITLE ===
    title = None
    if title_text:
        title = Tex(title_text, color=YELLOW).scale(1)
        title.next_to(table, UP, buff=0.5)

    return VGroup(title, table) if title else table

class XOR(Scene):
    def __init__(self, number1, number2, base=10, animate=False,show_table=True):
        self.number1=number1
        self.number2=number2
        self.base=base
        self.animate=animate
        self.show_table=show_table
        super().__init__(
                   file_writer_config={"write_to_movie":animate,"file_name":f"XOR_{number1}_{number2}_B{base}"},
                   camera_config={"background_color":BLACK},
                   )
    def construct(self):
        base=self.base
        animate=self.animate
        num1=self.number1
        num2=self.number2
        show_table=self.show_table
        bin1=get_binary(str(num1),base)
        bin2=get_binary(str(num2),base)

        table=create_truth_table(headers=['A','B','A \oplus B'],rows=[['0','0','0'],['0','1','1'],['1','0','1'],['1','1','0']]).to_edge(DR+UP*1)
        if animate or show_table:
            self.add(table)
        indecies={'00':1,'01':2,'10':3,'11':4}
        while len(bin1)<len(bin2):
            bin1='0'+bin1
        while len(bin2)<len(bin1):
            bin2='0'+bin2
        if base !=2:
            main_tex=Tex(f'({num1})_{{{base}}} \oplus ({num2})_{{{base}}}').to_edge(UP)
            self.add(main_tex)
        len_1 = len(str(num1)+str(base))+2
        len_2 = len(str(num2)+str(base))+2


        bin1_tex=VGroup(*[Tex(c) for c in bin1]).arrange(RIGHT,buff=.1)
        bin2_tex=VGroup(*[Tex(c) for c in bin2]).arrange(RIGHT,buff=.1).next_to(bin1_tex,DOWN*2)

        if base !=2:
            equ=VGroup(
                VGroup(main_tex[:len_1].copy(),Tex('='),bin1_tex.copy()).arrange(RIGHT),
                VGroup(main_tex[-len_2:].copy(),Tex('='),bin2_tex.copy()).arrange(RIGHT),
            ).arrange(RIGHT*2).next_to(main_tex,DOWN*2).scale(.85)
            

        et_char=Text("XOR").next_to(bin1_tex,LEFT+DOWN*.7).scale(.7)
        line=Line(bin2_tex.get_right()+DOWN*.45,bin2_tex.get_left()+DOWN*.45,)
        result=VGroup(*[Tex(xor(bin1[i],bin2[i])) for i in range(len(bin2))]).arrange(RIGHT,buff=.1).next_to(bin2_tex,DOWN*2)
        bin_result=''.join([c.get_string() for c in result])
        
        if base !=2:
            result_in_base=Tex(f'({binary_to_base(bin_result,base)})_{{{base}}}').next_to(result,DOWN*2)
        
        
        if animate:
            if base !=2:
                self.play(
                    TransformMatchingParts(main_tex[:len_1].copy(),equ[0][0]),
                    TransformMatchingParts(main_tex[-len_2:].copy(),equ[1][0]),
                    )
                self.play(FadeIn(equ[0][1:]))
                self.play(FadeIn(equ[1][1:]))
                self.play(TransformMatchingShapes(equ[0][-1].copy(),bin1_tex),TransformMatchingShapes(equ[1][-1].copy(),bin2_tex),FadeIn(et_char))
            else:
                self.play(FadeIn(bin1_tex),FadeIn(bin2_tex),FadeIn(et_char))

            self.play(Write(line))

            for i in range(len(bin1_tex))[::-1]:
                self.play(
                    Indicate(bin1_tex[i]),
                    Indicate(bin2_tex[i]),
                    FadeIn(result[i]),
                    Indicate(table[indecies[f'{bin1_tex[i].get_string()}{bin2_tex[i].get_string()}']][0][1]),
                    Indicate(table[indecies[f'{bin1_tex[i].get_string()}{bin2_tex[i].get_string()}']][1][1]),
                    Indicate(table[indecies[f'{bin1_tex[i].get_string()}{bin2_tex[i].get_string()}']][2][1]),
                    )
            if base !=2:
                self.play(Write(result_in_base))

            if not show_table:
                self.play(FadeOut(table))
            
        else:
            if base !=2:
                self.add(main_tex,equ,bin1_tex,bin2_tex,et_char,line,result,result_in_base)
            else:
                self.add(bin1_tex,bin2_tex,et_char,line,result)

            self.wait()


def and_logic(num1,num2,base,animation=True,show_table=True,bg=None):
    scene = AND(num1,num2,base,animate=animation)
    scene.run()
    if not animation:
        import os
        if not os.path.exists("images"):
            os.makedirs("images")
        scene.get_image().save(f"images/AND{num1}-{num2}-B{base}.png")


def or_logic(num1,num2,base,animation=True,show_table=True,bg=None):
    scene = OR(num1,num2,base,animate=animation)
    scene.run()
    if not animation:
        import os
        if not os.path.exists("images"):
            os.makedirs("images")
        scene.get_image().save(f"images/OR{num1}-{num2}-B{base}.png")


def xor_logic(num1,num2,base,animation=True,show_table=True,bg=None):
    scene = XOR(num1,num2,base,animate=animation,show_table=show_table)
    scene.run()
    if not animation:
        import os
        if not os.path.exists("images"):
            os.makedirs("images")
        scene.get_image().save(f"images/XOR{num1}-{num2}-B{base}.png")



if __name__=='__main__':
    
    xor_logic(101101,110011,2,animation=False)
    or_logic(154,118,10,animation=True)
    and_logic(154,118,10,animation=True)