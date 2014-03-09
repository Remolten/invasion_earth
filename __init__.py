import platform
import os
import sys
import pygame

def find_os():
    #Returns the OS name
    OS = platform.system()
    return OS

def find_resolution(OS):
    #Put in default values if we're on unsupported OS
    max_screen_size_x = 800
    max_screen_size_y = 600

    print('Looking for max screen resolution and an operating system...')

    #Find the system's max resolution
    if OS == 'Windows':
        try:
            import ctypes
            user32 = ctypes.windll.user32
            max_screen_size_x = user32.GetSystemMetrics(0)
            max_screen_size_y = user32.GetSystemMetrics(1)
            print('Your max screen resolution is %d, %d.' % (max_screen_size_x,
                                                        max_screen_size_y))
            print("You're running a supported version of Windows.")
        except:
            print("This isn't a supported Windows version.")

    elif OS == 'Mac OS' or OS == 'Mac OSX':
        #Not sure if Mac OSX return just OS or OSX
        print(OS)
        try:
            #Untested, only takes the first screen passed to it
            import AppKit
            for screen in AppKit.NSScreen.screens():
                max_screen_size_x = screen.frame().size.width
                max_screen_size_y = screen.frame().size.height
                break
            print('Your max screen resolution is %d, %d' % (max_screen_size_x,
                                                            max_screen_size_y))
            print("You're running a supported version of Mac OSX.")
        except:
            print("This isn't a supported Mac OSX version.")
            
    elif OS == 'Linux' or 'Unix':
    	try:
    		screen = os.popen('xrandr -q -d :0')
    		screen = screen.readlines()[0]
    		max_screen_size_x = int(screen.split()[7])
    		max_screen_size_y = int(screen.split()[9][:-1])
    		print('Your max screen resolution is %d, %d' % (max_screen_size_x, 
    														max_screen_size_y))
    		print("You're running a supported version of Linux/Unix.")
    	except:
    		print("This isn't a supported Linux/Unix version.")

    else:
    	#This hack should make the game work on all other OS's
        print("Couldn't find %d in the supported OS's.  The game will still attempt to "
              "run." % OS)
        pygame.init()
        pygame.display.set_mode((max_screen_size_x, max_screen_size_y), FULLSCREEN)
        max_screen_size_x = pygame.display.Info().currentw
        max_screen_size_y = pygame.display.Info().currenth
        pygame.quit()
        
    return max_screen_size_x, max_screen_size_y

def set_resolution(max_screen_size_x, max_screen_size_y):
	#Make sure we don't go over the maximum resolution
	if max_screen_size_x > 2000:
		print("You'll have to live with the resolution; the game can't "
              "scale any larger to fit your screen.")
    	screen_size_x = 2000
 
	if max_screen_size_y > 1500:
		print("You'll have to live with the resolution; the game can't "
              "scale any larger to fit your screen.")
        screen_size_y = 1500 
              
    #We figure out the closest supported display type to the maximum possible one
	if max_screen_size_x < 800 or max_screen_size_y < 600:
		sys.exit('Screen is too small to display the game properly.  Please get '
                 'a better resolution screen :D')
                       
	if screen_size_x != 2000 and screen_size_y != 1500:
        #Lambda is a hack to create a temporary function to work with min()
		screen_size_x = min([800, 1000, 1200, 1400, 1600, 1800, 2000],
                            key = lambda x:abs(x - max_screen_size_x))
        #Make sure the closest one isn't higher than the max plus some padding
        while screen_size_x >= max_screen_size_x:
            screen_size_x -= 200
        #Determine y by using the fact we are keeping the ratio at 4:3
        screen_size_y = screen_size_x * 3 / 4
        #Make sure the closest one isn't higher than the max plus some padding
        while screen_size_y >= max_screen_size_y:
            screen_size_y -= 200
            
	return screen_size_x, screen_size_y

def set_position(max_screen_size_x, screen_size_x):
    #Works on Windows
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%d, %d' % ((max_screen_size_x -
                                                      screen_size_x)  / 2, 30)
    #Will center the screen
    #Could use on platforms that don't work with above
    #os.environ['SDL_VIDEO_CENTERED'] = '1'
