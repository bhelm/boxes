#!/usr/bin/env python3
# Copyright (C) 2013-2014 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *
import math


class FlexBox5(Boxes):
    """Box with living hinge and clicking lock"""

    ui_group = "FlexBox"

    def __init__(self):
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings, surroundingspaces=1)
        self.addSettingsArgs(edges.FlexSettings)
        self.buildArgParser("x", "y", "outside")
        self.argparser.add_argument(
            "--z", action="store", type=float, default=100.0,
            help="height of the box")
        self.argparser.add_argument(
            "--h", action="store", type=float, default=10.0,
            help="height of the lid")
        self.argparser.add_argument(
            "--radius", action="store", type=float, default=10.0,
            help="radius of the lids living hinge")
        self.argparser.add_argument(
            "--c", action="store", type=float, default=9.0,
            dest="d", help="clearance of the lid")

    def flexBoxSide(self, x, y, r, callback=None, move=None):
        t = self.thickness
        if self.move(x+2*t, y+t, move, True):
            return

        self.moveTo(t, t)
        self.cc(callback, 0)
        self.edges["f"](x)
        self.corner(90, 0)
        self.cc(callback, 1)
        self.edges["f"](y - r)
        self.corner(90, r)
        self.cc(callback, 2)
        self.edge(x - r)
        self.corner(90, 0)
        self.cc(callback, 3)
        self.edges["f"](y)
        self.corner(90)

        self.move(x+2*t, y+t, move)

    def surroundingWall(self, move=None):
        x, y, z, r, d = self.x, self.y, self.z, self.radius, self.d
        t = self.thickness

        tw = x + y - 2*r + self.c4 + 2*t + d
        th = z + 2*t

        if self.move(tw, th, move, True):
            return

        self.moveTo(t, 0)

        self.edges["F"](y - r, False)
        #living hinge
        self.edges["X"](self.c4, z + 2 * t)

        self.edges["e"](x - r + d)
        self.corner(90, t)

        #front endge
        self.edges["B"](z)
        self.corner(90, t)

        self.edges["e"](x - r + d)
        #living hinge other side
        self.edge(self.c4)
        self.edges["F"](y - r)
        self.corner(90)
        self.edge(t)
        self.edges["f"](z)
        self.edge(t)
        self.corner(90)

        self.move(tw, th, move)

    def lidSide(self, move=None):
        x, y, z, r, d, h = self.x, self.y, self.z, self.radius, self.d, self.h
        t = self.thickness
        r2 = r + t if r + t <= h + t else h + t

        if r < h:
            r2 = r + t
            base_l = x + 2 * t
            if self.move(h+t, base_l+t, move, True):
                return

            self.edge(h + self.thickness - r2)
            self.corner(90, r2)
            self.edge(r - r2 + 2 * t)
        else:
            a = math.acos((r-h)/(r+t))
            ang = math.degrees(a)
            base_l = x + (r+t) * math.sin(a) - r
            if self.move(h+t, base_l+t, move, True):
                return

            self.corner(90-ang)
            self.corner(ang, r+t)

        self.edges["F"](x - r)
        self.edgeCorner("F", "f")
        self.edges["g"](h)
        self.edgeCorner("f", "e")
        self.edge(base_l)
        self.corner(90)

        self.move(h+t, base_l+t, move)

    def render(self):
        if self.outside:
            self.x = self.adjustSize(self.x)
            self.y = self.adjustSize(self.y)
            self.z = self.adjustSize(self.z)

        x, y, z, d, h = self.x, self.y, self.z, self.d, self.h
        r = self.radius = self.radius or min(x, y) / 2.0
        thickness = self.thickness

        self.c4 = math.pi * r * 0.5 * 0.95
        self.latchsize = 8 * thickness


        self.open()

        s = edges.FingerJointSettings(self.thickness, finger=1.,
                                      space=1., surroundingspaces=1)
        s.edgeObjects(self, "gGH")

        self.ctx.save()
        #lid
        self.surroundingWall(move="right")
        #bottom
        self.rectangularWall(x, z, edges="FFFF", move="right")

        self.ctx.restore()

        self.surroundingWall(move="up only")

        #sides
        self.flexBoxSide(x, y, r, move="right")
        self.flexBoxSide(x, y, r, move="mirror right")

        #front
        self.rectangularWall(z, y, edges="fFbF")

        self.close()


