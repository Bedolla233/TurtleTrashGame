def mouseMove(self):
        #Makes mouse invisible
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        self.rect.center= pygame.mouse.get_pos()