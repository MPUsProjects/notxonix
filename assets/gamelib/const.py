from assets.gamelib.scripts import *

# базовые
APPNAME = 'Notxonix'
APPVER = '1.0'

# технические
MAINSCR = 1
GAMESCR = 2
SHOPSCR = 3
SKINSCR = 4
BUYSCR = 5
GAMEOVERSCR = 6
STATUS = 2
LDBFILE = 'data/playerdata.db'

# controls (управление)
KUP = pg.K_UP
KDOWN = pg.K_DOWN
KLEFT = pg.K_LEFT
KRIGHT = pg.K_RIGHT

# textures
BALLS = load_ball_textures()
MISC = load_misc_textures()
BGTEX = load_bg_textures()

# deco
ARR = MISC['arrow']
BTN = pg.transform.rotozoom(MISC['button'], 0, 5)
MONEY = MISC['cash']
ARR2 = pg.transform.rotozoom(ARR, 180, 1)
BACK = pg.transform.rotozoom(ARR, 180, 1.5)
FOR = pg.transform.rotozoom(BACK, 180, 1)
pg.init()
FONT = pg.font.SysFont("timesnewroman", 26)
TITLE = pg.font.SysFont("timesnewroman", 42)
BF = FONT.render("назад", True, (255, 255, 255))  # BF = Back Font
MF = FONT.render("магазин", True, (255, 255, 255))  # MF = Magazin Font
MT = TITLE.render("МАГАЗИН", True, (255, 255, 255))  # MT = Magazin Title
ST = TITLE.render("ВЫБЕРИТЕ СКИН", True, (255, 255, 255))  # ST = Skinchanger Title
'YES = TITLE.render("ДА", True, (255, 255, 255))'
'NO = TITLE.render("НЕТ", True, (255, 255, 255))'
MON = pg.transform.rotozoom(MONEY, 0, 1.2)  # money resized
GAME = FONT.render("ИГРАТЬ", True, (255, 255, 255))
LEAVE = FONT.render("ВЫЙТИ", True, (255, 255, 255))
MT1 = FONT.render("МАГАЗИН", True, (255, 255, 255))
OVER = TITLE.render("ИГРА ОКОНЧЕНА", True, (255, 255, 255))
WINTEX = TITLE.render("ПОБЕДА!", True, (255, 255, 255))
LOSTEX = TITLE.render("ПОРАЖЕНИЕ!", True, (255, 255, 255))

# prices
FREE = 0
NORMAL = 5
RARE = 10
EPIC = 20
LEGENDARY = 50

# rarities
MINER = FREE
LOKI = LEGENDARY
WARRIOR = NORMAL
MEXICANES = EPIC
SHREK = RARE

# skins
LOKI_SKIN = 'loki.png'
MINER_SKIN = 'main_hero.png'
WARRIOR_SKIN = 'warrior.png'
MEXICAN_SKIN = 'mexicanes.png'
SHREK_SKIN = 'shrek.png'

# cellcodes
__CELLPLAYER = '@'
__CELLVOID = '.'
__CELLFIELD = '#'

# config облачной бд (Google Firebase)
DBCERT = {"type": "service_account",
          "project_id": "notxonix-game",
          "private_key_id": "a2164f4742ac95796bacf0c67b1812aad5427f7e",
          "private_key": ("-----BEGIN PRIVATE KEY-----\n" +
                          "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDCyezCPcJnX7Sj\nec54fGWr7DThMJILnSpRqt/NY"
                          + "79q+49zH+psnlmfccM7dUlk0QtNLwWfAI5XhdU+\n4kPc6EtW5K5OU4+Bfwvi/Jcec/oD6Wbega0OPYlvFQXDl5m+"
                          + "DhZIGDLY4tSE7gOY\nwWVsjJBOEcSbkqJjrmtcYybd0ZkEn5eDLK8Pg92xO5XqxQC8VnBz7in3csLW6x0r\nUr2Wx"
                          + "Aui325Mpp7Ev4F02oIadCr4SwXaAHrH7D6Ps1MHPwzQbFiUWj3jwEQvRYdY\nVgt5VUoKO+jgwjWfEsiXs8MfW+0k"
                          + "wKyMEWBf0xmogSAXudPHH4EW0b6Ocvy47lcz\nVyt2stKdAgMBAAECggEABERcOqJ6NmQCRvayRz4bk94EIYiI5n0"
                          + "hcgtyRPBOsoQD\nIwE7upHnqJnBuyhCvMhK8FYO0DcfQLt5wQ6/vSB2LnFETT4NqnqADIKk6wg2dzmS\nPpHfwRLB"
                          + "hp/fnrODOdN0RjOITgTk2J2f+AuihZoSev27wH6AYeEhnaY+Md7dzhwi\nf4T04aOr9A+tbuFSPnmbXWaqfLR3BUe"
                          + "aqSIRwFbcfBITZIXvY8LYsvAwi+KCI7UH\n9coolAJdS+zEWhlwSA7imCnBc1Muwav5VRAniWWM0MoBFcH+1jMDfn"
                          + "AmcdQBXq8c\nlGG0ZaBTHJC6Xb3bYcoU/C9X85MD7/yayRMyNlQVKQKBgQDh5LcTJGOLD69xne4n\nlKm000FVxS6"
                          + "QQ8jyEttDyHGsQZ/rtlW0LKSUkTJHbNpMtkOGNSnMeei8rNXY5M9A\nxoQnpkMyGAhi+WJ3GGLB24lUyM7a+8C7jr"
                          + "4GA0SKelQofVk/XZ0rqWC0163JQS+J\naN9Fkzqjnh1+t8WeTCGaVskn6QKBgQDcv/JHY2ZwJ4Ud/IQNNxJ7ahrTU"
                          + "+oSZgPW\no2WH8eTGZ8palQJpB7T9LBvxBSmYiI8GYpBgXk3h0oUgG8mFNkToBEpYZSLGWvHR\nhThAYSB8m81Ziw"
                          + "xxunsHKz8kLYOFKEbPWtJlfpprSldVFABymx3iZbne1YVlE1S3\nyI0PZSLYlQKBgEoG7uwJ/8khscgVDmfQMzE8D"
                          + "ewyu0ixvhd+kHaNKJtfwi23yixK\neQDq+EQp6vw6urQvlewZg2jZZxc2HKlIpSRtOxYehBkTSu5mgm6vKDktuYR"
                          + "P/mA4\nrhNAXOTYo93E/ktivVACqNt61sveXdq1EH43en8GIPpW9R8kKdrvV+qJAoGBAKz9\nhsHG9ZnifoEXR+yL"
                          + "QeKRLeB6HC663zsu5Pv55gxNfdgqea8RKRZVoLfqEcTFD0Az\nsWyzuljDfyvAWtYXxzwDULeg2fWTg3lr6r8Y3jq"
                          + "IZg5L1z6wooTlsR+Kw0xwWb1Z\nMRP0eNKneXTkrc0iHfMzQMuNjHG/Cl7TvSdZXEtZAoGAF1gg9/HxmqgY90SP/Z"
                          + "tD\n5oW9zkEFTtwhwfOhma3TOtnfbCAkRf2tLaEqnx57nySwO+8LpZlzhXpRp8K5UYlu\nYxb0RTZ+PBrGIpnic73"
                          + "pJ0V8VAPrIpTfKYRxxx/FSCFe82J1Hi4XWf0rQ/ajAori\n03berQ6GDgca7ZvmUO1ahek=\n" +
                          "-----END PRIVATE KEY-----\n"),
          "client_email": "firebase-adminsdk-fbsvc@notxonix-game.iam.gserviceaccount.com",
          "client_id": "103685725889865804938",
          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
          "token_uri": "https://oauth2.googleapis.com/token",
          "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
          "client_x509_cert_url": ("https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40notxoni"
                                   + "x-game.iam.gserviceaccount.com"),
          "universe_domain": "googleapis.com"
          }
DBURL = "https://notxonix-game-default-rtdb.europe-west1.firebasedatabase.app"

#  переменные в дб
"WB = warrior bought"
"LB = loki bought"
"MainB = main_skin bought"
"MexB = mexican bought"
'Money = деньги'
"Skin - выбранный скин"
"ShrekB - shrek bought"
