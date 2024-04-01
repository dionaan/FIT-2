import pyxel
import random

class Player:
    def __init__(self, x, y, ground_y):
        self.x = x
        self.y = y
        self.ground_y = ground_y
        self.width = 16
        self.height = 32
        self.score = 0
        self.GRAVITY = 1.3
        self.JUMP_VELOCITY = -15
        self.is_jumping = False
        self.jump_velocity = 0

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE) and not self.is_jumping:
            self.is_jumping = True 
            self.jump_velocity = self.JUMP_VELOCITY

        if self.is_jumping:
            self.jump_velocity += self.GRAVITY
            self.y += self.jump_velocity

            if self.y >= self.ground_y - self.height:
                self.y = self.ground_y - self.height
                self.is_jumping = False
                self.jump_velocity = 0
    
    def draw(self):
        pyxel.blt(self.x,self.y,0,7,48,18,32,1)

class Ingredient:
    INGREDIENTS = (
        "fish",
        "tomato",
        "egg",
        "cucumber",
        "mushroom",
        "lemon",
        "carrot",
        "scallion",
        "leaf",
        "chili",
        "tempe",
        "trash"
    )
    OTHER_INGREDIENTS = (
        "tomato",
        "egg",
        "cucumber",
        "mushroom",
        "lemon",
        "carrot",
        "scallion",
        "leaf",
        "chili",
        "tempe",
    )
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.width = 16
        self.height = 16

    def update(self):
        self.x -= pyxel.rndi(1,10)

    def draw(self):
        if self.type == "trash":
            pyxel.blt(self.x, self.y, 0, 16, 32, 16, 16, 0)
        elif self.type == "fish":
            pyxel.blt(self.x, self.y, 0, 48, 16, 16, 16, 15)
        elif self.type == "tomato":
            pyxel.blt(self.x, self.y, 0, 0, 0, 16, 16, 1)
        elif self.type == "egg":
            pyxel.blt(self.x, self.y, 0, 16, 0, 16, 16, 1)
        elif self.type == "cucumber":
            pyxel.blt(self.x, self.y, 0, 32, 0, 16, 16, 1)
        elif self.type == "mushroom":
            pyxel.blt(self.x, self.y, 0, 48, 0, 16, 16, 1)
        elif self.type == "lemon":
            pyxel.blt(self.x, self.y, 0, 0, 16, 16, 16, 1)
        elif self.type == "carrot":
            pyxel.blt(self.x, self.y, 0, 16, 16, 16, 16, 1)
        elif self.type == "scallion":
            pyxel.blt(self.x, self.y, 0, 32, 16, 16, 16, 1)
        elif self.type == "leaf":
            pyxel.blt(self.x, self.y, 0, 0, 32, 16, 16, 1)
        elif self.type == "chili":
            pyxel.blt(self.x, self.y, 0, 32, 32, 16, 16, 1)
        elif self.type == "tempe":
            pyxel.blt(self.x, self.y, 0, 48, 32, 16, 16, 1)

class App:
    def __init__(self):
        self.window_width = 200
        self.window_height = 120
        pyxel.init(self.window_width, self.window_height)
        pyxel.load("assets/pyxres.pyxres")

        self.player = Player(30, self.window_height - 32, self.window_height)
        self.ingredients = [] #what you have rn
        self.required_ingredients = [] #required per round
        #if touch = req, score +1, if req = 0, ing = obstacle, make obstacle list and add the ing to it after you get enough
        self.obstacles = [] #holding the trash
        self.ingredient_count = 0 #how much you need per ingredient
        self.score = 0
        self.is_game_over = False
        self.restart = False

        pyxel.sound(0).set(notes='A2C3', tones = 'TT', volumes = '33', effects = 'NN', speed=10)
        pyxel.sound(1).set(notes='F2G3', tones = 'NN', volumes = '33', effects = 'NN', speed=10)

        self.generate_ingredients()
        self.generate_ingredient_list()
        pyxel.run(self.update, self.draw)

    def generate_ingredients(self):
        if len(self.ingredients) < 1:
            x = self.window_width
            height = random.choice((self.window_height - 25, self.window_height - 60))
            y = int(height)
            ingredient_type = random.choice(Ingredient.INGREDIENTS)
            ingredient = Ingredient(x, y, ingredient_type)
            self.ingredients.append(ingredient)

    # list of what you can and cant get
    def generate_ingredient_list(self):
        required_ingredient_types = random.sample(Ingredient.OTHER_INGREDIENTS, 2)
        required_ingredient_types.append("fish")
        self.ingredient_count = random.choices(range(1,4), k=3)

        self.required_ingredients = [
            Ingredient(0, 0, type)
            for type in required_ingredient_types
        ]

        self.obstacles = list(Ingredient.INGREDIENTS)
        self.obstacles.remove("trash")
        for i in required_ingredient_types:
            self.obstacles.remove(i)

    def draw_ingredient_list(self):
        text_x = self.window_width - 85
        text_y = 5
        pyxel.text(text_x, text_y, "Ingredients:", 7)
        
        # required ingredients' illustration
        for i, ingredient in enumerate(self.required_ingredients):
            ingredient.x = text_x
            ingredient.y = text_y - 3 + (i + 1) * 12
            ingredient.draw()
        
        # ingredient name & count
        ingredient_count_x = text_x + 23
        ingredient_count_y = text_y + 10
        for i, ingredient in enumerate(self.required_ingredients[0:]):
            ingredient_count_y = text_y + (i + 1) * 13
            pyxel.text(ingredient_count_x, ingredient_count_y, 
                       f"{ingredient.type.capitalize()}: {self.ingredient_count[i]}", 7)

    def check_collisions(self, player, ingredients):
        if (player.x < ingredients.x + ingredients.width
            and player.x + player.width > ingredients.x
            and player.y < ingredients.y + ingredients.height
            and player.y + player.height > ingredients.y
            ):
            return True
        return False

    def restart_game(self):
        self.player = Player(30, self.window_height - 32, self.window_height)
        self.ingredients = []
        self.required_ingredients = []
        self.obstacles = []
        self.score = 0
        self.is_game_over = False
        self.restart = False

        self.generate_ingredients()
        self.generate_ingredient_list()

    def game_over(self):
        pyxel.cls(7)
        game_over_text = "GAME OVER"
        score_text = "Score: " + str(self.score)
        press_text = "Press Q to quit"
        text_x = self.window_width // 2 - len(game_over_text) * 2
        text_y = self.window_height // 2 - 30
        pyxel.text(text_x, text_y, game_over_text, 8)
        text_x = self.window_width // 2 - len(score_text) * 2
        pyxel.text(text_x, text_y + 10, score_text, 8)
        text_x = self.window_width // 2 - len(press_text) * 2
        pyxel.text(text_x, text_y + 20, press_text, 8)
        restart_text = "Press SPACE to restart"
        text_x = self.window_width // 2 - len(restart_text) * 2
        pyxel.text(text_x, text_y + 50, restart_text, 8)
        self.restart = True

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        if self.restart:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.restart_game()
            return

        if not self.is_game_over:
            self.player.update()

            for ingredient in self.ingredients:
                ingredient.update()

                score_minus = True

                for i, req_ingredient in enumerate(self.required_ingredients): 
                    if self.check_collisions(self.player, ingredient) :
                        if ingredient.type == req_ingredient.type:
                            self.score += 1
                            self.ingredient_count[i] -= 1
                            pyxel.play(0,0)
                            if self.ingredient_count[i] == 0:
                                if ingredient.type not in self.obstacles:
                                    self.obstacles.append(ingredient.type) # Add the ingredient to the removal list
                                    self.required_ingredients.remove(req_ingredient)
                                    self.ingredient_count.pop(i)
                            elif self.ingredient_count[i] < 0 :
                                self.ingredient_count[i] = 0

                        elif ingredient.type == "trash":
                            self.is_game_over = True
                            pyxel.play(0,1)
                            
                        else:
                            if score_minus == True:
                                if ingredient.type in self.obstacles:
                                    self.score -= 1
                                    score_minus = False
                                    pyxel.play(0,1)
                        
                        if ingredient in self.ingredients:
                            self.ingredients.remove(ingredient)

                if ingredient.x <= 0:
                    if ingredient in self.ingredients:
                        self.ingredients.remove(ingredient)
            
            if ingredient.x + 16 < self.window_width / 3*2:
                self.generate_ingredients()
         
            if self.ingredient_count == []:
                self.generate_ingredient_list()
                
            if self.score < 0:
                self.score = 0

    def draw(self):
        pyxel.blt(0, 0, 1, 0, 0, self.window_width, self.window_height, None)
        self.player.draw()

        for ingredient in self.ingredients:
            ingredient.draw()

        pyxel.mouse(True)
        self.draw_ingredient_list()
        pyxel.text(5, 5, "Score: " + str(self.score), 7)

        if self.is_game_over:
            self.game_over()

App()