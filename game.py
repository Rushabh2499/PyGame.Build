import os
import pygame
import random
import math
import time
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((860, 540))
#bgmusic
mixer.music.load('bgmusic.wav')
mixer.music.play(-1)

#bgimg load
background = pygame.image.load('bgimg.jpg')
background = pygame.transform.scale(background,(800,600))

pygame.display.set_caption('May The Force Be With You')

icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#createPlayer
player_Img = pygame.image.load('ppl.png')
player_Img = pygame.transform.scale(player_Img,(100,100))
playerX = 370
playerY = 440
playerX_change = 0

#createEnemy
enemy_Img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8
nmyimg = pygame.image.load('ufo.png')
nmyimg = pygame.transform.scale(nmyimg,(120,75))

for i in range(num_of_enemies):
	enemy_Img.append(nmyimg)
	enemyX.append(random.randint(0,736))
	enemyY.append(random.randint(50,150))
	enemyX_change.append(3)
	enemyY_change.append(40)

#createBullet
bullet_Img = pygame.image.load('bullet.png')
bullet_Img = pygame.transform.scale(bullet_Img,(30,40))

bulletX = 0
bulletY = 440
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#score
score_val = 0
font = pygame.font.Font('freesansbold.ttf', 36)
textX = 10
textY = 10

#gameover
gameover_font = pygame.font.Font('freesansbold.ttf', 100)


#playerfn
def player(x,y):
	#blit means draw img on scrn
	screen.blit(player_Img, (x,y))

#enemyfn
def enemy(x,y):
	#blit means draw img on scrn
	screen.blit(enemy_Img[i], (x,y))


#bulletfn
def fire_bullet(x,y):

	global bullet_state
	bullet_state = "fire"

	screen.blit(bullet_Img,(x+36,y-16))

#collision_detect
def isCollision(enemyX,enemyY,bulletX,bulletY):
	distance=math.sqrt((math.pow(enemyX-bulletX,2)) +  (math.pow(enemyY-bulletY,2)))

	if distance < 27:
		return True
	else:
		return False 

def show_score(x,y):
	score = font.render("Score: "+ str(score_val), True, (255,255,255))
	screen.blit(score, (x,y))

def game_over():
	
	for j in range(num_of_enemies):
		enemyY[j] = 2000
	gameover_text = gameover_font.render("GAME OVER",True, (255,20,20))
	screen.blit(gameover_text,(100,250))
	end_sound = mixer.Sound('end.wav')
	end_sound.play(0)
	time.sleep(2)
	end_sound = mixer.Sound('gameover.wav')
	end_sound.play(0)




#main game loop
running = True
while running:

	#RGB format
	screen.fill((0,0,0))

	#bgimg
	screen.blit(background,(0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -3
			if event.key == pygame.K_RIGHT:
				playerX_change = 3
			if event.key == pygame.K_SPACE:
				if bullet_state == "ready":
					#load bullet fire sound
					bullet_sound = mixer.Sound('fire.wav')
					#play sound
					bullet_sound.play()

					bulletX = playerX
					fire_bullet(bulletX, bulletY)

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change =0


	#playerMove
	playerX += playerX_change

	if playerX <= 0:
		playerX = 0
	elif playerX >= 800:
		playerX = 800


	#enemyMove
	for i in range(num_of_enemies):
		if enemyY[i] > 400:
			game_over()
			time.sleep(2)
			break

		enemyX[i] += enemyX_change[i]

		if enemyX[i] <= 0:
			enemyX_change[i] = 3
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= 800:
			enemyX_change[i] = -3
			enemyY[i] += enemyY_change[i]


		#collisionDetection
		collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
		if collision:
			hit_sound = mixer.Sound('hit.wav')
			hit_sound.play()
			bulletY = 440
			bullet_state = "ready"
			score_val += 1
			print(score_val)

			#respawn the enemy
			enemyX[i] = random.randint(0, 800)
			enemyY[i] = random.randint(50, 150)

		enemy(enemyX[i], enemyY[i])

	#bulletmove
	if bulletY <= 0:
		bulletY = 440
		bullet_state = "ready"

	if bullet_state == "fire":
		fire_bullet(bulletX, bulletY)
		bulletY -= bulletY_change


	player(playerX, playerY)
	show_score(textX,textY)


	#updateScreen
	pygame.display.update()

pygame.quit()




