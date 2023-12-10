import pygame
import sys
import constants
import random

# cutscene manager class
class CutsceneManager:
    def __init__(self):
        self.scenes = []
        self.active_scene = None
        self.scene_index = 0
        self.elapsed_time = 0

    def add_scene(self, scene):
        self.scenes.append(scene)

    def start(self):
        if self.scenes:
            self.active_scene = self.scenes[0]
            self.scene_index = 0
            self.active_scene.start()

    def update(self):
        if self.active_scene is not None:
            if self.active_scene.is_finished():
                self.scene_index += 1
                if self.scene_index < len(self.scenes):
                    self.active_scene = self.scenes[self.scene_index]
                    self.active_scene.start()
                else:
                    self.active_scene = None
            else:
                self.active_scene.update()

    def draw(self, screen):
        if self.active_scene is not None:
            self.active_scene.draw(screen)

    def is_finished(self):
        # check if there are no more scenes to play
        return self.active_scene is None and self.scene_index >= len(self.scenes)


# base class for scenes
class Scene:
    def start(self):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

    def is_finished(self):
        return True


# example of a specific scene
class DialogueScene(Scene):
    def __init__(self, text, duration, font, bg_image=None):
        self.text = text
        self.background_image = bg_image
        self.duration = duration
        self.font = font
        self.start_ticks = pygame.time.get_ticks()
        self.elapsed_time = 0

    def start(self):
        self.start_ticks = pygame.time.get_ticks()

    def update(self):
        current_ticks = pygame.time.get_ticks()
        self.elapsed_time = (current_ticks - self.start_ticks) / 1000

    def draw(self, screen):
        if self.background_image:
            # draws background image if it exists
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill(constants.BLACK)

        rect_height = 50  # Adjust the height as needed
        pygame.draw.rect(screen, constants.BLACK,
                         (0, screen.get_height() - rect_height, screen.get_width(), rect_height))

        render_text = self.font.render(self.text, True, constants.WHITE)
        text_rect = render_text.get_rect(center=(constants.SCREEN_WIDTH//2 + 25, 545))
        screen.blit(render_text, text_rect)

    def is_finished(self):
        return self.elapsed_time >= self.duration



class TrippyScene(Scene):
    def __init__(self, image_list, duration, font, text, change_interval=500):  # change_interval in milliseconds
        self.image_list = image_list
        self.duration = duration
        self.change_interval = change_interval
        self.last_change_time = 0
        self.elapsed_time = 0
        self.current_image = random.choice(self.image_list)
        self.transformed_image = self.apply_effect(self.current_image)
        self.start_ticks = pygame.time.get_ticks()
        self.font = font
        self.text = text

    def start(self):
        self.start_ticks = pygame.time.get_ticks()
        self.last_change_time = self.start_ticks
        self.current_image = random.choice(self.image_list)
        self.transformed_image = self.apply_effect(self.current_image)

    def update(self):
        current_ticks = pygame.time.get_ticks()
        self.elapsed_time = (current_ticks - self.start_ticks) / 1000

        # Change the image if the interval has passed
        if current_ticks - self.last_change_time > self.change_interval:
            self.current_image = random.choice(self.image_list)
            self.transformed_image = self.apply_effect(self.current_image)
            self.last_change_time = current_ticks

    def draw(self, screen):
        if self.elapsed_time < self.duration:
            # Draw the transformed image
            x = random.randint(0, max(0, screen.get_width() - self.transformed_image.get_width()))
            y = random.randint(0, max(0, screen.get_height() - self.transformed_image.get_height()))
            screen.blit(self.transformed_image, (x, y))

            rect_height = 50  # Adjust the height as needed
            pygame.draw.rect(screen, constants.BLACK,
                             (0, screen.get_height() - rect_height, screen.get_width(), rect_height))

            render_text = self.font.render(self.text, True, constants.WHITE)
            text_rect = render_text.get_rect(center=(constants.SCREEN_WIDTH // 2 + 25, 545))
            screen.blit(render_text, text_rect)

    def is_finished(self):
        return self.elapsed_time >= self.duration

    def apply_effect(self, image):
        # Apply the trippy effect
        angle = random.randint(0, 360)
        scale = random.uniform(0.5, 1.5)
        return pygame.transform.rotozoom(image, angle, scale)
