import pygame
import math
import numpy as np

class Segment:
    def __init__(self, x: float, y: float, length: float, angle: float):
        self.length = length
        self.a = np.array([x, y])
        self.b = np.array([0, 0]) # Defined as default, will be updated anyway
        self.angle = angle
        self.length = length

    def calculate_b(self):
        """
        Calculates b based on the angle and the length of the segment,
        converting polar coordinates to cathesian ones.
        """
        dx = self.length * math.cos(self.angle)
        dy = self.length * math.sin(self.angle)

        self.b = [
            self.a[0] + dx,
            self.a[1] + dy
        ]


    def follow(self, x, y):
        """
        First updates the new angle to where ever the target (x, y) is pointing,
        then recalculates a based on the new position of b.
        """
        self.angle = math.atan2(
            y - self.a[1], x - self.a[0]
        )

        target = np.array([x, y])
        dir = np.subtract(target, self.a)
        
        dir = dir / np.linalg.norm(dir)
        dir = dir * self.length

        dir = dir * -1

        self.a = np.add(target, dir)

    def draw(self, screen: pygame.surface):
        pygame.draw.line(screen, "white", self.a, self.b, 10)

class SegmentChain:
    def __init__(self, segment_amount, segments_length):
        self.segment_amount = segment_amount
        self.segments_length = segments_length
        self.attach_point = None
        self.segments = []
        self.generate_segments()


    def attach(self, attach_point):
        self.attach_point = attach_point

    def generate_segments(self):
        for i in range(self.segment_amount):
            self.segments.append(
                Segment(
                    1,
                    1,
                    self.segments_length,
                    0
                )
        )
            
    def update(self, screen: pygame.surface):
        """
        Update all the segments.
        """

        # Get the last segment, make it follow the mouse
        end = self.segments[len(self.segments) - 1]

        end.follow(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        end.calculate_b()

        # Browse the list of segments backward, excuding the last one, make it follow the starting point (a) of the next one.
        for i in range(len(self.segments) - 2, -1, -1):
            self.segments[i].follow(self.segments[i + 1].a[0], self.segments[i + 1].a[1])
            self.segments[i].calculate_b()

        if self.attach_point:
            self.attach_chain()

        # Draw every segments
        for i in range(len(self.segments)):
            self.segments[i].draw(screen)

        self.draw_circles(screen)

    def attach_chain(self):
        """
        Attach the chain to the attach point.
        """

        # Re define the a of the last one to the fixed point
        self.segments[0].a = self.attach_point
        self.segments[0].calculate_b()

        # Re attach every segments together except the first one
        for i in range(1, len(self.segments)):
            self.segments[i].a = self.segments[i - 1].b
            self.segments[i].calculate_b()

    def draw_circles(self, screen):
        """
        Draw the joint circles.
        """
        
        for segment in self.segments:
            pygame.draw.circle(screen, "red", segment.b, 20)
    
        pygame.draw.circle(screen, "red", self.segments[0].a, 40)
            
