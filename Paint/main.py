import pygame, sys, os
from pygame.locals import *
from math import ceil, floor

class Button:
    def __init__(self, pos, image, type, size):
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.image = image
        self.type = type
        self.size = size

    def render(self, surf):
        surf.blit(self.image, (self.rect[0], self.rect[1]))

    def if_click(self, surf, mpos, user):
        if pygame.mouse.get_pressed()[0] and self.rect.colliderect(
            mpos[0], mpos[1]+50, 1, 1
        ):
            pygame.draw.rect(surf, (255, 255, 255), self.rect, 1)
            
            match self.type:
                case 'rubber':
                    user.rubbing = True
                    user.curr_colour = (230, 230, 230)
                    user.start_fill = False
                    user.choose = False
                case 'bucket':
                    user.start_fill = True
                    user.rubbing = False
                    user.choose = False
                case 'pencil':
                    user.curr_colour = (0, 0, 0)
                    user.start_fill = False
                    user.rubbing = False
                    user.choose = False
                case 'choose':
                    user.start_fill = False
                    user.rubbing = False
                    user.choose = True
                case 'changing_colour':
                    user.start_fill = False
                    user.rubbing = False
                    user.choose = False
                    user.changing_colour = True
                    user.changed_colour = [
                        user.curr_colour[0], 
                        user.curr_colour[1], 
                        user.curr_colour[2]
                        ]
                case 'save':
                    user.save = True
                case 'open':
                    user.open = True

class User:
    def __init__(self, canvas):
        canvas.fill((230, 230, 230))
        self.tile_size = 16
        self.tiles = {}
        self.curr_colour = (0, 0, 0)
        self.change_colour_id = 0
        self.changed_colour = [
            self.curr_colour[0], 
            self.curr_colour[1], 
            self.curr_colour[2]
            ]
        self.changing_colour = False
        self.start_fill = False
        self.past_colour = (255, 255, 255)
        self.itter_cnt = 0
        self.choose = False

        self.colour_wheel = pygame.image.load('main_images/colourwheel2.png')
        self.colour_wheel = pygame.transform.scale(
            self.colour_wheel, (200, 200)
        )
        self.rubbing = False
        self.cursor_images = {
            'rubber': pygame.transform.scale(pygame.image.load('main_images/cursor_image1.png'), (48, 48)),
            'bucket': pygame.transform.scale(pygame.image.load('main_images/cursor_image2.png'), (48, 48)),
            'pencil': pygame.transform.scale(pygame.image.load('main_images/cursor_image3.png'), (48, 48)),
            'choose': pygame.transform.scale(pygame.image.load('main_images/cursor_image4.png'), (48, 48)),
            'changing_colour': pygame.transform.scale(pygame.image.load('main_images/cursor_image5.png'), (48, 48)),
            'save': pygame.transform.scale(pygame.image.load('main_images/cursor_image6.png'), (48, 48)),
            'open': pygame.transform.scale(pygame.image.load('main_images/cursor_image7.png'), (48, 48))
        }
        self.cursor_area = pygame.Rect(0, 0, self.tile_size, self.tile_size)
        self.save = False
        self.file_name = ''
        self.open = False

    def get_real_pos(self):
        mpos = self.get_pos()
        real_mpos = [
            mpos[0]-(mpos[0]%self.tile_size),
            mpos[1]-(mpos[1]%self.tile_size)
        ]
        self.cursor_area.x = real_mpos[0]
        self.cursor_area.y = (real_mpos[1]+50)
        return real_mpos

    def fill(self, tile_pos):
        self.itter_cnt += 1
        try: 
            pos = f'{tile_pos[0]} {tile_pos[1]-self.tile_size}'
            if self.tiles[pos] == self.past_colour:
                self.tiles[pos] = self.curr_colour
                new_pos = pos.split()
                pos = [int(new_pos[0]), int(new_pos[1])]
                self.fill(pos)
        except Exception as e: print(e)
        try: 
            pos = f'{tile_pos[0]} {tile_pos[1]+self.tile_size}'
            if self.tiles[pos] == self.past_colour:
                self.tiles[pos] = self.curr_colour
                new_pos = pos.split()
                pos = [int(new_pos[0]), int(new_pos[1])]
                self.fill(pos)
        except Exception as e: print(e)
        try: 
            pos = f'{tile_pos[0]-self.tile_size} {tile_pos[1]}'
            if self.tiles[pos] == self.past_colour:
                self.tiles[pos] = self.curr_colour
                new_pos = pos.split()
                pos = [int(new_pos[0]), int(new_pos[1])]
                self.fill(pos)
        except Exception as e: print(e)
        try: 
            pos = f'{tile_pos[0]+self.tile_size} {tile_pos[1]}'
            if self.tiles[pos] == self.past_colour:
                self.tiles[pos] = self.curr_colour
                new_pos = pos.split()
                pos = [int(new_pos[0]), int(new_pos[1])]
                self.fill(pos)
        except Exception as e: print(e)

    def draw_fills(self, window):
        for key in self.tiles:
            tmp_pos = key.split()
            pos = [int(tmp_pos[0]), int(tmp_pos[1])]
            pygame.draw.rect(window, self.tiles[key], (
                pos[0], pos[1], self.tile_size, self.tile_size
            ))

    def get_pos(self):
        mpos = pygame.mouse.get_pos()
        mpos = [mpos[0], mpos[1]-50]
        return mpos

    def draw(self, canvas, window):
        if pygame.mouse.get_pressed()[0]:
            try:
                mpos = self.get_pos()
                for j in range(int(self.cursor_area[3]/self.tile_size)):
                    for i in range(int(self.cursor_area[2]/self.tile_size)):
                        pygame.draw.rect(canvas, self.curr_colour, (
                            (mpos[0]-(mpos[0]%self.tile_size))+self.tile_size*i, 
                            mpos[1]-(mpos[1]%self.tile_size)+self.tile_size*j, 
                            self.tile_size, self.tile_size
                        ))
                        alligned_mpos = [(mpos[0]-(mpos[0]%self.tile_size))+self.tile_size*i, mpos[1]-(mpos[1]%self.tile_size)+self.tile_size*j]
                        if not self.tiles[f'{alligned_mpos[0]} {alligned_mpos[1]}'] == self.curr_colour:
                            self.past_colour = self.tiles[f'{alligned_mpos[0]} {alligned_mpos[1]}']
                            self.tiles[f'{alligned_mpos[0]} {alligned_mpos[1]}'] = self.curr_colour
            except: 
                try:
                    if mpos[0] > 600:
                        self.curr_colour = window.get_at(
                            (mpos[0], mpos[1])
                        )
                        self.changed_colour = [
                            self.curr_colour[0], 
                            self.curr_colour[1], 
                            self.curr_colour[2]
                            ]
                except: pass
        elif pygame.mouse.get_pressed()[2]:
            try:
                mpos = self.get_pos()
                pygame.draw.rect(canvas, (255, 255, 255), (
                    mpos[0]-(mpos[0]%self.tile_size), mpos[1]-(mpos[1]%self.tile_size), self.tile_size, self.tile_size
                ))
                alligned_mpos = [mpos[0]-(mpos[0]%self.tile_size), mpos[1]-(mpos[1]%self.tile_size)]
                self.tiles[f'{alligned_mpos[0]} {alligned_mpos[1]}'] = (255, 255, 255)
            except: pass

    def show_cursor(self, surf, colour, canvas):
        mpos = self.get_pos()
        if self.start_fill: pass
            #cursor_image = self.cursor_images['bucket']
        elif self.rubbing: pass
            #cursor_image = self.cursor_images['rubber']
        elif self.choose: pass
            #cursor_image = self.cursor_images['choose']
        elif self.changing_colour:
            #cursor_image = self.cursor_images['changing_colour']
            self.show_colour(surf, colour)
        else:pass
            #cursor_image = self.cursor_images['pencil']

        
        #surf.blit(cursor_image, mpos)   

    def show_colour(self, surf, colour):
        changing_colour = (
            colour[0],
            colour[1],
            colour[2]
        )
        pygame.draw.rect(surf, changing_colour, (650, 50, 100, 100))

def main():
    WINDOW_SIZE = (800, 650)
    window = pygame.display.set_mode(WINDOW_SIZE)
    sizex, sizey = 600, 600
    canvas = pygame.Surface((sizex, sizey))
    x, y = 0, 50
    start_drawing = False

    user = User(canvas)

    buttons = [Button([0, 0], user.cursor_images['rubber'], 'rubber', [50, 50]),
               Button([54, 0], user.cursor_images['bucket'], 'bucket', [50, 50]),
               Button([108, 0], user.cursor_images['pencil'], 'pencil', [50, 50]),
               Button([162, 0], user.cursor_images['choose'], 'choose', [50, 50]),
               Button([216, 0], user.cursor_images['changing_colour'], 'changing_colour', [50, 50]),
               Button([270, 0], user.cursor_images['save'], 'save', [50, 50]),
               Button([324, 0], user.cursor_images['open'], 'open', [50, 50])]
    btile_size = user.tile_size
    brush_rect = pygame.Rect(
        600+((200/2)-(btile_size/2)), 
        50+((100/2)-(btile_size/2)), 
        btile_size, btile_size
        )
    #pygame.mouse.set_visible(False)

    while 1:
        window.fill((0, 0, 0))
        window.blit(user.colour_wheel, (600, 400))
        pygame.draw.rect(window, (245, 245, 245), (600, 200, 400, 200))

        if not start_drawing:
            print(user.tile_size)
        
        if user.changing_colour:
            print(user.changed_colour)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if not user.save and not user.open:
                    if event.key == K_RETURN:
                        if not start_drawing:
                            cwidth = canvas.get_width()
                            cheight = canvas.get_height()
                            for j in range(cwidth):
                                for i in range(cheight):
                                    if j % user.tile_size == 0:
                                        if i % user.tile_size == 0:
                                            pos = f'{i} {j}'
                                            user.tiles[pos] = (230, 230, 230)
                            start_drawing = True
                            user.cursor_area[2] = user.tile_size
                            user.cursor_area[3] = user.tile_size
                            brush_rect = pygame.Rect(
                                600+((200/2)-(user.tile_size/2)), 
                                50+((100/2)-(user.tile_size/2)), 
                                user.tile_size, user.tile_size
                                )
                        else:
                            if user.changing_colour == True:
                                if user.change_colour_id < 2:
                                    user.change_colour_id += 1
                                else:
                                    user.changing_colour = False
                                    new_colour = (
                                        user.changed_colour[0],
                                        user.changed_colour[1],
                                        user.changed_colour[2]
                                    )
                                    user.curr_colour = new_colour
                                    user.changed_colour = [
                                        user.curr_colour[0], 
                                        user.curr_colour[1], 
                                        user.curr_colour[2]
                                        ]
                                    user.change_colour_id = 0
                    elif event.key == K_f:
                        user.start_fill = True
                    elif event.key == K_c:
                        user.choose = True
                else: 
                    if event.key != K_RETURN:
                        if event.key != K_BACKSPACE:
                            try: 
                                user.file_name += chr(event.key)
                                print(user.file_name)
                            except: pass
                        else: user.file_name[len(user.file_name)-1] = '\0'
                    else: 
                        if user.save:
                            images = os.listdir()

                            if not (user.file_name + '.png') in images: 
                                pygame.image.save(canvas, user.file_name + '.png')
                                pygame.quit()
                                sys.exit()
                            else:
                                user.file_name = ''
                                print('file name already in use - retype')
                        else:
                            images = os.listdir()

                            if (user.file_name + '.png') in images: 
                                saved_img = pygame.image.load(user.file_name + '.png')
                                canvas.blit(saved_img, (0, 0))
                                user.file_name = ''
                                for x in range(floor(canvas.get_width() / user.tile_size)):
                                    for y in range(floor(canvas.get_height() / user.tile_size)):
                                        new_x = x * user.tile_size
                                        new_y = y * user.tile_size
                                        colour = canvas.get_at((new_x, new_y))
                                        if user.tiles[f'{new_x} {new_y}'] != colour:
                                            user.tiles[f'{new_x} {new_y}'] = colour
                                user.open = False
                            else:
                                user.file_name = ''
                                print('file does not exist - retype')
            elif event.type == MOUSEBUTTONDOWN:
                keys = pygame.key.get_pressed()
                if not keys[pygame.K_z]:
                    if event.button == 1:
                        if user.start_fill:
                            start_pos = user.get_real_pos()
                            user.fill(start_pos)
                            user.start_fill = False
                            user.itter_cnt = 0
                            user.draw_fills(canvas)
                        elif user.choose:
                            mpos = user.get_real_pos()
                            pos = f'{mpos[0]} {mpos[1]}'
                            user.curr_colour = user.tiles[pos]
                            user.choose = False
                    elif event.button == 4:
                        if not start_drawing:
                            user.tile_size -= 1
                        else:
                            mpos = user.get_pos()
                            if user.changing_colour:
                                if user.changed_colour[user.change_colour_id] < 255:
                                    user.changed_colour[user.change_colour_id] += 1
                            elif brush_rect.colliderect((mpos[0], mpos[1]+50, 1, 1)):
                                if btile_size > user.tile_size:
                                    btile_size -= user.tile_size
                                user.cursor_area.width = btile_size
                                user.cursor_area.height = btile_size
                    elif event.button == 5:
                        if not start_drawing:
                            user.tile_size += 1
                        else:
                            mpos = user.get_pos()
                            if user.changing_colour:
                                if user.changed_colour[user.change_colour_id] > 0:
                                    user.changed_colour[user.change_colour_id] -= 1
                            elif brush_rect.colliderect((mpos[0], mpos[1]+50, 1, 1)):
                                btile_size += user.tile_size
                                user.cursor_area.width = btile_size
                                user.cursor_area.height = btile_size
                else:
                    if event.button == 4:
                        sizex += 10
                        sizey += 10
                    elif event.button == 5:
                        sizey -= 10
                        sizex -= 10

        if start_drawing:
            user.draw(canvas, window)

            for button in buttons:
                mpos = user.get_pos()
                button.if_click(window, mpos, user)
                button.render(window)

        window.blit(canvas, (0, 50))
        pygame.draw.rect(window, user.curr_colour, brush_rect)
        user.show_cursor(window, user.changed_colour, canvas)
        real_pos = user.get_real_pos()
        try:
            colour = user.tiles[f'{real_pos[0]} {real_pos[1]}']
            half = .5
            for id, value in enumerate(colour):
                if value > 127 and id != 3:
                    half = 2
            if half == .5:
                new_colour = (
                    abs((colour[2]/half)-abs(255-(colour[2]/half))),
                    abs((colour[1]/half)-abs(255-(colour[1]/half))),
                    abs((colour[0]/half)-abs(255-(colour[0]/half)))
                )
            else:
                new_colour = (
                    colour[2]/half,
                    colour[1]/half,
                    colour[0]/half
                )
            pygame.draw.rect(window, new_colour, user.cursor_area, 1)
        except: pygame.draw.rect(window, (255, 0, 0), user.cursor_area, 1)
        pygame.display.update()

if __name__ == '__main__':
    main()