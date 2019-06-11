# faces.py - put all the faces for the dialogue sections of the game here

class girl():
    face = [('''
             $$$&$$
            $$||||$$
            $ .  . $
            $   `  $
             \\  = /
              |--|
           __/    \\__
    ___________________________
    '''),

    ('''
             $$$&$$
            $$||||$$
            $ _  _ $
            $   `  $
             \\  = /
              |--|
           __/    \\__
    ___________________________
    ''')]

    

    messages = ['Hey You, Kid! Hey!',
                'There\'s a snake next door!',
                'You look tough, think you could kill it?',
                'I\'ll give you some gold!']
    messages2 = ['Have you killed the snake yet?',
                 'Well come back when you have!']
    messages3 = ['Hey thanks for killing that snake!']


class man():
    face = [('''
            |^^^^^^^^^|
            | ... ... |
            |  O   O  |
            |.   B   .|
            |..  >  ..|
            |.........|
    ___________________________
    '''),
    ('''
            |^^^^^^^^^|
            | ... ... |
            |  -   -  |
            |.   B   .|
            |..  >  ..|
            |.........|
    ___________________________
    ''')

            ]

    messages = ['Look, I\'m gonna be honest kid...',
                'You\'ve gotta cut it out with this shit.',
                'Everyone is getting REAL sick of your "adventures"',
                'Now go bother someone else! Bakka!']
    

class oven():
    face = [('''
            ^   ^  ^  ^
         |-------------|
         |.     .  .  .|
         |  ..      .  |
         |.  _______   |
         |  /       \\  |
         |..|       |. |
         |_____________|
    ___________________________
    '''),
    ('''
          ^ ^     ^   ^
         |-------------|
         |.     .  .  .|
         |  ..      .  |
         |.  _______   |
         |  /       \\  |
         |..|       |. |
         |_____________|
    ___________________________
    ''')]

    

    messages = ['It\'s an oven!',
                'You can access this to reset your HP to 10 if it\'s lower!',
                'Here\'s your HP you bum!']


class snakeMan():
    face = [('''
            ________
           /    ^   \\
          |^  ^    O \\
          |     _____/```
          | ^^    |
          | ^   ^ |
    ___________________________
    '''),
    ('''
            ________
           /    ^   \\
          |^  ^    - \\
          |     _____/`^`
          | ^^    |
          | ^   ^ |
    ___________________________
    ''')]

    messages = ['You fool! You\'ve come to the Viper!',
                'Prepare to die in Combat!',
                'HISSSSSSSSS']


class shopkeeper():
    face = [('''
             $$$$$$$$$
            $$$$$$$$$$$
           $| ... ... |$
           C|  O   O  |D
           $|.    |  .|$
          $$|..  -  ..|$$
             \\......./
    ___________________________
    '''),
    ('''
             $$$$$$$$$
            $$$$$$$$$$$
           $| ... ... |$
           C|  -   -  |D
           $|.    |  .|$
          $$|..  -  ..|$$
             \\......./
    ___________________________
    ''')]

    #messages = ['Hey there traveller!', 'What can I do for you?']
    messages = ['Fuck you!', 'You\'re gonna die now!', 'I\'m thirstin for blood!']
        

class anne():
    face = [('''
             $$$&$$
            $$||||$$
            $ .  . $
           $$   |  $$
           $$\\  - /$$
             $|--|$
           __/    \\__
    ___________________________
    '''),

    ('''
             $$$&$$
            $$||||$$
            $ -  - $
           $$   |  $$
           $$\\  - /$$
             $|--|$
           __/    \\__
    ___________________________
    ''')]

    

    messages = ['Hey, need an aly?', 'I\'ll help you fight if you need.',
                'Just say the word, and I\'ll be there to aid you.']

    comp_messages = ['Yes? What is it?',
                     'Just let me know when the next fight is.',
                     'I\'m not one for waiting around.']

class wizard():
    face = [('''
            /------\\
        ___/________\\___
            $$$$$$$$
            $ .  . $
           $$   |  $$
           $$$$$$$$$$
             $$$$$$
           __/$$$$\\__
    ___________________________
    '''),

    ('''
            /------\\
        ___/________\\___
            $$$$$$$$
            $ -  - $
           $$   |  $$
           $$$$$$$$$$
             $$$$$$
           __/$$$$\\__
    ___________________________
    ''')]

    messages = ['Hello, traveler.',
                'Need the assistance of a wizard?',
                'I\'m quite adept at sorcery and healing!']

    comp_messages = ['What is it, friend?',
                     'You\'re quite the fighter.',
                     'Let\'s not rest long, though-',
                     'There is always danger afoot!']


class tank():
    face = [('''
            |^^^^^^^^^|
            | ... ... |
           C|  O   O  |D
            |.    \  .|
            |../===\\..|
            |.........|
    ___________________________
    '''),
    ('''
            |^^^^^^^^^|
            | ... ... |
           C|  -   -  |D
            |.    \  .|
            |../===\\..|
            |.........|
    ___________________________
    ''')
        ]

    messages = ['Ho, looking for might?',
                'Let me take arms with you, adventurer!',
                'Come, we have many to crush!']

    comp_messages = ['Ho, friend.',
                     'How are you doing?',
                     'I\'m glad to have you as my ally!',
                     'Now lets move! I\'ll follow you!']


class king():
    face = [('''
            |_|_|_|_|_|
            | ... ... |
           C|  O   O  |D
            |.   C   .|
            |../===\\..|
            |.........|
    ___________________________
    '''),
    ('''
            |_|_|_|_|_|
            | ... ... |
           C|  -   -  |D
            |.   C   .|
            |../===\\..|
            |.........|
    ___________________________
    ''')
    ]

    messages = ['You come to my kingdom and kill my snake!',
                'Well now, traveler, you shall pay!',
                'WITH YOUR BLOOD!']
