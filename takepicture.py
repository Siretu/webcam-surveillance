import pygame.camera, pygame.image
import sys


def capture(name):
    #print "Capturing image into %s" % name
    pygame.camera.init()
    cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
    #print pygame.camera.list_cameras()
    cam.start()
    img = cam.get_image()
    pygame.image.save(img,name)
    pygame.camera.quit()

if __name__ == "__main__":
    capture(sys.argv[1])
