def setup():
    global bg, stageNum, winbg, losebg, startScreen, instructionsScreen
    global gun, gunX, gunY, gunW, gunH, gunfire
    global rocks, totalRocks, rockX, rockY, rock_dy, rockW, rockH
    global ammo, maxAmmo, worldHealth, maxHealth
    global isFiring, rockHit, damage
    global rockTypes
    global startTime, gameTime, gameWon, gameStarted, gameActive
    global rockBroken, breakingRocks

    size(1000, 800)
    stageNum = 0  #startscreen
    totalRocks = 6
    gameStarted = False
    gameActive = False

    #load images
    bg = loadImage("bg.png")
    winbg = loadImage("winbg.png")
    losebg = loadImage("losebg.png")
    startScreen = loadImage("startScreen.png")
    instructionsScreen = loadImage("instructions.png")
    gun = loadImage("gun.png")
    gunfire = loadImage("gunfire.png")

    #gun position
    gunX, gunY = width * 0.25, height * 0.67
    gunW, gunH = width * 0.07, height * 0.25

    #initialize ammo and world health
    maxAmmo = 45
    ammo = maxAmmo
    maxHealth = 45
    worldHealth = maxHealth
    damage = 2 #damage when a rock hits the bottom

    #timer variables
    startTime = millis()
    gameTime = 100000 # 100 seconds
    gameWon = False

    #lists for rocks
    rocks = []
    rockW = []
    rockH = []
    rockX = []
    rockY = []
    rock_dy = []
    rockHit = []
    rockTypes = []

    for i in range(totalRocks):
        scale = random(0.05, 0.09)
        rocks.append(loadImage("rock"+str(i)+".png"))
        rockW.append(rocks[i].width * scale)
        rockH.append(rocks[i].height * scale)
        rockX.append(random(width-200))
        rockY.append(random(-300, -50))
        rock_dy.append(random(6, 8))
        rockHit.append(False)
        rockTypes.append(i) #store the rock type 0 to 5

    rockBroken = [] #just for collecting broken rock
    for i in range(6):
        rockBroken.append(loadImage("rockb" + str(i) + ".png"))
    breakingRocks = [] #to store data for actual breaking{x, y, w, h, type, timer}

    isFiring = False

    checkOverlap(i)

def draw():
    global ammo, worldHealth, isFiring, rockX, rockY, rockHit, gameWon, stageNum
    
    #game stages
    if stageNum == 0:
        displayStartScreen() #start
    elif stageNum == 1:
        displayInstructionsScreen() #instr
    elif stageNum == 2:
        drawGameplay() #gameplay

def drawGameplay():
    global ammo, worldHealth, isFiring, rockX, rockY, rockHit, gameWon, gameActive
    
    #check if timer has elapsed for win condition
    if not gameWon and millis() - startTime >= gameTime:
        gameWon = True
        gameActive = False #timer stop
    
    #show victory screen if player has won
    if gameWon:
        displayVictoryScreen()
        return
    
    #game lose check
    if worldHealth<=0 or ammo<=0:
        gameActive = False
        displayGameOverScreen()
        return #skip rest draw function
    gameActive = True #timer only continues if gameactive
    
    #normal game draw
    image(bg, 0, 0, width, height)
    drawBars()
    drawEnduranceClock()

    #draw all breaking rocks
    drawBreakingRocks()

    for i in range(totalRocks):
        #only draw and update rocks that havent been hit
        if not rockHit[i]:
            image(rocks[i], rockX[i], rockY[i], rockW[i], rockH[i])
            rockY[i]+=rock_dy[i]

            #check if rock hits bottom
            if rockY[i]>=height: #reduce world health
                worldHealth -= damage
                worldHealth = max(0,worldHealth)
                resetRock(i) #reset position of rock

            if isFiring and rockGunPath(i):
                rockHit[i] = True
                
                #add breaking rock animation
                addBreakingRock(rockX[i], rockY[i], rockW[i], rockH[i], rockTypes[i])

                #check if it's blue rock(rock0) or red rock(rock1) and increase ammo
                if rockTypes[i] == 0: #blue
                    increaseAmmo(2) #increases ammo 
                elif rockTypes[i] == 1: #red
                    increaseAmmo(2) #increases ammo
                resetRock(i)
    
    #draw gun
    if isFiring: #fire gun
        image(gunfire, gunX, gunY - gunH * 0.2, gunW, gunH * 1.4)
        isFiring = False #reset firing state immediately
    else: #normal gun
        image(gun, gunX, gunY, gunW, gunH)

def addBreakingRock(x, y, w, h, rockType):
    global breakingRocks
    #x,y,w,h are for position of rock and rockType for type(0-5)
    #reate a new breaking rock with position, size, type and timer
    breakingRocks.append({
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'type': rockType,
        'timer': 10 #show for 10 frames
    })

def drawBreakingRocks():
    #draw all breaking rocks and update their timers and remove whose timers have expired
    global breakingRocks, rockBroken

    #process each breaking rock
    i = 0
    while i < len(breakingRocks):
        rock = breakingRocks[i]

        #draw the broken rock
        image(rockBroken[rock['type']], rock['x'], rock['y'], rock['w'], rock['h'])

        #decrease the timer
        rock['timer'] -= 1

        #if timer reaches zero, remove this rock
        if rock['timer'] <= 0:
            del breakingRocks[i]
        else:
            i += 1

def drawEnduranceClock():
    global gameStarted, startTime, gameActive
    
    if gameStarted and gameActive: #only count time when both are true
        timeElapsed = int((millis() - startTime) / 1000)
    else:
        timeElapsed = 0
        
    textX = width - (width * 0.06)
    textY = height * 0.5
    # Draw time value text
    fill(0,0,130)
    textSize(width * 0.019)
    textAlign(CENTER, CENTER)
    text("ENDURANCE \n CLOCK: " + str(timeElapsed) + "s", textX, textY)

def increaseAmmo(amount):
    #function to increase ammo with stop at maxAmmo
    global ammo, maxAmmo
    ammo = min(ammo + amount, maxAmmo)

def resetRock(i):
    global rockX, rockY, rock_dy, rockHit, rockTypes
    rockY[i] = random(-200, -100)
    rockX[i] = random(width-200)
    rock_dy[i] = random(4, 10)
    rockHit[i] = False

    randVal = random(100)

    if randVal < 10: #10% chance for blue(rock0)
        rockTypes[i] = 0
    elif randVal < 20: 
        rockTypes[i] = 1
    else: #80% chance for other rocks(2-5)
        rockTypes[i] = int(random(2, 6))

    #update the rock image
    rocks[i] = loadImage("rock"+str(rockTypes[i])+".png")
    checkOverlap(i)

def rockGunPath(rockIndex):
    global rockX, rockY, rockW, rockH, gunX, gunW
    gun_center = gunX+(gunW/2) #firing path directly above gun

    #allow some tolerance in the hit detection
    tolerance = gunW*0.75
    return (rockX[rockIndex] < gun_center + tolerance/2 and
            rockX[rockIndex] + rockW[rockIndex] > gun_center - tolerance/2)

def drawBars():
    barW = width * 0.03
    barH = height * 0.275 
    barGap = width * 0.055 
    barX = width - (width * 0.047) 
    barY = height * 0.025

    #ammo bar(blue)
    noStroke()
    fill(0, 120, 250)
    rect(barX - barGap, barY + barH * (1 - float(ammo)/maxAmmo),
         barW, barH * (float(ammo)/maxAmmo))

    #world health bar(yellow)
    fill(235, 235, 0)
    rect(barX, barY + barH * (1 - float(worldHealth)/maxHealth),
         barW, barH * (float(worldHealth)/maxHealth))

    #add numerical values
    textSize(width * 0.012)
    textAlign(CENTER, BOTTOM)
    fill(0,0,130)
    text(str(ammo), barX - barGap + barW/2, barY - 0.5)
    text(str(int(worldHealth)), barX + barW/2, barY - 0.5)

def checkOverlap(rockIndex):
    global rockX, rockY, rockW, rockH, totalRocks

    attempts = 0
    max_attempts = 10

    while attempts < max_attempts:
        overlap = False

        #check against all other rocks
        for j in range(totalRocks):
            if rockIndex != j: #to not compare with self
                #rectangle collision check
                if (rockX[rockIndex] < rockX[j] + rockW[j] and
                    rockX[rockIndex] + rockW[rockIndex] > rockX[j] and
                    rockY[rockIndex] < rockY[j] + rockH[j] and
                    rockY[rockIndex] + rockH[rockIndex] > rockY[j]):
                    overlap = True
                    break

        if not overlap:
            return #no overlap found

        #if overlap found generate new position
        rockX[rockIndex] = random(width-200)
        rockY[rockIndex] = random(-500, -50)
        attempts += 1

def keyPressed():
    global gunX, ammo, isFiring, stageNum
    
    if stageNum == 2:
        gunSpeed = width*0.05

        if keyCode == LEFT:
            gunX -= gunSpeed
        elif keyCode == RIGHT:
            gunX += gunSpeed
        elif key == ' ':
            if ammo>0:
                ammo -= 1
                isFiring = True #set firing state

        #gun within screen bounds by using constrain
        gunX = constrain(gunX, 0, width - gunW)

def displayStartScreen():
    image(startScreen, 0, 0, width, height) 
    drawBars()
    drawEnduranceClock()
    drawStartScreenButtons() #draw start and instructions buttons

def displayInstructionsScreen():
    image(instructionsScreen, 0, 0, width, height)
    drawBars()
    drawEnduranceClock()
    drawInstructionsScreenButtons()

def drawStartScreenButtons():
    rectMode(CENTER)
    buttonW = width * 0.3
    buttonH = height * 0.1
    cornerRadius = 25
    
    titleY = height * 0.3 
    buttonSpacing = height * 0.15 
    
    
    fill(255, 50, 50) #start button
    rect(width * 0.4, titleY + buttonSpacing, buttonW, buttonH, cornerRadius)
    fill(50, 50, 255)  #instructions button
    rect(width * 0.4, titleY + buttonSpacing*2, buttonW, buttonH, cornerRadius)

    #button text
    textSize(width * 0.03)
    fill(255)
    textAlign(CENTER, CENTER)
    text("START", width * 0.4, titleY + buttonSpacing)
    text("INSTRUCTIONS", width * 0.4, titleY + buttonSpacing*2)
    #reset rectMode for other 
    rectMode(CORNER)

def drawInstructionsScreenButtons():
    rectMode(CENTER)
    buttonW = width * 0.3
    buttonH = height * 0.1
    cornerRadius = 25

    fill(255, 50, 50) #start button
    rect(width/2, height * 0.8, buttonW, buttonH, cornerRadius)
    
    #button text
    textSize(width * 0.03)
    fill(255)
    textAlign(CENTER, CENTER)
    text("START GAME", width/2, height * 0.8)
    rectMode(CORNER)

def displayGameOverScreen():
    image(losebg, 0, 0, width, height)
    drawBars()
    drawEnduranceClock()
    drawGameButtons("ROCK & RELOAD!", "NOPE, I'M OUT!")

def displayVictoryScreen():
    image(winbg, 0, 0, width, height)
    drawBars()
    drawEnduranceClock()
    drawGameButtons("ROCK & RELOAD!", "NOPE, I'M OUT!")

def drawGameButtons(playAgainText, quitText):
    rectMode(CORNER)
    buttonW = width * 0.3
    buttonH = height * 0.1
    buttonY = height * 0.45
    cornerRadius = 25
    
    fill(255, 50, 50) #play again button
    rect(width/2 - buttonW - 100, buttonY, buttonW, buttonH, cornerRadius)
    
    fill(180, 40, 40) #quit button
    rect(width/2-20, buttonY, buttonW, buttonH, cornerRadius)
    
    textSize(width * 0.023) #buttons text
    fill(255)
    textAlign(CENTER, CENTER)
    text(playAgainText, width/2 - buttonW/2 - 100, buttonY + buttonH/2)
    text(quitText, width/2 + buttonW/2-20, buttonY + buttonH/2)

def mousePressed():
    global startTime, gameWon, worldHealth, ammo, maxAmmo, stageNum, gameStarted, gameActive
    #check which stages we're in
    if stageNum == 0:
        buttonW = width * 0.3
        buttonH = height * 0.1
        titleY = height * 0.3
        buttonSpacing = height * 0.15
        
        #start button clicked
        if (mouseX > width * 0.4 - buttonW/2 and 
            mouseX < width * 0.4 + buttonW/2 and
            mouseY > titleY + buttonSpacing - buttonH/2 and 
            mouseY < titleY + buttonSpacing + buttonH/2):
            stageNum = 2 #go to gameplay
            gameStarted = True  
            gameActive = True
            startTime = millis() #reset timer
            
        #instructions button clicked
        if (mouseX > width * 0.4 - buttonW/2 and 
            mouseX < width * 0.4 + buttonW/2 and
            mouseY > titleY + buttonSpacing*2 - buttonH/2 and 
            mouseY < titleY + buttonSpacing*2 + buttonH/2):
            stageNum = 1 #go to instructions
            startTime = millis() #reset timer
            
    elif stageNum == 1:
        #instructions screen button
        buttonW = width * 0.3
        buttonH = height * 0.1
        
        #start game button clicked
        if (mouseX > width/2 - buttonW/2 and mouseX < width/2 + buttonW/2 and
            mouseY > height * 0.8 - buttonH/2 and mouseY < height * 0.8 + buttonH/2):
            stageNum = 2 #go to gameplay
            gameStarted = True
            gameActive = True
            startTime = millis()  #reset timer when starting
            
    elif stageNum == 2:
        #check if game is over (victory or game over)
        if gameWon or worldHealth <= 0 or ammo <= 0:
            buttonW = width * 0.3
            buttonH = height * 0.1
            buttonY = height * 0.45

            #play again button clicked
            if (mouseX > width/2 - buttonW - 100 and mouseX < width/2 - 100 and
                mouseY > buttonY and mouseY < buttonY + buttonH):
                #reset game
                startTime = millis()
                gameStarted = True #reset
                gameActive = True
                gameWon = False
                worldHealth = maxHealth
                ammo = maxAmmo

                for i in range(totalRocks): #reset all rocks
                    resetRock(i)
                loop() #restart game loop

            #quit button clicked, exit
            elif (mouseX > width/2-20 and mouseX < width/2-20 + buttonW and
                  mouseY > buttonY and mouseY < buttonY + buttonH):
                exit()def setup():
    global bg, stageNum, winbg, losebg, startScreen, instructionsScreen
    global gun, gunX, gunY, gunW, gunH, gunfire
    global rocks, totalRocks, rockX, rockY, rock_dy, rockW, rockH
    global ammo, maxAmmo, worldHealth, maxHealth
    global isFiring, rockHit, damage
    global rockTypes
    global startTime, gameTime, gameWon, gameStarted, gameActive
    global rockBroken, breakingRocks

    size(1000, 800)
    stageNum = 0  #startscreen
    totalRocks = 6
    gameStarted = False
    gameActive = False

    #load images
    bg = loadImage("bg.png")
    winbg = loadImage("winbg.png")
    losebg = loadImage("losebg.png")
    startScreen = loadImage("startScreen.png")
    instructionsScreen = loadImage("instructions.png")
    gun = loadImage("gun.png")
    gunfire = loadImage("gunfire.png")

    #gun position
    gunX, gunY = width * 0.25, height * 0.67
    gunW, gunH = width * 0.07, height * 0.25

    #initialize ammo and world health
    maxAmmo = 45
    ammo = maxAmmo
    maxHealth = 45
    worldHealth = maxHealth
    damage = 2 #damage when a rock hits the bottom

    #timer variables
    startTime = millis()
    gameTime = 100000 # 100 seconds
    gameWon = False

    #lists for rocks
    rocks = []
    rockW = []
    rockH = []
    rockX = []
    rockY = []
    rock_dy = []
    rockHit = []
    rockTypes = []

    for i in range(totalRocks):
        scale = random(0.05, 0.09)
        rocks.append(loadImage("rock"+str(i)+".png"))
        rockW.append(rocks[i].width * scale)
        rockH.append(rocks[i].height * scale)
        rockX.append(random(width-200))
        rockY.append(random(-300, -50))
        rock_dy.append(random(6, 8))
        rockHit.append(False)
        rockTypes.append(i) #store the rock type 0 to 5

    rockBroken = [] #just for collecting broken rock
    for i in range(6):
        rockBroken.append(loadImage("rockb" + str(i) + ".png"))
    breakingRocks = [] #to store data for actual breaking{x, y, w, h, type, timer}

    isFiring = False

    checkOverlap(i)

def draw():
    global ammo, worldHealth, isFiring, rockX, rockY, rockHit, gameWon, stageNum
    
    #game stages
    if stageNum == 0:
        displayStartScreen() #start
    elif stageNum == 1:
        displayInstructionsScreen() #instr
    elif stageNum == 2:
        drawGameplay() #gameplay

def drawGameplay():
    global ammo, worldHealth, isFiring, rockX, rockY, rockHit, gameWon, gameActive
    
    #check if timer has elapsed for win condition
    if not gameWon and millis() - startTime >= gameTime:
        gameWon = True
        gameActive = False #timer stop
    
    #show victory screen if player has won
    if gameWon:
        displayVictoryScreen()
        return
    
    #game lose check
    if worldHealth<=0 or ammo<=0:
        gameActive = False
        displayGameOverScreen()
        return #skip rest draw function
    gameActive = True #timer only continues if gameactive
    
    #normal game draw
    image(bg, 0, 0, width, height)
    drawBars()
    drawEnduranceClock()

    #draw all breaking rocks
    drawBreakingRocks()

    for i in range(totalRocks):
        #only draw and update rocks that havent been hit
        if not rockHit[i]:
            image(rocks[i], rockX[i], rockY[i], rockW[i], rockH[i])
            rockY[i]+=rock_dy[i]

            #check if rock hits bottom
            if rockY[i]>=height: #reduce world health
                worldHealth -= damage
                worldHealth = max(0,worldHealth)
                resetRock(i) #reset position of rock

            if isFiring and rockGunPath(i):
                rockHit[i] = True
                
                #add breaking rock animation
                addBreakingRock(rockX[i], rockY[i], rockW[i], rockH[i], rockTypes[i])

                #check if it's blue rock(rock0) or red rock(rock1) and increase ammo
                if rockTypes[i] == 0: #blue
                    increaseAmmo(2) #increases ammo 
                elif rockTypes[i] == 1: #red
                    increaseAmmo(2) #increases ammo
                resetRock(i)
    
    #draw gun
    if isFiring: #fire gun
        image(gunfire, gunX, gunY - gunH * 0.2, gunW, gunH * 1.4)
        isFiring = False #reset firing state immediately
    else: #normal gun
        image(gun, gunX, gunY, gunW, gunH)

def addBreakingRock(x, y, w, h, rockType):
    global breakingRocks
    #x,y,w,h are for position of rock and rockType for type(0-5)
    #reate a new breaking rock with position, size, type and timer
    breakingRocks.append({
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'type': rockType,
        'timer': 10 #show for 10 frames
    })

def drawBreakingRocks():
    #draw all breaking rocks and update their timers and remove whose timers have expired
    global breakingRocks, rockBroken

    #process each breaking rock
    i = 0
    while i < len(breakingRocks):
        rock = breakingRocks[i]

        #draw the broken rock
        image(rockBroken[rock['type']], rock['x'], rock['y'], rock['w'], rock['h'])

        #decrease the timer
        rock['timer'] -= 1

        #if timer reaches zero, remove this rock
        if rock['timer'] <= 0:
            del breakingRocks[i]
        else:
            i += 1

def drawEnduranceClock():
    global gameStarted, startTime, gameActive
    
    if gameStarted and gameActive: #only count time when both are true
        timeElapsed = int((millis() - startTime) / 1000)
    else:
        timeElapsed = 0
        
    textX = width - (width * 0.06)
    textY = height * 0.5
    # Draw time value text
    fill(0,0,130)
    textSize(width * 0.019)
    textAlign(CENTER, CENTER)
    text("ENDURANCE \n CLOCK: " + str(timeElapsed) + "s", textX, textY)

def increaseAmmo(amount):
    #function to increase ammo with stop at maxAmmo
    global ammo, maxAmmo
    ammo = min(ammo + amount, maxAmmo)

def resetRock(i):
    global rockX, rockY, rock_dy, rockHit, rockTypes
    rockY[i] = random(-200, -100)
    rockX[i] = random(width-200)
    rock_dy[i] = random(4, 10)
    rockHit[i] = False

    randVal = random(100)

    if randVal < 10: #10% chance for blue(rock0)
        rockTypes[i] = 0
    elif randVal < 20: 
        rockTypes[i] = 1
    else: #80% chance for other rocks(2-5)
        rockTypes[i] = int(random(2, 6))

    #update the rock image
    rocks[i] = loadImage("rock"+str(rockTypes[i])+".png")
    checkOverlap(i)

def rockGunPath(rockIndex):
    global rockX, rockY, rockW, rockH, gunX, gunW
    gun_center = gunX+(gunW/2) #firing path directly above gun

    #allow some tolerance in the hit detection
    tolerance = gunW*0.75
    return (rockX[rockIndex] < gun_center + tolerance/2 and
            rockX[rockIndex] + rockW[rockIndex] > gun_center - tolerance/2)

def drawBars():
    barW = width * 0.03
    barH = height * 0.275 
    barGap = width * 0.055 
    barX = width - (width * 0.047) 
    barY = height * 0.025

    #ammo bar(blue)
    noStroke()
    fill(0, 120, 250)
    rect(barX - barGap, barY + barH * (1 - float(ammo)/maxAmmo),
         barW, barH * (float(ammo)/maxAmmo))

    #world health bar(yellow)
    fill(235, 235, 0)
    rect(barX, barY + barH * (1 - float(worldHealth)/maxHealth),
         barW, barH * (float(worldHealth)/maxHealth))

    #add numerical values
    textSize(width * 0.012)
    textAlign(CENTER, BOTTOM)
    fill(0,0,130)
    text(str(ammo), barX - barGap + barW/2, barY - 0.5)
    text(str(int(worldHealth)), barX + barW/2, barY - 0.5)

def checkOverlap(rockIndex):
    global rockX, rockY, rockW, rockH, totalRocks

    attempts = 0
    max_attempts = 10

    while attempts < max_attempts:
        overlap = False

        #check against all other rocks
        for j in range(totalRocks):
            if rockIndex != j: #to not compare with self
                #rectangle collision check
                if (rockX[rockIndex] < rockX[j] + rockW[j] and
                    rockX[rockIndex] + rockW[rockIndex] > rockX[j] and
                    rockY[rockIndex] < rockY[j] + rockH[j] and
                    rockY[rockIndex] + rockH[rockIndex] > rockY[j]):
                    overlap = True
                    break

        if not overlap:
            return #no overlap found

        #if overlap found generate new position
        rockX[rockIndex] = random(width-200)
        rockY[rockIndex] = random(-500, -50)
        attempts += 1

def keyPressed():
    global gunX, ammo, isFiring, stageNum
    
    if stageNum == 2:
        gunSpeed = width*0.05

        if keyCode == LEFT:
            gunX -= gunSpeed
        elif keyCode == RIGHT:
            gunX += gunSpeed
        elif key == ' ':
            if ammo>0:
                ammo -= 1
                isFiring = True #set firing state

        #gun within screen bounds by using constrain
        gunX = constrain(gunX, 0, width - gunW)

def displayStartScreen():
    image(startScreen, 0, 0, width, height) 
    drawBars()
    drawEnduranceClock()
    drawStartScreenButtons() #draw start and instructions buttons

def displayInstructionsScreen():
    image(instructionsScreen, 0, 0, width, height)
    drawBars()
    drawEnduranceClock()
    drawInstructionsScreenButtons()

def drawStartScreenButtons():
    rectMode(CENTER)
    buttonW = width * 0.3
    buttonH = height * 0.1
    cornerRadius = 25
    
    titleY = height * 0.3 
    buttonSpacing = height * 0.15 
    
    
    fill(255, 50, 50) #start button
    rect(width * 0.4, titleY + buttonSpacing, buttonW, buttonH, cornerRadius)
    fill(50, 50, 255)  #instructions button
    rect(width * 0.4, titleY + buttonSpacing*2, buttonW, buttonH, cornerRadius)

    #button text
    textSize(width * 0.03)
    fill(255)
    textAlign(CENTER, CENTER)
    text("START", width * 0.4, titleY + buttonSpacing)
    text("INSTRUCTIONS", width * 0.4, titleY + buttonSpacing*2)
    #reset rectMode for other 
    rectMode(CORNER)

def drawInstructionsScreenButtons():
    rectMode(CENTER)
    buttonW = width * 0.3
    buttonH = height * 0.1
    cornerRadius = 25

    fill(255, 50, 50) #start button
    rect(width/2, height * 0.8, buttonW, buttonH, cornerRadius)
    
    #button text
    textSize(width * 0.03)
    fill(255)
    textAlign(CENTER, CENTER)
    text("START GAME", width/2, height * 0.8)
    rectMode(CORNER)

def displayGameOverScreen():
    image(losebg, 0, 0, width, height)
    drawBars()
    drawEnduranceClock()
    drawGameButtons("ROCK & RELOAD!", "NOPE, I'M OUT!")

def displayVictoryScreen():
    image(winbg, 0, 0, width, height)
    drawBars()
    drawEnduranceClock()
    drawGameButtons("ROCK & RELOAD!", "NOPE, I'M OUT!")

def drawGameButtons(playAgainText, quitText):
    rectMode(CORNER)
    buttonW = width * 0.3
    buttonH = height * 0.1
    buttonY = height * 0.45
    cornerRadius = 25
    
    fill(255, 50, 50) #play again button
    rect(width/2 - buttonW - 100, buttonY, buttonW, buttonH, cornerRadius)
    
    fill(180, 40, 40) #quit button
    rect(width/2-20, buttonY, buttonW, buttonH, cornerRadius)
    
    textSize(width * 0.023) #buttons text
    fill(255)
    textAlign(CENTER, CENTER)
    text(playAgainText, width/2 - buttonW/2 - 100, buttonY + buttonH/2)
    text(quitText, width/2 + buttonW/2-20, buttonY + buttonH/2)

def mousePressed():
    global startTime, gameWon, worldHealth, ammo, maxAmmo, stageNum, gameStarted, gameActive
    #check which stages we're in
    if stageNum == 0:
        buttonW = width * 0.3
        buttonH = height * 0.1
        titleY = height * 0.3
        buttonSpacing = height * 0.15
        
        #start button clicked
        if (mouseX > width * 0.4 - buttonW/2 and 
            mouseX < width * 0.4 + buttonW/2 and
            mouseY > titleY + buttonSpacing - buttonH/2 and 
            mouseY < titleY + buttonSpacing + buttonH/2):
            stageNum = 2 #go to gameplay
            gameStarted = True  
            gameActive = True
            startTime = millis() #reset timer
            
        #instructions button clicked
        if (mouseX > width * 0.4 - buttonW/2 and 
            mouseX < width * 0.4 + buttonW/2 and
            mouseY > titleY + buttonSpacing*2 - buttonH/2 and 
            mouseY < titleY + buttonSpacing*2 + buttonH/2):
            stageNum = 1 #go to instructions
            startTime = millis() #reset timer
            
    elif stageNum == 1:
        #instructions screen button
        buttonW = width * 0.3
        buttonH = height * 0.1
        
        #start game button clicked
        if (mouseX > width/2 - buttonW/2 and mouseX < width/2 + buttonW/2 and
            mouseY > height * 0.8 - buttonH/2 and mouseY < height * 0.8 + buttonH/2):
            stageNum = 2 #go to gameplay
            gameStarted = True
            gameActive = True
            startTime = millis()  #reset timer when starting
            
    elif stageNum == 2:
        #check if game is over (victory or game over)
        if gameWon or worldHealth <= 0 or ammo <= 0:
            buttonW = width * 0.3
            buttonH = height * 0.1
            buttonY = height * 0.45

            #play again button clicked
            if (mouseX > width/2 - buttonW - 100 and mouseX < width/2 - 100 and
                mouseY > buttonY and mouseY < buttonY + buttonH):
                #reset game
                startTime = millis()
                gameStarted = True #reset
                gameActive = True
                gameWon = False
                worldHealth = maxHealth
                ammo = maxAmmo

                for i in range(totalRocks): #reset all rocks
                    resetRock(i)
                loop() #restart game loop

            #quit button clicked, exit
            elif (mouseX > width/2-20 and mouseX < width/2-20 + buttonW and
                  mouseY > buttonY and mouseY < buttonY + buttonH):
                exit()