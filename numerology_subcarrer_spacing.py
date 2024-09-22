from manim import *
import random

abel_watermark = Text("By Abel Chacko", font_size=12).to_edge(DL)
class symbol_to_numerology(Scene):
     def construct(self):
        max_subframes= 64.0
        rect_size=1
        numerologies = list(range(0,7))
        groups = []
        braces = []
        for num in numerologies:
            num = num + 1
            rects = []
            for i in range(10):
                rects.append(RoundedRectangle(corner_radius=.1/num, width=rect_size/num, height=1.0, grid_xstep=rect_size/num, grid_ystep=1.0,fill_color=GREEN,fill_opacity=1) )
            group = Group(*rects).arrange(buff=.1+((num-1)*.002))
            group.to_edge(LEFT)
            braces.append(BraceLabel(group, f"1 slot = 14 symbols = {.25/2**num} ms", font_size=28-num))
            groups.append(group)
       
        self.add(groups[0])
        self.add(braces[0])
        self.add(abel_watermark)
        for i in numerologies[:-1]:
            self.play(ReplacementTransform(groups[i], groups[i+1]), ReplacementTransform(braces[i], braces[i+1]))
            self.wait(1)


class SubFrameToNumerology(Scene):
    def construct(self):
        max_subframes= 64.0
        rect_size=8
        numerologies = list(range(0,7))
        rects = [Rectangle(width=rect_size, height=1.0, grid_xstep=rect_size/max_subframes*2**(max(numerologies)-i), grid_ystep=1.0,fill_color=PURPLE,fill_opacity=1) for i in numerologies]
       
        for i in numerologies:
            rects[i].to_edge(LEFT)

        braces = [BraceLabel(rects[i], f"1\,subframe = {2 ** i}\,slots = 1\,ms") for i in numerologies]
        print(braces)
        #self.add(abel_watermark)
        self.add(rects[0])
        self.add(braces[0])
        for i in numerologies[:-1]:

            self.play(ReplacementTransform(rects[i], rects[i+1]), ReplacementTransform(braces[i], braces[i+1]))
            self.wait(1)

        self.wait()

class radio_frame(Scene):
     def construct(self):
        max_subframes= 64.0
        rect_size=1
        numerologies = list(range(0,7))
        rects = []
        for i in range(10):
            rects.append(RoundedRectangle(corner_radius=.1, width=rect_size, height=1.0, grid_xstep=rect_size, grid_ystep=1.0,fill_color=YELLOW,fill_opacity=1) )
        
        rects_group = Group(*rects).arrange(buff=.1)
        rects_group.to_edge(LEFT)
        brace = BraceLabel(rects_group, f"1 frame = 10 subframes = 10 ms") 
        self.add(brace)
        #self.add(abel_watermark)
        self.add(rects_group)   
        self.wait()

class LineGraphAxis(object):
    def __init__(self, x_max, y_max, step):
        self._x_max = ValueTracker(x_max)
        self._y_max = y_max
        self.step = step
        self.ax = self.make_graph()

    @property
    def x_max(self):
        return self._x_max.get_value()

    def make_axis(self):
        y_axis_config = {
            #"numbers_to_include": [12/15.0*2],
            "include_numbers": False
            }
        x_axis_config = {
            #"numbers_to_include": [12/15.0*2],
            "include_numbers": False
            #"numbers_to_include": [self._x_max.get_value()/2],
            }
        return Axes(
            x_range=[0, self._x_max.get_value(), self.step],
            y_range=[0, self._y_max, 1], x_axis_config=x_axis_config, y_axis_config=y_axis_config

        )

    def make_graph(self):
        ax = self.make_axis()

        def become_ax(mob):
            old_ax = mob
            new_ax = self.make_axis()
            old_ax.become(new_ax)

            # Copy additional properties that are not
            # copied with .become()
            old_ax.x_axis.x_range = new_ax.x_axis.x_range
            old_ax.x_axis.scaling = new_ax.x_axis.scaling
            old_ax.y_axis.x_range = new_ax.y_axis.x_range
            old_ax.y_axis.scaling = new_ax.y_axis.scaling

        ax.add_updater(become_ax)
        return ax

    def update_x_max(self, x_max):
        #self._x_max.set_value(x_max)
        return self._x_max.animate.set_value(x_max)



class SubCarrierSpacingToNumerology(Scene):
    def construct(self):
        numerologiesTracker = ValueTracker(0)
        max_subframes= 64.0
        rect_size=10
        max_numerology = 7
        numerologies = list(range(0,max_numerology))
        axes = LineGraphAxis(12/15.0, 3, 1/(15.0))
        colors = [BLUE, GREEN, GOLD, YELLOW, RED, MAROON, PURPLE]
        old_graphs = []
        old_lines = []
        old_dots = []
        title = Text("Resource Block Bandwidth", font_size=30).to_edge(UP)
        self.add(title)
        # values_x = [
        #         (12/15.0*2**0/2, str(15*2**0) + "KHz"),  # (position 3.5, label "3.5")
        #         (12/15.0*2**1/2, str(15*2**1) + "KHz"),  # (position 4.5, label "9/2")
        #         (12/15.0*2**2/2, str(15*2**2) + "KHz"),  # (position 4.5, label "9/2")
        #         (12/15.0*2**3/2, str(15*2**3) + "KHz"),  # (position 4.5, label "9/2")
        #         (12/15.0*2**4/2, str(15*2**4) + "KHz"),  # (position 4.5, label "9/2")
        #         (12/15.0*2**5/2, str(15*2**5) + "KHz"),  # (position 4.5, label "9/2")
        #         (12/15.0*2**6/2, str(15*2**6) + "KHz"),  # (position 4.5, label "9/2")
        #         (12/15.0*2**7/2, str(15*2**7) + "KHz"),  # (position 4.5, label "9/2")
        #     ]
        
        # axes.ax.x_axis_labels = VGroup()  # Create a group named x_axis_labels
        # axis = axes.ax
        # #   pos.   tex.
        # for x_val, x_tex in values_x:
        #     tex = Tex(x_tex)  # Convert string to tex
        #     #tex.set_color(axis.label_nums_color)
        #     #tex.scale(axis.x_label_font_size)
        #     tex.next_to(axis.coords_to_point(x_val, 0), DOWN)  # Put tex on the position
        #     axes.ax.x_axis_labels.add(tex)  # Add tex in graph

        self.add(abel_watermark)
        for i in numerologies:
            axes_transform = None
            if i != 0:
                axes.step = 1/(15.0) * 2 ** i
                axes_transform = axes.update_x_max(12/15.0*2**i)
            else:
                axes_transform = Write(axes.ax)

  

            graph_transforms = []
            new_graphs = []
            new_lines = []
            new_dots = []
            temp_axes = LineGraphAxis(12/15.0*2**i, 3, 1/(15.0))
            for j in numerologies[:i+1]:
                print(i)
                new_graphs.append(temp_axes.ax.plot(lambda x: abs(np.sin(2*np.pi*15*x/(2**j))/((i-j+1))), x_range=[0, 12/15.0/2.0*(2**j),0.001*2**i], use_smoothing=True, color=colors[j]))
                
                point = temp_axes.ax.c2p(12/15.0*2**j/2, 1/((i-j+1)))
                dot = Dot(point)
                new_dots.append(dot)
                khz = 15*2**j * 12
                cur_line = temp_axes.ax.get_horizontal_line(point, line_func=Line)
                new_lines.append(LabeledLine(label=str(khz)+" KHz",start=cur_line.start,end=cur_line.end ))

            for j in range(0,i):
                graph_transforms.append(ReplacementTransform(old_graphs[j], new_graphs[j]))
                graph_transforms.append(ReplacementTransform(old_lines[j], new_lines[j]))
                graph_transforms.append(ReplacementTransform(old_dots[j], new_dots[j]))

            axes.coordinate_labels = VGroup()
            self.play(axes_transform, *graph_transforms)
 
            self.play(Write(new_graphs[-1]))
            self.play(Write(new_lines[-1]))
            self.play(Write(new_dots[-1]))

            
            old_graphs = new_graphs
            old_lines = new_lines
            old_dots = new_dots
        self.wait()

class ResourceGrid(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=.5,
            zoomed_display_width=1/10*3*6*4,
            zoomed_display_height=20/200*8*4,
            image_frame_stroke_width=1,
            zoomed_camera_config={
                "default_frame_stroke_width": 0,
                #"frame_height": 20/200*8*4,
                #"frame_width": 1/10*3*6*4*4
            },
            **kwargs
        )


    def construct(self):
        kwargs = {"fill_opacity": 1, "stroke_color": BLACK}
        number_plane = NumberPlane(
            x_range=(0, 10, 1),
            y_range=(0,20*10, 1),
            x_length=3,
            y_length=6,
        ).to_edge(LEFT)
        abel_watermark = Text("By Abel Chacko", font_size=12).to_edge(DL)

        temp_numbplane=NumberPlane(x_range=(0, 10, 1),y_range=(0,20*10, 1),x_length=3,y_length=6,background_line_style={
                "stroke_width": .01,
            }).to_edge(LEFT)
        pss_point = temp_numbplane.c2p(0.5, 50)
        pbch_1_point = temp_numbplane.c2p(1.5, 50)
        pbch_2_1_point = temp_numbplane.c2p(2.5, 60-2)
        sss_point = temp_numbplane.c2p(2.5, 50)
        pbch_2_2_point = temp_numbplane.c2p(2.5, 40+2)
        pbch_3_point = temp_numbplane.c2p(3.5, 50)

        pss_rect = Rectangle(width=.93/10*3, height=10.5/200*6,fill_color=GREEN,fill_opacity=1, stroke_width=0)
        pbch_1_rect = Rectangle(width=.93/10*3, height=20/200*6,fill_color=RED,fill_opacity=1, stroke_width=0)
        pbch_2_1_rect = Rectangle(width=.93/10*3, height=4/200*6,fill_color=RED,fill_opacity=1, stroke_width=0)
        sss_rect = Rectangle(width=.93/10*3, height=10.5/200*6,fill_color=PURPLE,fill_opacity=1, stroke_width=0)
        pbch_2_2_rect = Rectangle(width=.93/10*3, height=4/200*6,fill_color=RED,fill_opacity=1, stroke_width=0)
        pbch_3_rect = Rectangle(width=.93/10*3, height=20/200*6,fill_color=RED,fill_opacity=1, stroke_width=0)


        pss_rect.move_to(pss_point)
        pbch_1_rect.move_to(pbch_1_point)
        pbch_2_1_rect.move_to(pbch_2_1_point)
        sss_rect.move_to(sss_point)
        pbch_2_2_rect.move_to(pbch_2_2_point)
        pbch_3_rect.move_to(pbch_3_point)

        y_label = temp_numbplane.get_y_axis_label(Text("Resource Blocks").scale(0.45).rotate(PI/2), edge=LEFT, direction=LEFT, buff=0.4)
        x_label = temp_numbplane.get_x_axis_label(Tex("OFDM Symbols").scale(0.45), edge=DOWN, direction=DOWN, buff=.1)


        pss_text = Text("P\nS\nS",font_size=6).move_to(pss_rect.get_center()) # create text
        pbch_1_text = Text("P\nB\nC\nH\n",font_size=6).move_to(pbch_1_rect.get_center()) # create text
        pbch_2_1_text = Text("PBCH",font_size=3).move_to(pbch_2_1_rect.get_center()) # create text
        sss_text = Text("S\nS\nS",font_size=6).move_to(sss_rect.get_center())
        pbch_2_2_text = Text("PBCH",font_size=3).move_to(pbch_2_2_rect.get_center()) # create text
        pbch_3_text = Text("P\nB\nC\nH\n",font_size=6).move_to(pbch_3_rect.get_center()) # create text


        self.add(abel_watermark)
        self.play(Write(number_plane),Write(pss_rect),Write(pbch_1_rect),Write(pbch_2_1_rect),
            Write(sss_rect),Write(pbch_2_2_rect),Write(pbch_3_rect),Write(y_label),Write(x_label),
            Write(pss_text), Write(pbch_1_text), Write(pbch_2_1_text), Write(pbch_2_2_text), Write(sss_text), Write(pbch_3_text))

        gscn_num = 0
        gscn_search_point = temp_numbplane.c2p(2, 50-5*8+8*gscn_num)
        gscn_search_rect = DashedVMobject(Rectangle(width=1/10*3*4, height=20/200*6,fill_opacity=0, stroke_width=1),  num_dashes=20, stroke_color=YELLOW_C)
        gscn_search_rect.move_to(gscn_search_point)
        self.zoomed_camera.frame.move_to(gscn_search_point)
        brace = BraceLabel(self.zoomed_display, "GSCN Search")

        self.play(Write(gscn_search_rect))
        self.activate_zooming(animate=False)
        self.add(brace)
        gscn_search_rect_lock = None
        prev_rect = gscn_search_rect
        max_steps = 23
        for gscn_num in range(1,max_steps):
            gscn_search_point = temp_numbplane.c2p(2, 50-5*8+8*gscn_num)
            gscn_search_rect = DashedVMobject(Rectangle(width=1/10*3*4, height=20/200*6,fill_opacity=0, stroke_width=1),  num_dashes=20, stroke_color=YELLOW_C)
            gscn_search_rect.move_to(gscn_search_point)
            self.play(ReplacementTransform(prev_rect, gscn_search_rect),self.zoomed_camera.frame.animate.move_to(gscn_search_point))
            
            if gscn_num == 5:
                gscn_search_rect_lock = DashedVMobject(Rectangle(width=1/10*3*4, height=20/200*6,fill_opacity=0, stroke_width=4, stroke_color=PURE_RED),  num_dashes=20, color=PURE_RED) 
                gscn_search_rect_lock.move_to(gscn_search_point)
                self.add(gscn_search_rect_lock)

            if gscn_num >= 5:
                radius = 20/200
                self.play(ShowPassingFlash(
                gscn_search_rect_lock.copy().set_color(BLUE),
                run_time=2,
                time_width=1))

            prev_rect = gscn_search_rect

class TradRanToOran(Scene):

    def construct(self):
        trad_ran_text = Text("Tradition RAN")
        oran_text = Text("ORAN")
        trad_ran_text.to_edge(UP)
        oran_text.to_edge(UP)
        abel_watermark = Text("By Abel Chacko", font_size=12).to_edge(DL)

        scale=1.5
        bbu_rect = Rectangle(width=2*scale, height=1*scale, fill_opacity=1, fill_color=GREEN)
        radio_head = Rectangle(width=1*scale, height=1*scale, fill_opacity=1, fill_color=RED)
        core_rect = Rectangle(width=1*scale, height=1*scale, fill_opacity=1, fill_color=PURPLE)
        ue_rect = Rectangle(width=1*scale, height=1*scale, fill_opacity=1, fill_color=LOGO_GREEN)
        
        radio_head.shift(UP + UP + LEFT*scale*2)
        core_rect.shift(RIGHT + RIGHT * 2 *scale)
        ue_rect.shift(UP + UP + LEFT*scale*2 + LEFT*3)

        bbu_text = Text("BBU", font_size=12*scale).move_to(bbu_rect.get_center())
        core_text = Text("Core", font_size=12*scale).move_to(core_rect.get_center())
        rh_text = Text("Radio Head", font_size=12*scale).move_to(radio_head.get_center())

        rh_bbu_1 = Line(radio_head.get_bottom(), bbu_rect.get_left() + LEFT*scale)
        rh_bbu_2 = Line(bbu_rect.get_left() + LEFT*scale, bbu_rect.get_left())
        bbu_core = Line(bbu_rect.get_right(), core_rect.get_left())
        arc_1 = Arc(radius=.25, start_angle=PI*2/3, angle=PI*2/3, arc_center=radio_head.get_left()+LEFT*.25, color=WHITE)
        arc_2 = Arc(radius=.5, start_angle=PI*2/3, angle=PI*2/3, arc_center=radio_head.get_left()+LEFT*.25, color=WHITE)
        arc_3 = Arc(radius=.75, start_angle=PI*2/3, angle=PI*2/3, arc_center=radio_head.get_left()+LEFT*.25, color=WHITE)

        ric_rect = Rectangle(width=3*scale, height=1*scale, fill_opacity=1, fill_color=GREEN)
        cu_rect = Rectangle(width=1*scale, height=1*scale, fill_opacity=1, fill_color=DARK_BLUE)
        du_rect = Rectangle(width=1*scale, height=1*scale, fill_opacity=1, fill_color=BLUE)


        du_rect.shift(LEFT*scale)
        cu_rect.shift(RIGHT*scale)
        ric_rect.shift(DOWN*2*scale)

        cu_text = Text("CU", font_size=12*scale).move_to(cu_rect.get_center())
        du_text = Text("DU", font_size=12*scale).move_to(du_rect.get_center())
        ric_text = Text("RIC", font_size=12*scale).move_to(ric_rect.get_center())
        ue_text = Text("UE", font_size=12*scale).move_to(ue_rect.get_center())

        
        rh_du_1 = Line(radio_head.get_bottom(), du_rect.get_left() + LEFT*scale*.5)
        rh_du_2 = LabeledLine(start=du_rect.get_left() + LEFT * scale/2, end=du_rect.get_left(), label="7.2x", font_size=12)
        du_cu = Line(du_rect.get_right(), cu_rect.get_left())
        cu_core = Line(cu_rect.get_right(), core_rect.get_left())
        cu_ric = Line(cu_rect.get_bottom(), ric_rect.get_top()+RIGHT*scale)
        du_ric = Line(du_rect.get_bottom(), ric_rect.get_top()+LEFT*scale)
        self.add(abel_watermark)
        self.play(Write(trad_ran_text))
        self.play(Write(bbu_rect), Write(radio_head),Write(core_rect), Write(rh_bbu_1), Write(rh_bbu_2), Write(bbu_core), Write(ue_rect),
            Write(arc_1), Write(arc_2), Write(arc_3))
        self.play(Write(bbu_text),Write(rh_text), Write(core_text), Write(ue_text))
        self.wait(2)

        self.play(ReplacementTransform(trad_ran_text,oran_text), 
            FadeOut(bbu_rect, scale=0.5),FadeOut(bbu_text, scale=0.5),
            FadeOut(rh_bbu_1), FadeOut(rh_bbu_2), FadeOut(bbu_core),
            Write(cu_rect), Write(du_rect), Write(cu_text), Write(du_text), Write(ric_rect), Write(ric_text),
            Write(rh_du_1),Write(rh_du_2),Write(du_cu),Write(cu_core), Write(du_ric), Write(cu_ric)
            )
        self.wait(2)



class OFDM_Intution(ThreeDScene):
    def construct(self):
        symbols = 14
        time = 12
        axes = ThreeDAxes(x_range=[0,time+1], y_range=[0,symbols+1], z_range=[0, 5])
        #RIGHT * 1.8
        x_label = axes.get_x_axis_label(Tex("Time")).shift(-5*RIGHT+DOWN*2).rotate(angle=-PI, axis=np.array([1., 0., 0])).rotate(angle=PI, axis=np.array([0, 1., 0]))
        x_label.rotate(angle=-PI/2, axis=np.array([1, 0., 0])).shift([0,0,1])
        global abel_watermark
        abel_watermark = abel_watermark.shift([10,0,3])
        abel_watermark.rotate(angle=PI/2, axis=np.array([1, 0., 0])).rotate(angle=PI, axis=[0,0,1])
        y_label = axes.get_y_axis_label(Tex("Frequency")).shift(LEFT * 1.8 + DOWN*3+[0,0,1]).shift([0,0,1]).rotate(angle=PI/2, axis=np.array([0, 1., 0]))
        # zoom out so we see the axes
        self.set_camera_orientation(zoom=0.5)
        self.wait(0.5)

        # animate the move of the camera to properly see the axes
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)
        self.add(abel_watermark)
        self.play(FadeIn(axes), FadeIn(x_label), FadeIn(y_label))
        
        # built-in updater which begins camera rotation
        self.begin_ambient_camera_rotation(rate=0.15)

        self.wait(2)

        new_graphs = []
        colors = [BLUE, GREEN, GOLD, YELLOW, RED, MAROON, PURPLE]
        amplitudes = [i * 1/8 for i in range(8)]
        random.seed(12312)
        for i in range(time):
            for j in range(symbols):
                #graph = ParametricFunction(lambda x: (0, j, np.sin(PI*x)), t_range=[0, 1,0.001*2], use_smoothing=True, color=colors[j], use_vectorized=True)
                amp = random.choice(amplitudes)
                graph = axes.plot_parametric_curve(lambda x: (i, j+x, amp * np.sin(PI*.8*x)), t_range=[0, PI/(PI*.8),0.01*2], use_smoothing=True, color=colors[j%len(colors)]).set_fill(colors[j%len(colors)],opacity=1)
                self.add(graph)     
            self.wait(.1)
        self.wait()   

class Tdd_patterns(Scene):
    def construct(self):
        max_symbols = 14
        rect_size=.5
        rects = []
        all_tdd_patterns = [["D","D","D","D","D","D","D","D","D","D","D","D","D","D"],
        ["U","U","U","U","U","U","U","U","U","U","U","U","U","U"],
        ["F","F","F","F","F","F","F","F","F","F","F","F","F","F"],
        ["D","D","D","D","D","D","D","D","D","D","D","D","D","F"],
        ["D","D","D","D","D","D","D","D","D","D","D","D","F","F"],
        ["D","D","D","D","D","D","D","D","D","D","D","F","F","F"],
        ["D","D","D","D","D","D","D","D","D","D","F","F","F","F"],
        ["D","D","D","D","D","D","D","D","D","F","F","F","F","F"],
        ["F","F","F","F","F","F","F","F","F","F","F","F","F","U"],
        ["F","F","F","F","F","F","F","F","F","F","F","F","U","U"],
        ["F","U","U","U","U","U","U","U","U","U","U","U","U","U"],
        ["F","F","U","U","U","U","U","U","U","U","U","U","U","U"],
        ["F","F","F","U","U","U","U","U","U","U","U","U","U","U"],
        ["F","F","F","F","U","U","U","U","U","U","U","U","U","U"],
        ["F","F","F","F","F","U","U","U","U","U","U","U","U","U"],
        ["F","F","F","F","F","F","U","U","U","U","U","U","U","U"],
        ["D","F","F","F","F","F","F","F","F","F","F","F","F","F"],
        ["D","D","F","F","F","F","F","F","F","F","F","F","F","F"],
        ["D","D","D","F","F","F","F","F","F","F","F","F","F","F"],
        ["D","F","F","F","F","F","F","F","F","F","F","F","F","U"],
        ["D","D","F","F","F","F","F","F","F","F","F","F","F","U"],
        ["D","D","D","F","F","F","F","F","F","F","F","F","F","U"],
        ["D","F","F","F","F","F","F","F","F","F","F","F","U","U"],
        ["D","D","F","F","F","F","F","F","F","F","F","F","U","U"],
        ["D","D","D","F","F","F","F","F","F","F","F","F","U","U"],
        ["D","F","F","F","F","F","F","F","F","F","F","U","U","U"],
        ["D","D","F","F","F","F","F","F","F","F","F","U","U","U"],
        ["D","D","D","F","F","F","F","F","F","F","F","U","U","U"],
        ["D","D","D","D","D","D","D","D","D","D","D","D","F","U"],
        ["D","D","D","D","D","D","D","D","D","D","D","F","F","U"],
        ["D","D","D","D","D","D","D","D","D","D","F","F","F","U"],
        ["D","D","D","D","D","D","D","D","D","D","D","F","U","U"],
        ["D","D","D","D","D","D","D","D","D","D","F","F","U","U"],
        ["D","D","D","D","D","D","D","D","D","F","F","F","U","U"],
        ["D","F","U","U","U","U","U","U","U","U","U","U","U","U"],
        ["D","D","F","U","U","U","U","U","U","U","U","U","U","U"],
        ["D","D","D","F","U","U","U","U","U","U","U","U","U","U"],
        ["D","F","F","U","U","U","U","U","U","U","U","U","U","U"],
        ["D","D","F","F","U","U","U","U","U","U","U","U","U","U"],
        ["D","D","D","F","F","U","U","U","U","U","U","U","U","U"],
        ["D","F","F","F","U","U","U","U","U","U","U","U","U","U"],
        ["D","D","F","F","F","U","U","U","U","U","U","U","U","U"],
        ["D","D","D","F","F","F","U","U","U","U","U","U","U","U"],
        ["D","D","D","D","D","D","D","D","D","F","F","F","F","U"],
        ["D","D","D","D","D","D","F","F","F","F","F","F","U","U"],
        ["D","D","D","D","D","D","F","F","U","U","U","U","U","U"],
        ["D","D","D","D","D","F","U","D","D","D","D","D","F","U"],
        ["D","D","F","U","U","U","U","D","D","F","U","U","U","U"],
        ["D","F","U","U","U","U","U","D","F","U","U","U","U","U"],
        ["D","D","D","D","F","F","U","D","D","D","D","F","F","U"],
        ["D","D","F","F","U","U","U","D","D","F","F","U","U","U"],
        ["D","F","F","U","U","U","U","D","F","F","U","U","U","U"],
        ["D","F","F","F","F","F","U","D","F","F","F","F","F","U"],
        ["D","D","F","F","F","F","U","D","D","F","F","F","F","U"],
        ["F","F","F","F","F","F","F","D","D","D","D","D","D","D"],
        ["D","D","F","F","F","U","U","U","D","D","D","D","D","D"]]
        for i in range(max_symbols):
            rects.append(RoundedRectangle(corner_radius=.1, width=rect_size, height=1.0, grid_xstep=rect_size, grid_ystep=1.0))
        
        rects_group = Group(*rects).arrange(buff=.1)
        self.add(rects_group,abel_watermark) 
        self.wait()
        old_pat = None
        old_pat_mobject = None
        for index, pat in enumerate(all_tdd_patterns):
            new_pat_mobject = []
            new_pat_transform = []
            for rect_index, rect in enumerate(rects_group):
                cur_symbol = pat[rect_index]
                cur_arrow = None
                text = None
                if cur_symbol == "D":
                    cur_arrow = Arrow(end=rect.get_bottom(), start=rect.get_top(), color=RED)
                elif cur_symbol == "U":
                    cur_arrow = Arrow(start=rect.get_bottom(), end=rect.get_top(), color=BLUE)
                elif cur_symbol == "F":

                    arrow = Arrow(start=rect.get_bottom() - [.15,0,0], end=rect.get_top() - [.15,0,0], color=BLUE)
                    arrow1 = Arrow(start=rect.get_top() + [.15,0,0], end=rect.get_bottom() + [.15,0,0], color=RED)
                    slash_text = Text("/", font_size=15).move_to(rect.get_center())
                    cur_arrow = Group(arrow, slash_text , arrow1)

                new_pat_mobject.append(cur_arrow)

                if index > 0:
                    new_pat_transform.append(FadeOut(old_pat_mobject[rect_index]))
                    new_pat_transform.append(FadeIn(new_pat_mobject[rect_index]))

            if index > 0:
                self.play(*new_pat_transform)
            else:
                self.add(*new_pat_mobject)

            old_pat_mobject = new_pat_mobject

             
            self.wait(.05)
        self.wait()



class AirInterfaceZoom(MovingCameraScene):

    def construct(self):
        trad_ran_text = Text("Tradition RAN")
        oran_text = Text("ORAN")
        trad_ran_text.to_edge(UP)
        oran_text.to_edge(UP)

        scale=1.5
        radio_head = Rectangle(width=1*scale, height=1*scale, fill_opacity=1, fill_color=RED)
        core_rect = Rectangle(width=1*scale, height=1*scale, fill_opacity=1, fill_color=PURPLE)
        ue_rect = Rectangle(width=1*scale, height=1*scale, fill_opacity=1, fill_color=LOGO_GREEN)
        
        radio_head.shift(UP + UP + LEFT*scale*2)
        core_rect.shift(RIGHT + RIGHT * 2 *scale)
        ue_rect.shift(UP + UP + LEFT*scale*2 + LEFT*3)

        core_text = Text("Core", font_size=12*scale).move_to(core_rect.get_center())
        rh_text = Text("Radio Head", font_size=12*scale).move_to(radio_head.get_center())

        arc_1 = Arc(radius=.25, start_angle=PI*2/3, angle=PI*2/3, arc_center=radio_head.get_left()+LEFT*.25, color=WHITE)
        arc_2 = Arc(radius=.5, start_angle=PI*2/3, angle=PI*2/3, arc_center=radio_head.get_left()+LEFT*.25, color=WHITE)
        arc_3 = Arc(radius=.75, start_angle=PI*2/3, angle=PI*2/3, arc_center=radio_head.get_left()+LEFT*.25, color=WHITE)

        ric_rect = Rectangle(width=3*scale, height=1*scale, fill_opacity=1, fill_color=GREEN)
        cu_rect = Rectangle(width=1*scale, height=1*scale, fill_opacity=1, fill_color=DARK_BLUE)
        du_rect = Rectangle(width=1*scale, height=1*scale, fill_opacity=1, fill_color=BLUE)


        du_rect.shift(LEFT*scale)
        cu_rect.shift(RIGHT*scale)
        ric_rect.shift(DOWN*2*scale)

        cu_text = Text("CU", font_size=12*scale).move_to(cu_rect.get_center())
        du_text = Text("DU", font_size=12*scale).move_to(du_rect.get_center())
        ric_text = Text("RIC", font_size=12*scale).move_to(ric_rect.get_center())
        ue_text = Text("UE", font_size=12*scale).move_to(ue_rect.get_center())

        
        rh_du_1 = Line(radio_head.get_bottom(), du_rect.get_left() + LEFT*scale*.5)
        rh_du_2 = LabeledLine(start=du_rect.get_left() + LEFT * scale/2, end=du_rect.get_left(), label="7.2x", font_size=12)
        du_cu = Line(du_rect.get_right(), cu_rect.get_left())
        cu_core = Line(cu_rect.get_right(), core_rect.get_left())
        cu_ric = Line(cu_rect.get_bottom(), ric_rect.get_top()+RIGHT*scale)
        du_ric = Line(du_rect.get_bottom(), ric_rect.get_top()+LEFT*scale)

        all_mobjects = Group(radio_head,core_rect,ue_rect,rh_text,core_text,ue_text,
            arc_1,arc_2,arc_3,ric_rect,cu_rect,du_rect,cu_text,du_text,ric_text,rh_du_1,rh_du_2,du_cu,cu_core,cu_ric,du_ric)
        self.add(all_mobjects,abel_watermark)
        self.wait()
        self.camera.frame.save_state()
        # Animation of the camera
        self.play(self.camera.frame.animate.move_to(radio_head.get_center()+DOWN+RIGHT).set(width=3,height=4))

        self.wait()
        
