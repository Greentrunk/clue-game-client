import pygame
import queue


class GUI:
    def __init__(self, ws):
        pygame.init()
        self.game_state_queue = queue.Queue()
        self.ws = ws
        self.screen = pygame.display.set_mode((1200, 720))
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.game_board_img = pygame.image.load("assets/textures/clue_board.jpg")
        self.game_board = self.game_board_img.get_rect()
        self.game_board.center = self.screen.get_rect().center

    def run(self):
        while self.is_running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    self.is_running = False

            # POLL FOR CURRENT GAME STATE IF MESSAGE
            try:
                while not self.game_state_queue.empty():
                    game_state = self.game_state_queue.get_nowait()
                    print(f"Game state is {game_state}")
            except queue.Empty:
                pass

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("black")

            # RENDER HERE
            self.screen.blit(self.game_board_img, self.game_board)

            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

    def quit(self):
        pygame.quit()
        self.ws.close()
