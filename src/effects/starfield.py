import os
import sys
import pygame
import random
from src.utils import get_asset_path

class Star:
    def __init__(self, x, y, speed, size):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.alpha = random.randint(50, 255)

    def update(self, height):
        self.y += self.speed
        if self.y > height:
            self.y = 0
            self.x = random.randint(0, 800)

    def draw(self, surface):
        color = (self.alpha, self.alpha, self.alpha)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)

class SpaceObject:
    def __init__(self, x, y, speed, image, size, image_name):
        self.x = x
        self.y = y
        self.speed = speed
        self.original_image = image
        self.image = pygame.transform.scale(image, (size, size))
        self.alpha = random.randint(30, 50)
        self.type = image_name  # Usar el nombre del archivo

    def update(self, height):
        self.y += self.speed
        if self.y > height:
            return True
        return False
            
    def draw(self, surface):
        temp_surface = self.image.copy()
        temp_surface.set_alpha(self.alpha)
        surface.blit(temp_surface, (int(self.x), int(self.y)))

class StarField:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.space_images = {}

        try:
            # Usar get_asset_path para obtener la ruta correcta
            base_path = get_asset_path('space')
            
            if os.path.exists(base_path):
                print(f"Carpeta space encontrada en: {base_path}")
                for file in os.listdir(base_path):
                    if file.endswith('.png'):
                        img_path = os.path.join(base_path, file)
                        try:
                            img = pygame.image.load(img_path)
                            self.space_images[file] = img
                            print(f"Cargada imagen espacial: {file}")
                        except Exception as e:
                            print(f"Error cargando imagen {file}: {e}")
            else:
                print(f"Directorio space no encontrado: {base_path}")
                self._create_backup_images()
        except Exception as e:
            print(f"Error accediendo a space: {e}")
            self._create_backup_images()

        # Crear estrellas
        self.back_stars = [Star(random.randint(0, width), random.randint(0, height), 1, 1) for _ in range(50)]
        self.mid_stars = [Star(random.randint(0, width), random.randint(0, height), 2, 1) for _ in range(30)]
        self.front_stars = [Star(random.randint(0, width), random.randint(0, height), 3, 2) for _ in range(20)]
        
        # Array para múltiples objetos espaciales
        self.space_objects = []
        self.spawn_counter = 0
        self.spawn_delay = 300  # Más tiempo entre grupos de spawn
        self.max_objects = 3
        self.current_types = set()  # Registrar tipos actuales

    def _create_backup_images(self):
        """Crear imágenes de respaldo si no se encuentran las originales"""
        colors = [(100, 100, 100), (150, 150, 150), (200, 200, 200)]
        for i, color in enumerate(colors):
            backup = pygame.Surface((50, 50))
            backup.fill(color)
            self.space_images[f'backup_{i}.png'] = backup
        print("Creadas imágenes de respaldo")

    def spawn_group(self):
        available_images = [name for name in self.space_images.keys() 
                          if name not in self.current_types]
        
        if len(available_images) >= 3:
            selected_names = random.sample(available_images, 3)
            
            configs = [
                {"size": 40, "speed": 0.3},
                {"size": 30, "speed": 0.5},
                {"size": 20, "speed": 0.7}
            ]
            
            x_positions = random.sample(range(50, self.width - 50, 100), 3)
            
            for name, config, x in zip(selected_names, configs, x_positions):
                obj = SpaceObject(x, -50, config["speed"], 
                                self.space_images[name], 
                                config["size"],
                                name)
                self.space_objects.append(obj)
                self.current_types.add(name)

    def update(self):
        # Actualizar estrellas
        for star in self.back_stars + self.mid_stars + self.front_stars:
            star.update(self.height)
            
        # Actualizar y limpiar objetos espaciales
        new_objects = []
        for obj in self.space_objects:
            if not obj.update(self.height):
                new_objects.append(obj)
            else:
                self.current_types.remove(obj.type)
        self.space_objects = new_objects
            
        # Spawning de nuevo grupo
        if len(self.space_objects) == 0:
            self.spawn_counter += 1
            if self.spawn_counter >= self.spawn_delay:
                self.spawn_counter = 0
                if random.random() < 0.8:  # 80% de probabilidad
                    self.spawn_group()

    def draw(self, surface):
        # Dibujar objetos espaciales primero
        for space_obj in self.space_objects:
            space_obj.draw(surface)
        # Luego las estrellas
        for star in self.back_stars + self.mid_stars + self.front_stars:
            star.draw(surface)
