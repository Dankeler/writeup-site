{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Initial thoughts", "initial-thoughts")}}

{{text("The challange supplies us with a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>MyNokiaBroke.jar</code>. Since the challange name contains the word <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Nokia</code>, and the description mentions this is a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>MIDlet</code> app, we can expect this to be a mobile application.")}}

{{header("Reverse engineering", "reverse-engineering")}}

{{text("First thing I tried is searching for some kind of <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>java decompiler</code> tool online that might help me understand this file better.")}}

{{link("https://www.decompiler.com/", "https://www.decompiler.com/favicon.ico", "Java Decompiler Tool Online")}}

{{text("After uploading the file to the mentioned site, I saw three files.")}}

{{image("../../static/writeups/mynokiabroke/images/000001.jpg")}}

{{text("The <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>MANIFEST.MF</code> won't be useful to us, but the other two probably will.")}}

{{text("Next file, <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>AppMIDlet.java</code> contains the program logic, asking for a password, inputting it, validating it and displaying something if the password is correct.")}}

{{console("if (command == PASSWD_COMMAND && this.textField.getString().equals(\"This is a very long password OoOOoOOOoOOOoOOOoOoOooOooooOOOoo\"))", "")}}

{{text("This line is the most important, it checks if the inputted password equals <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>This is a very long password OoOOoOOOoOOOoOOOoOoOooOooooOOOoo</code> and if it does, it displays the graphics that are defined in the other file, <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>FlagCanvas.java</code>.")}}

{{text("The rendered graphic is probably the flag, so we can either run the app, input the correct password and get the flag this way, or try to read the flag from the last file.")}}

{{text("I prefer the latter approach, so let's try to read the last file.")}}

{{image("../../static/writeups/mynokiabroke/images/000002.jpg")}}

{{text("It simply draw a couple of things on the screen, which is probably our flag.")}}

{{header("Getting the flag", "getting-the-flag")}}

{{text("We can recreate this function in python and get the flag.")}}

{{console("import pygame
import sys

pygame.init()

width, height = 200, 200
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(\"Flag Drawing\")

RED = (255, 0, 0)

def draw_flag():
screen.fill((255, 255, 255))
pygame.draw.line(screen, RED, (140, 10), (160, 10))
pygame.draw.line(screen, RED, (110, 130), (110, 170))
pygame.draw.line(screen, RED, (50, 130), (50, 170))
pygame.draw.line(screen, RED, (10, 110), (30, 110))
pygame.draw.line(screen, RED, (105, 50), (120, 10))
pygame.draw.line(screen, RED, (180, 130), (180, 170))
pygame.draw.line(screen, RED, (50, 110), (70, 110))
pygame.draw.line(screen, RED, (20, 70), (20, 110))
pygame.draw.line(screen, RED, (160, 50), (160, 10))
pygame.draw.line(screen, RED, (90, 10), (105, 50))
pygame.draw.line(screen, RED, (50, 10), (70, 10))
pygame.draw.line(screen, RED, (10, 10), (30, 10))
pygame.draw.line(screen, RED, (120, 50), (120, 10))
pygame.draw.line(screen, RED, (150, 130), (150, 170))
pygame.draw.line(screen, RED, (140, 50), (160, 50))
pygame.draw.line(screen, RED, (10, 130), (30, 130))
pygame.draw.line(screen, RED, (90, 170), (110, 170))
pygame.draw.line(screen, RED, (50, 70), (50, 90))
pygame.draw.line(screen, RED, (30, 150), (20, 150))
pygame.draw.line(screen, RED, (30, 150), (30, 170))
pygame.draw.line(screen, RED, (90, 150), (110, 150))
pygame.draw.line(screen, RED, (50, 150), (70, 170))
pygame.draw.line(screen, RED, (20, 10), (20, 50))
pygame.draw.line(screen, RED, (140, 30), (160, 30))
pygame.draw.line(screen, RED, (20, 50), (10, 50))
pygame.draw.line(screen, RED, (70, 90), (70, 110))
pygame.draw.line(screen, RED, (50, 70), (70, 70))
pygame.draw.line(screen, RED, (170, 130), (190, 130))
pygame.draw.line(screen, RED, (50, 25), (50, 50))
pygame.draw.line(screen, RED, (10, 170), (30, 170))
pygame.draw.line(screen, RED, (10, 170), (10, 130))
pygame.draw.rect(screen, RED, (50, 130, 20, 20), 1)
pygame.draw.line(screen, RED, (90, 130), (110, 130))
pygame.draw.line(screen, RED, (70, 10), (70, 25))
pygame.draw.line(screen, RED, (150, 150), (130, 150))
pygame.draw.line(screen, RED, (50, 25), (70, 25))
pygame.draw.line(screen, RED, (10, 90), (20, 70))
pygame.draw.line(screen, RED, (90, 10), (90, 50))
pygame.draw.line(screen, RED, (130, 130), (130, 150))
pygame.draw.line(screen, RED, (70, 90), (50, 90))
pygame.draw.line(screen, RED, (50, 50), (70, 50))
pygame.display.flip()

draw_flag()

while True:
for event in pygame.event.get():
if event.type == pygame.QUIT:
pygame.quit()
sys.exit()", "")}}

{{text("Now we get a window with our flag.")}}

{{image("../../static/writeups/mynokiabroke/images/000003.jpg")}}

{{script()}}