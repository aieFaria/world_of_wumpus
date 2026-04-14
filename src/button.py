import pygame

class Button():
	def __init__(self, image, pos, text_input="", font="qa", base_color="#000000", hovering_color="#000000"):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		if font is None or isinstance(font, str):
			self.font = pygame.font.SysFont("Arial", 20) # Tamanho 20 por padrão
		else:
			self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
		self.copia = self.image.copy()
		self.image_destaque = self.image.copy()
		self.image_destaque.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

	def changeImage(self, position, image):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.image = image

	def changeColorImagem(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.image = self.image_destaque.copy()
			# print("aqui")
		else:
			self.image = self.copia.copy()