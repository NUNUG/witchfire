#import pygame
from pygame.locals import *

class KonamiKode:
	def __init__(self, konami_kode_func):
		self._konami_kode_func = konami_kode_func
		self._last9 = []
		self.clear_previous_states()
		self.the_konami_kode = [K_UP, K_UP, K_DOWN, K_DOWN, K_LEFT, K_RIGHT, K_LEFT, K_RIGHT, K_SPACE]
		pass
	def clear_previous_states(self):
		self._last_up = False
		self._last_down = False
		self._last_left = False
		self._last_right = False
		self._last_space = False

	def capture(self, keystates):
		if keystates[K_UP] or keystates[K_KP8]:
			self.capture_down(K_UP)
		else:
			self.capture_up(K_UP)
		if keystates[K_DOWN] or keystates[K_KP2]:
			self.capture_down(K_DOWN)
		else:
			self.capture_up(K_DOWN)
		if keystates[K_LEFT] or keystates[K_KP4]:
			self.capture_down(K_LEFT)
		else:
			self.capture_up(K_LEFT)
		if keystates[K_RIGHT] or keystates[K_KP6]:
			self.capture_down(K_RIGHT)
		else:
			self.capture_up(K_RIGHT)
		if keystates[K_SPACE]:
			self.capture_down(K_SPACE)
		else:
			self.capture_up(K_SPACE)

	def capture_up(self, keyboard_kode):
		if keyboard_kode == K_UP and (self._last_up):
			self._last_up = False
		if keyboard_kode == K_DOWN and (self._last_down):
			self._last_down = False
		if keyboard_kode == K_LEFT and (self._last_left):
			self._last_left = False
		if keyboard_kode == K_RIGHT and (self._last_right):
			self._last_right = False
		if keyboard_kode == K_SPACE and (self._last_space):
			self._last_space = False

	def capture_down(self, keyboard_kode):
		#print("Last9: ", self._last9)
		#print("konkd: ", self.the_konami_kode)
		#print("")
		if (keyboard_kode == K_UP and (not self._last_up)):
			self._last9.append(K_UP)
			self.clear_previous_states()
			self._last_up = True
		if (keyboard_kode == K_DOWN and (not self._last_down)):
			self._last9.append(K_DOWN)
			self.clear_previous_states()
			self._last_down = True
		if (keyboard_kode == K_LEFT and (not self._last_left)):
			self._last9.append(K_LEFT)
			self.clear_previous_states()
			self._last_left = True
		if (keyboard_kode == K_RIGHT and (not self._last_right)):
			self._last9.append(K_RIGHT)
			self.clear_previous_states()
			self._last_right = True
		if (keyboard_kode == K_SPACE and (not self._last_space)):
			self._last9.append(K_SPACE)
			self.clear_previous_states()
			self._last_space = True
		
		if(len(self._last9) > 9):
			self._last9 = self._last9[-9:]

		if (self._last9 == self.the_konami_kode):
			print("Konami Kode Detected!")
			self._konami_kode_func()
			self._last9 = []
