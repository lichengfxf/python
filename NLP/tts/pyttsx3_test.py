import pyttsx3

# 初始化， 必须要有奥
engine = pyttsx3.init()

engine.save_to_file('hello world , we have a nice day', 'pytts.mp3')

# engine.say('Sally sells seashells by the seashore.')
# engine.say('The quick brown fox jumped over the lazy dog.')
# # 注意，没有本句话是没有声音的
# engine.runAndWait()
