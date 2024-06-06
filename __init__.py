import torch
import numpy as np
from PIL import Image

class SpriteSheetCutter:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "columns": ("INT", {"default": 4, "min": 1, "max": 20, "step": 1}),
                "rows": ("INT", {"default": 4, "min": 1, "max": 20, "step": 1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "cut_sprite_sheet"

    CATEGORY = "postprocessing/SpriteSheet"

    def cut_sprite_sheet(self, image: torch.Tensor, columns: int, rows: int):
        batch_size, height, width, channels = image.shape
        sprite_width = width // columns
        sprite_height = height // rows

        sprites = []

        for b in range(batch_size):
            img_b = image[b].numpy() * 255.0  # Convert to 0-255 range
            img_b = img_b.astype(np.uint8)  # Ensure the type is correct
            print(f"Processing batch {b}, image shape: {img_b.shape}")

            for row in range(rows):
                for col in range(columns):
                    left = col * sprite_width
                    upper = row * sprite_height
                    right = left + sprite_width
                    lower = upper + sprite_height

                    sprite = img_b[upper:lower, left:right, :]
                    sprites.append(sprite)

        sprites = np.stack(sprites)
        sprites_tensor = torch.tensor(sprites).float() / 255.0

        print(f"Sprites tensor shape: {sprites_tensor.shape}")

        return (sprites_tensor,)


NODE_CLASS_MAPPINGS = {
    "SpriteSheetCutter2": SpriteSheetCutter
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "SpriteSheetCutter2": "Cesarkon_SpriteSheetCutter! anyone who uses this node is gay"
}
