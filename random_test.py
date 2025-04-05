import random

word_list = ["apple", "banana", "cherry", "durian", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon", "mango", "nectarine", "orange", "peach", "pear", "plum", "quince", "raspberry", "strawberry", "tangerine", "watermelon"]
guessed_list = []
unguessed_list = []
def get_random_word(word_list):
    return random.choice(word_list).upper()

def display_hangman(lifes):
    state=[
        """
           +---+
           |   |
               |
               |
               |
               |  生命值为6
        =========
        """,
        """
           +---+
               |
               |
               |
               |
               |    生命值为5
        =========
        """,
        """
           +---+
                
               |
               |
               |
               |    生命值为4
        =========
        """,
        """
        +---+
                
                
               |
               |
               |    生命值为3
        """,
        """
        +---+
                
                
                
               |
               |    生命值为2
        """,
        """
        +---+
                
                
                
                
               |    生命值为1
        """,
        """
        +---+
                
                
                
                
                    生命值为0，你死啦死啦滴 
                
        """,
    ]
    print(state[6-lifes])

def handle_guess(guss_bite,random_word):
    # 处理用户输入的字母
    # 检查用户输入的字母是否在随机单词中
    # 如果在，返回True
    # 如果不在，返回False
    print(f"random_word={random_word}")
    for i in range(len(random_word)):
        if guss_bite==random_word[i]:
            guessed_list.append(guss_bite)
            print(f"your right:{guessed_list}")
            return 0
    unguessed_list.append(guss_bite)
    print(f"you are wrong :{unguessed_list}")
    return 1
def play_game():
    # 创建一个循环，直到用户输入'quit'为止
    # 在循环中，调用get_random_word函数获取一个随机单词
    # 在循环中，调用display_hangman函数显示绞刑架状态
    # 在循环中，调用handle_guess函数处理用户输入的字母
    # 在循环中，检查用户输入的字母是否在随机单词中
    # 如果在，将用户输入的字母添加到已猜测的字母列表中
    # 如果不在，将用户输入的字母添加到未猜测的字母列表中
    """主游戏页面
    """
    lifes=6
    random_word=get_random_word(word_list)


    while lifes>0:
        guess_bite = input("请输入一个字母：")
        lifes = lifes - int(handle_guess(guess_bite, random_word))
        display_hangman(lifes)

if __name__ == "__main__":
    play_game()