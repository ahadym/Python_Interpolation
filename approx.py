import pygame
import functools

SCREEN_WIDTH = 1640
SCREEN_HEIGHT = 980
DISPLAY_FORMULA = False

def newton(points, formula, x):
  """
    Using Newton's method, interpol the points present in the 'points' list
      and return the value of the polynom at point x.
  """

  if DISPLAY_FORMULA and not formula:
    formula_get = True
    formula.append('Newton :\n')
  else:
    formula_get = False

  res = 0.0
  array = []

  for j in xrange(0, len(points)):
    array.append([0.0] * (len(points) + 1))
    array[j][0] = float(points[j][0])
    array[j][1] = float(points[j][1])

  res += array[0][1]
  tmp = x - array[0][0]

  if formula_get:
    formula.append(str(res))
    formula.append(' + ')
    formula.append('(x - ' + str(array[0][0]) + ')')

  for i in xrange(2, len(points) + 1):
    for j in xrange(0, len(points) - i + 1):
      try:
        array[j][i] = float(array[j + 1][i - 1] - array[j][i - 1])            \
          / float(array[j + i - 1][0] - array[j][0])
      except:
        pass
    if formula_get:
      formula.append(' * ')
      formula.append(str(array[0][i]))
      formula.append(' + ')
      formula.append(formula[-4] + '(x - ' + str(array[i - 1][0]) + ')')
    res += tmp * array[0][i]
    tmp *= x - array[i - 1][0]

  return res



def lagrange(points, formula, x):
  """
    Using Lagrange's method, interpol the points present in the 'points' list
    and return the value of the polynom at point x.
  """

  if DISPLAY_FORMULA and not formula:
    formula_get = True
    formula.append('Lagrange :\n')
  else:
    formula_get = False

  res = 0.0

  for i in xrange(0, len(points)):
    tmp = float(points[i][1])
    for j in xrange(0, len(points)):
      if i == j:
        continue
      try:
        tmp *= float(x - points[j][0]) / float(points[i][0] - points[j][0])
        if formula_get:
          formula.append('(x - ' + str(points[j][0]) + ') / ('                \
              + str(points[i][0]) + ' - ' + str(points[j][0]) + ')')
          formula.append(' + ')
      except:
        pass
    res += tmp

  if formula_get:
    del formula[-1]

  return int(res)




def interpol(points, method):
  """
    Using the interpolation, build the set of points to draw
  """

  result = []
  formula = []
  points_compute = functools.partial(method, points, formula)

  for i in xrange(0, SCREEN_WIDTH, 2):
    result.append((i, points_compute(i)))

  if formula:
    print ''.join(formula)
  return result



def main():

  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  running = 1

  points = []
  changed = True
  l1 = []
  l2 = []


  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = 0
      elif event.type == pygame.MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        points.append((x, y))
        changed = True
        if len(points) > 1:
          l1 = interpol(points, lagrange)
          l2 = interpol(points, newton)
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        running = 0

    if changed:

      screen.fill((0, 0, 0))
      pygame.draw.aaline(screen, (100, 0, 0), (0, SCREEN_HEIGHT / 2), (SCREEN_WIDTH, SCREEN_HEIGHT / 2), 1)
      pygame.draw.aaline(screen, (100, 0, 0), (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT), 1)
      for p in points:
        rect = pygame.Rect(p[0] - 5, p[1] - 5, 10, 10)
        pygame.draw.rect(screen, (0, 0, 255), rect, 4)
      if len(l1) > 1 and len(l2) > 1:
        pygame.draw.aalines(screen, (0, 255, 0), False, l1, 1)
        pygame.draw.aalines(screen, (255, 0, 0), False, l2, 1)
      pygame.display.flip()
      changed = False


if __name__ == '__main__':
  main()
