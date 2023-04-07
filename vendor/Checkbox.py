import pygame

pygame.font.init()

class Checkbox:
    def __init__(self, surface, x, y, idnum, color=(230, 230, 230), caption="", outline_color=(0, 0, 0), check_color=(0, 0, 0),font_size=22, font_color=(0, 0, 0), text_offset=(28, 1), font='Ariel Black', checked=False, algo="classic"):
        """
         Initialize the object with the parameters. This is the constructor for the class. It will be called by pygame.
         
         @param surface - Surface to draw on. This is the surface that will be used for drawing the object.
         @param x - X position of the object in pixels. ( x y ) is the upper left corner of the bounding box.
         @param y - Y position of the object in pixels. ( y x ) is the upper left corner of the bounding box.
         @param idnum - Unique number for the object. This is an integer between 0 and 3.
         @param color - Color of the object. ( r g b ) is the red green and blue components of the rectangle.
         @param caption - Text to display in the textbox. ( r g b ) is the green component of the rectangle.
         @param outline_color - Color of the outline of the object.
         @param check_color - Color of the check box.
         @param font_size - Font size of the textbox. Default is 22. ( width height ) is the minimum size of the textbox.
         @param font_color - Font color of the textbox. Default is ( 0 0 0 ).
         @param text_offset - Offset to be added to the textbox.
         @param font
         @param checked
         @param algo
        """
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        self.ft = font

        #identification for removal and reorginazation
        self.idnum = idnum

        # Algorithm linked with the checkbox
        self.algo = algo
        # checkbox object
        self.checkbox_obj = pygame.Rect(self.x, self.y, 12, 12)
        self.checkbox_outline = self.checkbox_obj.copy()

        # variables to test the different states of the checkbox
        self.checked = checked

    def _draw_button_text(self):
        """
         Draw button text on the surface. This is called by self. _draw_button () to draw the button
        """
        self.font = pygame.font.SysFont(self.ft, self.fs)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + self.to[0], self.y + 12 / 2 - h / 2 + 
        self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        """
         Render the checkbox to the surface. This is called every time the checkbox is toggled on or
        """
        # Draw the checkboxes in the surface.
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + 6, self.y + 6), 4)

        elif not self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self, event_object):
        """
         Update the state of the checkbox based on the mouse position. This is called by pygame. event. OnMouseDown and pygame. event. OnMouseUp
         
         @param event_object - The object that triggered
        """
        x, y = pygame.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        # if x y w x y w
        if px < x < px + w and py < y < py + w:
            # Set the checked state of the checkbox.
            if self.checked:
                self.checked = False
            else:
                self.checked = True

    def update_checkbox(self, event_object):
        """
         Update the checkbox based on mouse events. This is called by pygame. event. OnMouseDown
         
         @param event_object - The event that triggered
        """
        # This method is called when the mouse button is pressed.
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
            self._update(event_object)
            