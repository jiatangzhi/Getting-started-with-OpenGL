# imports all openGL functions
from OpenGL.GL import *

# pygame is just used to create a window with the operating system on which to draw.
import pygame

# we will use numpy to store data in arrays
import numpy as np

class Scene:
    '''
    This is the main class for drawing an OpenGL scene using the PyGame library
    '''
    def __init__(self):
        '''
        Initialises the scene
        '''
    
        self.window_size = (800,600)

        # the first two lines initialise the pygame window. You could use another library for this,
        # for example GLut or Qt
        pygame.init()
        screen = pygame.display.set_mode(self.window_size, pygame.OPENGL | pygame.DOUBLEBUF, 24)

        # Here we start initialising the window from the OpenGL side
        glViewport(0, 0, self.window_size[0], self.window_size[1])

        # this selects the background colour
        glClearColor(0.0, 0.5, 0.5, 1.0)
        
        self.camera = Camera(self.window_size)

        # This class will maintain a list of models to draw in the scene,
        # we will initalise it to empty
        self.models = []

    def add_model(self,model):
        '''
        This method just adds a model to the scene.
        :param model: The model object to add to the scene
        :return: None
        '''
        self.models.append(model)

    def draw(self):
        '''
        Draw all models in the scene
        :return: None
        '''

        # first we need to clear the scene
        glClear(GL_COLOR_BUFFER_BIT)

        # saves the current position
        glPushMatrix()

        # apply the camera parameters
        self.camera.apply()

        # then we loop over all models in the list and draw them
        for model in self.models:
            model.draw()
                
        # retrieve the last saved position
        glPopMatrix()

        # once we are done drawing, we display the scene
        # Note that here we use double buffering to avoid artefacts:
        # we draw on a different buffer than the one we display,
        # and flip the two buffers once we are done drawing.
        pygame.display.flip()


    def keyboard(self, event):
        if event.key == pygame.K_q:
            self.running = False

        elif event.key == pygame.K_0:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);

        elif event.key == pygame.K_1:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);


        self.camera.keyboard(event)

    def run(self):
        '''
        Draws the scene in a loop until exit.
        '''

    # We have a classic program loop
        running = True
        while running:

        # check whether the window has been closed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # keyboard events
                elif event.type == pygame.KEYDOWN:
                    self.keyboard(event)

                elif False and event.type == pygame.MOUSEMOTION:
                    if pygame.MOUSEBUTTONDOWN:
                        dx, dy = event.rel
                        self.camera.position[0] -= dx / self.window_size[0] /10 - 0.5
                        self.camera.position[1] -= dy / self.window_size[1] /10- 0.5

        # otherwise, continue drawing
            self.draw()


class BaseModel:
    '''
    Base class for all models, implementing the basic draw function for triangular meshes.
    Inherit from this to create new models.
    '''

    def __init__(self, position=[0,0,0], orientation=0, scale=1, color=[1,1,1]):
        '''
        Initialises the model data
        '''

        # store the object's color
        self.color = color

        # store the position of the model in the scene, ...
        self.position = position

        # ... the orientation, ...
        self.orientation = orientation

        # ... and the scale factor
        self.scale = scale


    def applyParameters(self):
        # apply the position and orientation of the object
        glTranslate(*self.position)
        glRotate(self.orientation, 0, 0, 1)

        # apply scaling across all dimensions
        glScale(self.scale, self.scale, self.scale)

        # then set the colour
        glColor(self.color)

    def draw(self):
        '''
        Draws the model using OpenGL functions
        :return:
        '''

        # saves the current pose parameters
        glPushMatrix()

        self.applyParameters()

        # Here we will use the simple GL_TRIANGLES primitive, that will interpret each sequence of
        # 3 vertices as defining a triangle.
        glBegin(GL_TRIANGLES)

        # we loop over all vertices in the model
        for vertex in self.vertices:

            # This function adds the vertex to the list
            glVertex(vertex)

        # the call to glEnd() signifies that all vertices have been entered.
        glEnd()

        # retrieve the previous pose parameters
        glPopMatrix()

        def applyPose(self):
            # apply the position and orientation and size of the object
            glTranslate(*self.position)
            glRotate(self.orientation, 0, 0, 1)
            glScale(self.scale, self.scale, self.scale)
            glColor(self.color)

class TriangleModel(BaseModel):
    '''
    A very simple model for drawing a single triangle. This is only for illustration purpose.
    '''
    def __init__(self, position=[0, 0, 0], orientation=0, scale=1, color=[1, 1, 1]):
        BaseModel.__init__(self, position=position, orientation=orientation, scale=scale, color=color)

        # each row encodes the coordinate for one vertex.
        # given that we are drawing in 2D, the last coordinate is always zero.
        self.vertices = np.array(
            [
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0],
                [1.0, 1.0, 0.0]
            ], 'f')

class ComplexModel(BaseModel):
    def __init__(self, position=[0,0,0], orientation=0, scale=1):
        BaseModel.__init__(self, position=position, orientation=orientation, scale=scale)

        # list of simple components
        self.components = [
            TriangleModel(position=[0, 0, 0], scale=0.5, orientation=-45, color=[0, 1, 0]),
            TriangleModel(position=[0, 0.25, 0], scale=0.5, orientation=-45, color=[0, 1, 0]),
            TriangleModel(position=[0, 0.5, 0], scale=0.5, orientation=-45, color=[0, 1, 0]),
            TriangleModel(position=[0.25, -0.25, 0], scale=0.25, orientation=0, color=[0.6, 0.2, 0.2]),
            TriangleModel(position=[0.5, 0, 0], scale=0.25, orientation=-180, color=[0.6, 0.2, 0.2])
        ]

    def draw(self):
        glPushMatrix()

        # apply the parameters for the whole model
        self.applyParameters()

        # draw all component primitives
        for component in self.components:
            component.draw()

        glPopMatrix()
        
        
class HouseModel(BaseModel):
    def __init__(self, position=[0,0,0], orientation=0, scale=1):
        BaseModel.__init__(self, position=position, orientation=orientation, scale=scale)

        # list of simple components
        self.components = [
            #House
            TriangleModel(position=[0.3, -0.75, 0], scale=1, orientation=90, color=[0.45,0.5,0.5]),
            TriangleModel(position=[-0.7, 0.25, 0], scale=1, orientation=-90, color=[0.45,0.5,0.5]),
            #Roof
            TriangleModel(position=[-0.9, 0.25, 0], scale=1, orientation=-45, color=[1,0,0]),
            #LeftWindow
            TriangleModel(position=[-0.63, -0.25, 0], scale=0.4, orientation=0, color=[1, 0.9, 5]),
            TriangleModel(position=[-0.23, 0.15, 0], scale=0.4, orientation=-180, color=[1, 0.9, 5]),
            #RightWindow
            TriangleModel(position=[-0.15, -0.25, 0], scale=0.4, orientation=0, color=[1, 0.9, 5]),
            TriangleModel(position=[0.25, 0.15, 0], scale=0.4, orientation=-180, color=[1, 0.9, 5]),
            #Door
            TriangleModel(position=[-0.3, -0.75, 0], scale=0.3, orientation=0, color=[0.6, 0.2, 0.2]),
            TriangleModel(position=[0, -0.45, 0], scale=0.3, orientation=-180, color=[0.6, 0.2, 0.2])
        ]

    def draw(self):
        glPushMatrix()

        # apply the parameters for the whole model
        self.applyParameters()

        # draw all component primitives
        for component in self.components:
            component.draw()

        glPopMatrix()


class Camera:
    '''
    Basic class for handling the camera pose. At this stage, just x and y offsets.
    '''
    def __init__(self,size):
        self.size = size
        self.position = [0.0,0.0,0.0]

    def apply(self):
        '''
        Apply the camera parameters to the current OpenGL context
        Note that this is the old fashioned API, we will use matrices in the
        future.
        '''
        glTranslate(*self.position)

    def keyboard(self,event):
        '''
        Handles keyboard events that are related to the camera.
        '''
        if event.key == pygame.K_PAGEDOWN:
            self.position[2] += 0.01

        if event.key == pygame.K_PAGEUP:
            self.position[2] -= 0.01

        if event.key == pygame.K_DOWN:
            self.position[1] += 0.01

        if event.key == pygame.K_UP:
            self.position[1] -= 0.01

        if event.key == pygame.K_LEFT:
            self.position[0] += 0.01

        if event.key == pygame.K_RIGHT:
            self.position[0] -= 0.01


if __name__ == '__main__':
    # initialises the scene object
    scene = Scene()

    # adds a few objects to the scene
    scene.add_model(ComplexModel(position=[-0.15,-0.8,0], scale=0.6))
    scene.add_model(ComplexModel(position=[-0.8,-0.6,0], scale=0.6))
    scene.add_model(HouseModel(position=[-0.25,-0.60,0], scale=0.5))
    scene.add_model(ComplexModel(position=[0.2,0.6,0], scale=0.3))
    scene.add_model(ComplexModel(position=[-0.15,0.4,0], scale=0.4))
    scene.add_model(HouseModel(position=[0.5,0.5,0], scale=0.25))
    scene.add_model(ComplexModel(position=[0.5,0.3,0], scale=0.5))

    # starts drawing the scene
    scene.run()
