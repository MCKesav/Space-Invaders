from pygame import *
from os import *
# a = input()
font.init()
mixer.init()


#diaplay
WIDTH, HEIGHT = 900, 700

WIN = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Space Invaders")
icon = image.load(path.join('Assets', 'icon.png'))
display.set_icon(icon)

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 238)
DARK_CYAN = (0, 107, 100)

# black line
BORDER = Rect(WIDTH / 2 - 5, 0, 10, HEIGHT)

#sound
BULLET_FIRE_SOUND = mixer.Sound(path.join('Assets', 'bulletfiresound.mp3'))
BULLET_HIT_SOUNT = mixer.Sound(path.join('Assets', 'gunhitsound.mp3'))

#adding text
HEALTH_FONT = font.SysFont("Bradley Hand ITC", 45, True)
WINNER_FONT = font.SysFont("Bradley Hand ITC", 120, True)
SPACESHIP_SIZE = (65, 45)


FPS = 60
vel = 5
bullets_vel = 7
max_bullets = 3

# health values
player1_health = 10  # TODO
player2_health = 10  # TODO
health_swap_value = 0  # TODO


YELLOW_HIT = USEREVENT + 1
RED_HIT = USEREVENT + 2

#images
YELLOW_SPACESHIP_IMG = image.load(path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = transform.rotate(
    transform.scale(YELLOW_SPACESHIP_IMG, SPACESHIP_SIZE), 90)
RED_SPACESHIP_IMG = image.load(path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = transform.rotate(
    transform.scale(RED_SPACESHIP_IMG, SPACESHIP_SIZE), 270)



def bg_changer(bg):
  space = transform.scale(image.load(path.join('Assets', f's{bg}.webp')),(WIDTH, HEIGHT))
  WIN.blit(space, (0, 0))

def draw_window(red, yellow, red_bullets, yellow_bullets, player1_health,player2_health, bg):

  bg_changer(bg)
  draw.rect(WIN, BLACK, BORDER)

# displaying health
  player1_text = HEALTH_FONT.render("Health : " + str(player1_health), 1,WHITE)
  player2_text = HEALTH_FONT.render("Health : " + str(player2_health), 1,WHITE)
  WIN.blit(player2_text, (WIDTH - player2_text.get_width() - 10, 7))
  WIN.blit(player1_text, (10, 10))

  #displaying spaceship
  WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
  WIN.blit(RED_SPACESHIP, (red.x, red.y))

  #displaying bullets
  for bullet in red_bullets:
    draw.rect(WIN, RED, bullet)

  for bullet in yellow_bullets:
    draw.rect(WIN, YELLOW, bullet)

  display.update()


def yellow_keys_movements(key_pressed, yellow):
  if key_pressed[K_a] and (yellow.x - vel + 4 > 0):
    yellow.x -= vel
  if key_pressed[K_d] and (yellow.x + vel + yellow.width - 4 < BORDER.x):
    yellow.x += vel
  if key_pressed[K_w] and (yellow.y - vel - 50 > 0):
    yellow.y -= vel
  if key_pressed[K_s] and (yellow.y + vel + yellow.height - 4 < HEIGHT):
    yellow.y += vel


def red_keys_movements(key_pressed, red):
  if key_pressed[K_LEFT] and (red.x - vel + 4 > BORDER.x + BORDER.width):
    red.x -= vel
  if key_pressed[K_RIGHT] and (red.x + vel + red.width - 4 < WIDTH):
    red.x += vel
  if key_pressed[K_UP] and (red.y - vel - 50 > 0):
    red.y -= vel
  if key_pressed[K_DOWN] and (red.y + vel + red.height - 4 < HEIGHT):
    red.y += vel


def handle_bullets(yellow_bullets, red_bullets, yellow, red):

  for bullet in yellow_bullets:
    bullet.x += bullets_vel

    #detect collisions
    if red.colliderect(bullet):
      event.post(event.Event(RED_HIT))
      yellow_bullets.remove(bullet)

    elif bullet.x > WIDTH:
      yellow_bullets.remove(bullet)

  for bullet in red_bullets:
    bullet.x -= bullets_vel

    #detecting collisions
    if yellow.colliderect(bullet):
      event.post(event.Event(YELLOW_HIT))
      red_bullets.remove(bullet)

    elif bullet.x < 0:
      red_bullets.remove(bullet)


def draw_winner(text):
  draw_winner_text = WINNER_FONT.render(text, 1, WHITE)
  WIN.blit(draw_winner_text, (WIDTH / 2 - draw_winner_text.get_width() / 2, HEIGHT / 2 - draw_winner_text.get_height() / 2))
  display.update()
  time.delay(5000)

#cheatcode for reset
def reset(bg, health_reset_value1, health_reset_value2):  # TODO
  global player1_health
  global player2_health
  global health_swap_value
  if player1_health > 10:
    player1_health = 10
  if player2_health > 10:
    player2_health = 10
  if health_swap_value & 1 == 1:
    player1_health, player2_health = player2_health, player1_health
    health_swap_value -= 1
  if health_reset_value1 == 1:
    player1_health -= 5
  if health_reset_value2 == 1:
    player2_health -= 5
  bg_changer(0)


def main():

  bg = 0
  if bg == 0:
    bg_changer(0)

  red = Rect(675 - SPACESHIP_SIZE[0] / 2, 300, SPACESHIP_SIZE[0] - 17,SPACESHIP_SIZE[1] + 20)
  yellow = Rect(450 / 2 - SPACESHIP_SIZE[0] / 2, 300, SPACESHIP_SIZE[0] - 17,SPACESHIP_SIZE[1] + 20)
  
  red_bullets = []
  yellow_bullets = []
  health_reset_value1 = 0
  health_reset_value2 = 0

  vel = 5
  bullets_vel = 7
  max_bullets = 3

  global player1_health  # TODO
  global player2_health  # TODO
  global health_swap_value  # TODO

  clock = time.Clock()
  run = True

  #running loop
  while run:
    clock.tick(FPS)

    for evt in event.get():
      if evt.type == QUIT:
        run = False

      if evt.type == KEYDOWN:

        if evt.key == K_LCTRL and len(yellow_bullets) < max_bullets:
          bullet = Rect(yellow.x + yellow.width,yellow.y + yellow.height / 2 - 2, 10, 5)
          yellow_bullets.append(bullet)
          BULLET_FIRE_SOUND.play()

        if evt.key == K_RCTRL and len(red_bullets) < max_bullets:
          bullet = Rect(red.x, red.y + red.height / 2 - 2, 10, 5)
          red_bullets.append(bullet)
          BULLET_FIRE_SOUND.play()

        # Cheat Codes  
        if evt.key == K_1:
          player1_health += 5
          if player1_health < 10 and player1_health - 5 != 0:
            health_reset_value1 = 1
          else:
            health_reset_value1 = 0
        if evt.key == K_0:
          player2_health += 5
          if player2_health < 10 and player2_health - 5 != 0:
            health_reset_value2 = 1
          else:
            health_reset_value1 = 0
        if evt.key == K_2 and player2_health - 5 > 0:
          player2_health -= 5
        if evt.key == K_9 and player1_health - 5 > 0:
          player1_health -= 5
        if evt.key == K_h:
          health_swap_value += 1
          player1_health, player2_health = player2_health, player1_health
        if evt.key == K_b:
          if bg == 5:
            bg = 0
            bg_changer(0)
          else:
            bg += 1
            bg_changer(bg)
        if evt.key == K_r:
          bg = 0
          reset(bg, health_reset_value1, health_reset_value2)

      #deducting health
      if evt.type == YELLOW_HIT:
        player1_health -= 1
        BULLET_HIT_SOUNT.play()
      if evt.type == RED_HIT:
        player2_health -= 1
        BULLET_HIT_SOUNT.play()

    #display winner
    winner_text = ''
    if player1_health <= 0:
      winner_text = "Player 2 wins"
    if player2_health <= 0:
      winner_text = "Player 1 wins"
    if winner_text != '':
      draw_winner(winner_text)
      break

    key_pressed = key.get_pressed()
    yellow_keys_movements(key_pressed, yellow)
    red_keys_movements(key_pressed, red)
    handle_bullets(yellow_bullets, red_bullets, yellow, red)
    draw_window(red, yellow, red_bullets, yellow_bullets, player1_health,player2_health, bg)


if __name__ == "__main__":
  main()