from manimlib import *

def n_2_c(num):
    d={
        0:'0',
        1:'1',
        2:'2',
        3:'3',
        4:'4',
        5:'5',
        6:'6',
        7:'7',
        8:'8',
        9:'9',
        10:'A',
        11:'B',
        12:'C',
        13:'D',
        14:'E',
        15:'F',
        }
    return d[num]

def c_2_n(c):
    d={
        0:'0',
        1:'1',
        2:'2',
        3:'3',
        4:'4',
        5:'5',
        6:'6',
        7:'7',
        8:'8',
        9:'9',
        10:'A',
        11:'B',
        12:'C',
        13:'D',
        14:'E',
        15:'F',
        }
    d2={b:a for a,b in d.items()}
    return d2[c]


class TentoN(Scene):
    def __init__(self,number,base,animate=True,**kwargs):
        self.number=number
        self.base=base
        self.animate=animate
        super().__init__(
                   file_writer_config={"write_to_movie":animate,"file_name":f"{number}-B10_to_B{base}"},
                   **kwargs)
        
    def construct(self):
        up_buf=.15
        base=self.base
        number=self.number
        animate=self.animate
        
        if type(base)!=int:
            raise ValueError("base must be an integer")
        
        if base <2 or base > 16:
            raise ValueError("base mut be between 2 and 16")
        


        main_group=VGroup()
        i=0
        while number > 0:
            if i ==0:
                str_num=str(number)
                tex_num=Tex(str_num)
                v_line=Line(start=tex_num.get_top()+up_buf*UP,end=tex_num.get_bottom()+DOWN*up_buf,).shift(RIGHT*((len(str(number))/2)*.4))
            else:
                tex_num=group1[-2]
                v_line=Line(group1[-3].get_end(),group1[-3].get_end()+DOWN*.6)

            str_dev=str(base)
            devider=Tex(str_dev).next_to(v_line)

            str_val=str(int(number/base))
            val=Tex(str_val).move_to(devider.get_center()+DOWN*.6)
            
            h_line=Line(v_line.get_end(),v_line.get_end()+(max(val.get_width(),1))*RIGHT)
            str_rest=n_2_c(number%base)
            rest=Tex(str_rest).move_to(tex_num.get_bottom()+DOWN*.4)
            if i==0:
                group1=VGroup(tex_num,v_line,devider,h_line,val,rest)
            else:
                group1=VGroup(v_line,devider,h_line,val,rest)
            main_group.add(group1)

            number=int(val.get_string())
            i+=1
        if i >10:
            main_group.scale(.9)
        main_group.to_corner(UL)
        main_group.shift(RIGHT)
        frame = self.camera.frame
        target_width = main_group.get_width() * 1.1  
        scale_factor = target_width / frame.get_width()
        frame.scale(max(scale_factor,1))
        if scale_factor >1:
            frame.move_to(main_group)
        
        if animate:
            speed=1
            for grp in main_group:
                # the first element if it's the first group wich is the nuber itself (6)
                # and every other time we will repeat the first elemnt wich is the v_line (5)
                self.play(FadeIn(VGroup(grp[0],grp[-5],grp[-4],grp[-3])),run_time=1/speed)
                self.play(FadeIn(grp[-2]),run_time=1/speed)
                self.play(FadeIn(grp[-1]),run_time=1/speed)
                speed+=.8
        else:
            self.add(main_group)

        r=2 if len(main_group)>5 else 0
        arrow=Arrow(main_group[-1][-1].get_bottom()+LEFT*(r+1),main_group[r][-1].get_left()+LEFT*(r+1))
        self.add(arrow) if not animate else self.play(ShowCreation(arrow))

        result=VGroup(Tex(f"({self.number})_{{10}}"),Tex("="),VGroup(Tex("("))
                      ).arrange(RIGHT).next_to(main_group[0]).shift(RIGHT*3)
        self.add(result)
        buff=.2
        boxes=VGroup()
        for grp in main_group[::-1]:
            box=SurroundingRectangle(grp[-1])
            self.add(box)
            boxes.add(box)
            res=grp[-1].copy()
            if animate:
                self.play(res.animate.move_to(result[2].get_center()+RIGHT*buff),run_time=.3)
            else:
                res.move_to(result[2].get_center()+RIGHT*buff)
                self.add(res)
            result[-1].add(res)
            buff+=.15
        closing=Tex(f")_{{{base}}}").move_to(result[2].get_center()+RIGHT*(buff+0.15))
        result.add(closing)

        if animate:
            self.play(FadeOut(main_group),FadeOut(VGroup(arrow,boxes)))
            frame=self.frame
            self.play(result.animate.move_to(ORIGIN),frame.animate.move_to(ORIGIN))
        self.wait(2)
        # self.embed()
        
class NtoTen(Scene):
    def __init__(self,number,base,animate=True,**kwargs):
        self.number=number
        self.base=base
        self.animate=animate
        super().__init__(
                   file_writer_config={"write_to_movie":animate,"file_name":f"{number}-B10_to_B{base}"},
                   **kwargs)
        
    def construct(self):
        num=str(self.number)
        base=self.base
        animate=self.animate
        n=len(num)
        
        if type(base)!=int:
            raise ValueError("base must be an integer")
        
        if base <2 or base > 16:
            raise ValueError("base mut be between 2 and 16")


        num_group=VGroup(*[Tex(c) for c in num]).arrange(RIGHT).shift(UP*2)
        indecies=VGroup(*[Tex(f'{i}',fill_color=BLUE,fill_opacity=.5).move_to(num_group[n-i-1].get_top()+UP*.4).scale(.8) for i in range(n)])
        if animate:
            ...
            self.add(num_group)   
            self.add(indecies)  
        else:
            self.add(num_group)   
            self.add(indecies)  
        equation=VGroup()
        for i in range(n):
            equation.add(Tex(fr"{num[n-1-i]} \cdot {{{base}}}^{{{i}}}",t2c={f'{{{base}}}^{{{i}}}':BLUE}))
            if i != n-1:
                equation.add(Tex("+"))

        equation2=VGroup()
        for i in  range(n):
            equation2.add(VGroup(Tex(fr"{c_2_n(num[n-1-i])}"),Tex("\cdot"),Tex(f"{base**i}",t2c={fr'{base**i}':BLUE,})).arrange(RIGHT))
            if i != n-1:
                equation2.add(Tex("+"))

        equation3=VGroup()
        for i in  range(n):
            equation3.add(Tex(f"{c_2_n(num[n-1-i]) * (base**i)}"))
            if i != n-1:
                equation3.add(Tex("+"))

        scl = 1 if n <8 else .8
        equation.arrange(RIGHT).shift(UP).scale(scl)
        equation2.arrange(RIGHT).move_to(equation.get_center()+DOWN).scale(scl)
        equation3.arrange(RIGHT).move_to(equation2.get_center()+DOWN).scale(scl)
        somme=sum([c_2_n(num[n-1-i]) * (base**i) for i in range(n)])
        summ=Tex(f"{somme}").move_to(equation3.get_center()+DOWN)
        result=VGroup(Tex(f"({num})_{{{base}}}"),Tex("="),Tex(f"({somme})_{{10}}")).arrange(RIGHT).move_to(summ.get_center()+DOWN)
        
        frame = self.camera.frame
        target_width = equation2.get_width() * 1.1  
        scale_factor = target_width / frame.get_width()
        frame.scale(max(scale_factor,1))


        if animate:
            for i in range(n):
                self.play(
                    TransformFromCopy(num_group[n-1-i],equation[i*2][0]),
                    TransformFromCopy(indecies[i],equation[i*2][-1]),
                    FadeIn(equation[i*2][1::]),
                    )
                if i!=n-1:
                    self.add(equation[i*2+1])

            for i in range(n):
                self.play(
                    TransformFromCopy(equation[i*2][0],equation2[i*2][0]),
                    TransformFromCopy(equation[i*2][1],equation2[i*2][1]),
                    TransformFromCopy(equation[i*2][2:],equation2[i*2][2]),
                    )
                if i!=n-1:
                    self.add(equation2[i*2+1])
            
            for i in range(n):
                self.play(TransformFromCopy(equation2[i*2],equation3[i*2]))
                if i!=n-1:
                    self.add(equation3[i*2+1])
            self.play(TransformFromCopy(equation3,summ),FadeIn(result[:-1]))

            self.play(TransformMatchingStrings(summ.copy(),result[-1]))

            
        else:
            self.add(equation,equation2,equation3,summ,result) 
            self.wait(2)


def convert_base10_to_n(num,base,animation=True):
    scene = TentoN(num,base,animate=animation)
    scene.run()
    if not animation:
        import os
        if not os.path.exists("images"):
            os.makedirs("images")
        scene.get_image().save(f"images/{num}-B10_to_B{base}.png")
    
def convert_n_to_base10(num,base,animation=True):
    scene = NtoTen(num,base,animate=animation)
    scene.run()
    if not animation:
        import os
        if not os.path.exists("images"):
            os.makedirs("images")
        scene.get_image().save(f"images/{num}-B{base}_to_B10.png")


if __name__ == "__main__":
    convert_base10_to_n(255091,'7',animation=False)