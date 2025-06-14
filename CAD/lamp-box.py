from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)
from build123d import *
import math

class StandOff(BasePartObject):
    def __init__(self, height, outer_dia, bottom_dia, inner_dia, inner_depth,
                 rotation = (0, 0, 0), align = None, mode = Mode.ADD):
        with BuildPart() as p:
            Cone(bottom_dia/2, outer_dia/2, height)
            with BuildSketch(faces().sort_by(Axis.Z)[-1]):
                Circle(inner_dia/2)
            extrude(amount=-inner_depth, mode=Mode.SUBTRACT)
        super().__init__(p.part, rotation, align, mode)

lid_inset = 2
wall_thickness = 1.2
board_width = 68
board_depth = 29
board_height = 19
board_thickness = 1.6
corner_radius=5
bottom_chamfer=2
fit = 0.2
usb_width = 59
usb_width_inner = 28.495
usb_height = 8.2 - board_thickness
usb_c_width = 9
usb_c_height = 5

def screw_x_pos(x):
    edge = (x - wall_thickness*2 - fit*2)/2
    return edge - (edge - board_width/2)/2

screw_head_len = 3
            
button_1 = (-16.258, 14.035)
button_2 = (16.192, 14.035)

class MyBox(BasePartObject):
    def __init__(self, x, y, z,
                 rotation = (0, 0, 0), align = None, mode = Mode.ADD):

        with BuildPart() as p:
            Box(x, y, z)
            fillet(edges().filter_by(Axis.Z), radius=corner_radius)
            chamfer(edges().group_by(Axis.Z)[0], length=bottom_chamfer)
            top = faces().sort_by(Axis.Z)[-1]
            with BuildSketch(top):
                offset(objects=top, amount=-wall_thickness)
            extrude(amount=-lid_inset, mode=Mode.SUBTRACT)
            inner_face = faces(Select.LAST).sort_by(Axis.Z)[0]
            mid_front = inner_face.edges().sort_by(Axis.Y)[0]@0.5
            with BuildSketch(inner_face):
                offset(inner_face, amount=0.01)
            extrude(amount=-board_height, mode=Mode.SUBTRACT)
            fillet(edges(Select.LAST).group_by(Axis.Z)[0],
                   radius=2.5)

            with Locations(faces(Select.LAST).sort_by(Axis.Z)[0].center()):
                with Locations((-29.527, 4.128, 0),
                               (28.892, 4.128, 0)):
                    StandOff(board_height-board_thickness,
                             7.5, 12.5, 3, 10,
                             align=(Align.CENTER, Align.CENTER, Align.MIN))
            
            front_face = faces().sort_by(Axis.Y)[0]
            with BuildSketch(Plane(origin=front_face.edges().sort_by(Axis.Z)[-1]@0.5,
                                   x_dir=(1, 0, 0),
                                   z_dir=(0, -1, 0))):
                with Locations((0, -(lid_inset + 8.5), 0)):
                    Rectangle(usb_width, 20,
                              align=(Align.CENTER, Align.MIN))
                with Locations((0, -(lid_inset + 17.5), 0)):
                    Rectangle(usb_c_width, 30,
                              align=(Align.CENTER, Align.MIN))
            extrude(amount=-5, mode=Mode.SUBTRACT)

            with Locations(faces().sort_by(Axis.Z)[0]):
                with Locations((-screw_x_pos(x), 0),
                               (screw_x_pos(x), 0)):
                    CounterSinkHole(3.5/2, 7/2, 10)
                with BuildSketch(faces().sort_by(Axis.Z)[0].offset(-screw_head_len)):
                    with Locations((-screw_x_pos(x), 0)):
                        RectangleRounded(7.5, 7.5, 1)
                extrude(amount=-40, mode=Mode.SUBTRACT)
                with BuildSketch(faces().sort_by(Axis.Z)[0].offset(-screw_head_len)):
                    with Locations((screw_x_pos(x), 0)):
                        RectangleRounded(7.5, 7.5, 1)
                extrude(amount=-40, mode=Mode.SUBTRACT)
                
        super().__init__(p.part, rotation, align, mode)

class TrapezoidPrism(BasePartObject):
    def __init__(self, height, base1, base2, depth, rotation = (0, 0, 0), align = None, mode = Mode.ADD):
        with BuildPart() as p:
            with BuildSketch(Plane.XZ):
                adj = (base1 - base2) / 2
                angle = math.degrees(math.atan(height / adj))
                Trapezoid(base1, height, angle)
            extrude(amount=depth)
                
        super().__init__(p.part, rotation, align, mode)

class MyLid(BasePartObject):
    def __init__(self, x, y, z, button, box_z, rotation = (0, 0, 0), align = None, mode = Mode.ADD):
        with BuildPart() as p:
            Box(x, y, z)
            fillet(edges().filter_by(Axis.Z), radius=corner_radius)
            chamfer(edges().group_by(Axis.Z)[-1], length=bottom_chamfer)
            bottom = faces().sort_by(Axis.Z)[0]
            with BuildSketch(bottom):
                offset(objects=bottom, amount=-wall_thickness-fit)
            extrude(amount=lid_inset+fit, mode=Mode.ADD)
            
            bottom = faces().sort_by(Axis.Z)[0]
            mid_front = bottom.edges().sort_by(Axis.Y)[-1]@0.5
            with BuildSketch(bottom):
                with Locations(mid_front+(0, -fit, 0)):
                    Rectangle(board_width, board_depth, align=(Align.CENTER, Align.MAX))
                #with Locations(mid_front):
                #    Rectangle(usb_width-wall_thickness*2, board_depth-2)
            extrude(amount=-4, mode=Mode.SUBTRACT)
            
            with Locations(edges().filter_by(Axis.X).group_by(Axis.Y)[0].sort_by(Axis.Z)[0]@0.5):
                Box(usb_width, wall_thickness, lid_inset + board_thickness + 0.4,
                    align=(Align.CENTER, Align.MIN, Align.MAX))
                Box(usb_width_inner, wall_thickness, lid_inset + board_thickness + 0.4 + usb_height,
                    align=(Align.CENTER, Align.MIN, Align.MAX))
                Box(usb_c_width, wall_thickness, lid_inset + board_thickness + 0.4 + 16.5 - usb_c_height,
                    align=(Align.CENTER, Align.MIN, Align.MAX))
            with Locations(edges(Select.LAST).group_by(Axis.Z)[0].sort_by(Axis.Y)[-1]@0.5 + (0, 0, board_thickness)):
                Box(usb_c_width + wall_thickness*2, wall_thickness/2, 16.5 - usb_c_height - usb_height + 0.1 - board_thickness,
                    align=(Align.CENTER, Align.MIN, Align.MIN))
            chamfer(edges(Select.LAST).group_by(Axis.Z)[-1].sort_by(Axis.Y)[0],
                    length=wall_thickness/2 - 0.01)

            # Screw mounts.
            radius = corner_radius - wall_thickness - fit
            with BuildSketch(bottom) as sk_b:
                with Locations((-screw_x_pos(x), 0)):
                    RectangleRounded((x - wall_thickness*2 - fit*2 - board_width)/2,
                                        max(y - wall_thickness*2 - fit*2, radius*2),
                                        radius)
            with BuildSketch(bottom.offset(box_z - wall_thickness * 2 - screw_head_len - fit)):
                with Locations((-screw_x_pos(x), 0)):
                    RectangleRounded(7, 7, 1)
            loft()
            with Locations(faces().group_by(Axis.Z)[0]):
                Hole(1.5, 10)
                    
            with BuildSketch(bottom) as sk_b:
                with Locations((screw_x_pos(x), 0)):
                    RectangleRounded((x - wall_thickness*2 - fit*2 - board_width)/2,
                                        max(y - wall_thickness*2 - fit*2, radius*2),
                                        radius)
            with BuildSketch(bottom.offset(box_z - wall_thickness * 2 - screw_head_len - fit)):
                with Locations((screw_x_pos(x), 0)):
                    RectangleRounded(7, 7, 1)
            loft()
            with Locations(faces().group_by(Axis.Z)[0]):
                Hole(1.5, 10)
            
            with Locations((0, 0, faces().filter_by(Plane.XY).sort_by(Axis.Z)[-1].center().Z)):
                # Move to the front of the board.
                button_height = 3.6 + wall_thickness + 1
                with Locations((0,
                                -y/2+wall_thickness + 0.5,
                                button_height / 2 - wall_thickness*2)):
                    with Locations(button_1, button_2):
                        add(button,
                            mode=Mode.SUBTRACT)
                        # Cut out the box it left in the middle.
                        Cylinder(7, 20,
                                mode=Mode.SUBTRACT)
                        # Cut out enough space at the bottom.
                        with Locations((0, 0, - button_height/2 + 2)):
                            Cylinder(13.2, 10,
                                    mode=Mode.SUBTRACT,
                                    align=(Align.CENTER, Align.CENTER, Align.MAX))


        super().__init__(p.part, rotation, align, mode)

class Button(BasePartObject):
    def __init__(self, rotation = (0, 0, 0), align = None, mode = Mode.ADD):
        switch_height = 3.25
        switch_height_from_board = 5.5
        button_dome_height = 3.6
        button_rad = 11
        button_rad2 = button_rad + wall_thickness
        button_base = 1
        with BuildPart() as p:
            with BuildSketch(Plane.XZ):
                with BuildLine():
                    Bezier((0, button_dome_height),
                           (button_rad, button_dome_height), 
                           (button_rad, 0))
                    Polyline((button_rad, 0),
                             (button_rad2, -wall_thickness),
                             (button_rad2  + button_base, -wall_thickness),
                             (button_rad2 + button_base, -wall_thickness - button_base),
                             (0, -wall_thickness - button_base),
                             (0, button_dome_height))
                make_face()
            revolve()
            with BuildSketch(faces().sort_by(Axis.Z)[0]):
                Rectangle(6.5, 6.5)
            extrude(amount=-switch_height, mode=Mode.SUBTRACT)

            chamfer(edges().group_by(Axis.Z)[0], length=0.5)
        super().__init__(p.part, rotation, align, mode)

box = MyBox(92, 32, 25)
button = Button()
lid = MyLid(92, 32, 2.75,
            button, 25)
button = Button()

show_object(box, "box")
show_object(Pos(0, 0, 20) * lid, "lid")
show_object(Pos(button_1[0], -32/2 + wall_thickness + button_1[1], 15) * button, "button1")
show_object(Pos(button_2[0], -32/2 + wall_thickness + button_2[1], 15) * button, "button2")

export_step(box, "lamp_box.step")
export_step(lid, "lamp_lid.step")
export_step(button, "lamp_button.step")
