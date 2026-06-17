all_emote_list: list[tuple[str, str]] = [
    ("Rest", "sit-idle-cute"),                          # 0
    ("Zombie", "idle_zombie"),                          # 1
    ("Relaxed", "idle_layingdown2"),                    # 2
    ("Attentive", "idle_layingdown"),                   # 3
    ("Sleepy", "idle-sleep"),                           # 4
    ("Pouty Face", "idle-sad"),                         # 5
    ("Posh", "idle-posh"),                              # 6
    ("Sleepy", "idle-loop-tired"),                      # 7
    ("Tap Loop", "idle-loop-tapdance"),                 # 8
    ("Sit", "idle-loop-sitfloor"),                      # 9
    ("Shy", "idle-loop-shy"),                           # 10
    ("Bummed", "idle-loop-sad"),                        # 11
    ("Chillin'", "idle-loop-happy"),                    # 12
    ("Annoyed", "idle-loop-annoyed"),                   # 13
    ("Aerobics", "idle-loop-aerobics"),                 # 14
    ("Ponder", "idle-lookup"),                          # 15
    ("Hero Pose", "idle-hero"),                         # 16
    ("Relaxing", "idle-floorsleeping2"),                # 17
    ("Cozy Nap", "idle-floorsleeping"),                 # 18
    ("Enthused", "idle-enthusiastic"),                  # 19
    ("Boogie Swing", "idle-dance-swinging"),            # 20
    ("Feel The Beat", "idle-dance-headbobbing"),        # 21
    ("Irritated", "idle-angry"),                        # 22
    ("Yes", "emote-yes"),                               # 23
    ("I Believe I Can Fly", "emote-wings"),             # 24
    ("The Wave", "emote-wave"),                          # 25
    ("Tired", "emote-tired"),                            # 26
    ("Think", "emote-think"),                            # 27
    ("Theatrical", "emote-theatrical"),                  # 28
    ("Tap Dance", "emote-tapdance"),                     # 29
    ("Super Run", "emote-superrun"),                     # 30
    ("Super Punch", "emote-superpunch"),                 # 31
    ("Sumo Fight", "emote-sumo"),                        # 32
    ("Thumb Suck", "emote-suckthumb"),                   # 33
    ("Splits Drop", "emote-splitsdrop"),                 # 34
    ("Snowball Fight!", "emote-snowball"),               # 35
    ("Snow Angel", "emote-snowangel"),                   # 36
    ("Shy", "emote-shy"),                                # 37
    ("Secret Handshake", "emote-secrethandshake"),       # 38
    ("Sad", "emote-sad"),                                # 39
    ("Rope Pull", "emote-ropepull"),                     # 40
    ("Roll", "emote-roll"),                              # 41
    ("ROFL!", "emote-rofl"),                             # 42
    ("Robot", "emote-robot"),                            # 43
    ("Rainbow", "emote-rainbow"),                        # 44
    ("Proposing", "emote-proposing"),                    # 45
    ("Peekaboo!", "emote-peekaboo"),                     # 46
    ("Peace", "emote-peace"),                            # 47
    ("Panic", "emote-panic"),                            # 48
    ("No", "emote-no"),                                  # 49
    ("Ninja Run", "emote-ninjarun"),                     # 50
    ("Night Fever", "emote-nightfever"),                 # 51
    ("Monster Fail", "emote-monster_fail"),              # 52
    ("Model", "emote-model"),                            # 53
    ("Flirty Wave", "emote-lust"),                       # 54
    ("Level Up!", "emote-levelup"),                      # 55
    ("Amused", "emote-laughing2"),                       # 56
    ("Laugh", "emote-laughing"),                         # 57
    ("Kiss", "emote-kiss"),                              # 58
    ("Super Kick", "emote-kicking"),                     # 59
    ("Jump", "emote-jumpb"),                             # 60
    ("Judo Chop", "emote-judochop"),                     # 61
    ("Imaginary Jetpack", "emote-jetpack"),              # 62
    ("Hug Yourself", "emote-hugyourself"),               # 63
    ("Sweating", "emote-hot"),                           # 64
    ("Hero Entrance", "emote-hero"),                     # 65
    ("Hello", "emote-hello"),                            # 66
    ("Headball", "emote-headball"),                      # 67
    ("Harlem Shake", "emote-harlemshake"),               # 68
    ("Happy", "emote-happy"),                            # 69
    ("Handstand", "emote-handstand"),                    # 70
    ("Greedy Emote", "emote-greedy"),                    # 71
    ("Graceful", "emote-graceful"),                      # 72
    ("Moonwalk", "emote-gordonshuffle"),                 # 73
    ("Ghost Float", "emote-ghost-idle"),                 # 74
    ("Gangnam Style", "emote-gangnam"),                  # 75
    ("Frolic ", "emote-frollicking"),                    # 76
    ("Faint", "emote-fainting"),                         # 77
    ("Clumsy", "emote-fail2"),                           # 78
    ("Fall", "emote-fail1"),                             # 79
    ("Face Palm", "emote-exasperatedb"),                 # 80
    ("Exasperated", "emote-exasperated"),                # 81
    ("Elbow Bump", "emote-elbowbump"),                   # 82
    ("Disco", "emote-disco"),                            # 83
    ("Blast Off", "emote-disappear"),                    # 84
    ("Faint Drop", "emote-deathdrop"),                   # 85
    ("Collapse", "emote-death2"),                        # 86
    ("Revival", "emote-death"),                          # 87
    ("Dab", "emote-dab"),                                # 88
    ("Curtsy", "emote-curtsy"),                          # 89
    ("Confusion", "emote-confused"),                     # 90
    ("Cold", "emote-cold"),                              # 91
    ("Charging", "emote-charging"),                      # 92
    ("Bunny Hop", "emote-bunnyhop"),                     # 93
    ("Bow", "emote-bow"),                                # 94
    ("Boo", "emote-boo"),                                # 95
    ("Home Run!", "emote-baseball"),                     # 96
    ("Falling Apart", "emote-apart"),                    # 97
    ("Thumbs Up", "emoji-thumbsup"),                     # 98
    ("Point", "emoji-there"),                            # 99
    ("Sneeze", "emoji-sneeze"),                          # 100
    ("Smirk", "emoji-smirking"),                         # 101
    ("Sick", "emoji-sick"),                              # 102
    ("Gasp", "emoji-scared"),                            # 103
    ("Punch", "emoji-punch"),                            # 104
    ("Pray", "emoji-pray"),                              # 105
    ("Stinky", "emoji-poop"),                            # 106
    ("Naughty", "emoji-naughty"),                        # 107
    ("Mind Blown", "emoji-mind-blown"),                  # 108
    ("Lying", "emoji-lying"),                            # 109
    ("Levitate", "emoji-halo"),                          # 110
    ("Fireball Lunge", "emoji-hadoken"),                 # 111
    ("Give Up", "emoji-give-up"),                        # 112
    ("Tummy Ache", "emoji-gagging"),                     # 113
    ("Flex", "emoji-flex"),                              # 114
    ("Stunned", "emoji-dizzy"),                          # 115
    ("Cursing Emote", "emoji-cursing"),                  # 116
    ("Sob", "emoji-crying"),                             # 117
    ("Clap", "emoji-clapping"),                          # 118
    ("Raise The Roof", "emoji-celebrate"),               # 119
    ("Arrogance", "emoji-arrogance"),                    # 120
    ("Angry", "emoji-angry"),                            # 121
    ("Vogue Hands", "dance-voguehands"),                 # 122
    ("Savage Dance", "dance-tiktok8"),                   # 123
    ("Don't Start Now", "dance-tiktok2"),                # 124
    ("Yoga Flow", "dance-spiritual"),                    # 125
    ("Smoothwalk", "dance-smoothwalk"),                  # 126
    ("Ring on It", "dance-singleladies"),                # 127
    ("Let's Go Shopping", "dance-shoppingcart"),         # 128
    ("Russian Dance", "dance-russian"),                  # 129
    ("Robotic", "dance-robotic"),                        # 130
    ("Penny's Dance", "dance-pennywise"),                # 131
    ("Orange Juice Dance", "dance-orangejustice"),       # 132
    ("Rock Out", "dance-metal"),                         # 133
    ("Karate", "dance-martial-artist"),                  # 134
    ("Macarena", "dance-macarena"),                      # 135
    ("Hands in the Air", "dance-handsup"),               # 136
    ("Floss", "dance-floss"),                            # 137
    ("Duck Walk", "dance-duckwalk"),                     # 138
    ("Breakdance", "dance-breakdance"),                  # 139
    ("K-Pop Dance", "dance-blackpink"),                  # 140
    ("Push Ups", "dance-aerobics"),                      # 141
    ("Hyped", "emote-hyped"),                            # 142
    ("Jinglebell", "dance-jinglebell"),                  # 143
    ("Nervous", "idle-nervous"),                         # 144
    ("Toilet", "idle-toilet"),                           # 145
    ("Attention", "emote-attention"),                    # 146
    ("Astronaut", "emote-astronaut"),                    # 147
    ("Dance Zombie", "dance-zombie"),                    # 148
    ("Ghost", "emoji-ghost"),                            # 149
    ("Heart Eyes", "emote-hearteyes"),                   # 150
    ("Swordfight", "emote-swordfight"),                  # 151
    ("TimeJump", "emote-timejump"),                      # 152
    ("Snake", "emote-snake"),                            # 153
    ("Heart Fingers", "emote-heartfingers"),             # 154
    ("Heart Shape", "emote-heartshape"),                 # 155
    ("Hug", "emote-hug"),                                # 156
    ("Laugh", "emote-lagughing"),                        # 157
    ("Eyeroll", "emoji-eyeroll"),                        # 158
    ("Embarrassed", "emote-embarrassed"),                # 159
    ("Float", "emote-float"),                            # 160
    ("Telekinesis", "emote-telekinesis"),                # 161
    ("Sexy dance", "dance-sexy"),                        # 162
    ("Puppet", "emote-puppet"),                          # 163
    ("Fighter idle", "idle-fighter"),                    # 164
    ("Penguin dance", "dance-pinguin"),                  # 165
    ("Creepy puppet", "dance-creepypuppet"),             # 166
    ("Sleigh", "emote-sleigh"),                          # 167
    ("Maniac", "emote-maniac"),                          # 168
    ("Energy Ball", "emote-energyball"),                 # 169
    ("Singing", "idle_singing"),                         # 170
    ("Frog", "emote-frog"),                              # 171
    ("Superpose", "emote-superpose"),                    # 172
    ("Cute", "emote-cute"),                              # 173
    ("TikTok Dance 9", "dance-tiktok9"),                 # 174
    ("Weird Dance", "dance-weird"),                      # 175
    ("TikTok Dance 10", "dance-tiktok10"),               # 176
    ("Pose 7", "emote-pose7"),                           # 177
    ("Pose 8", "emote-pose8"),                           # 178
    ("Casual Dance", "idle-dance-casual"),               # 179
    ("Pose 1", "emote-pose1"),                           # 180
    ("Pose 3", "emote-pose3"),                           # 181
    ("Pose 5", "emote-pose5"),                           # 182
    ("Cutey", "emote-cutey"),                            # 183
    ("Punk Guitar", "emote-punkguitar"),                 # 184
    ("Zombie Run", "emote-zombierun"),                   # 185
    ("Fashionista", "emote-fashionista"),                # 186
    ("Gravity", "emote-gravity"),                        # 187
    ("Ice Cream Dance", "dance-icecream"),               # 188
    ("Wrong Dance", "dance-wrong"),                      # 189
    ("UwU", "idle-uwu"),                                 # 190
    ("TikTok Dance 4", "idle-dance-tiktok4"),            # 191
    ("Advanced Shy", "emote-shy2"),                      # 192
    ("Anime Dance", "dance-anime"),                      # 193
    ("Kawaii", "dance-kawai"),                           # 194
    ("Scritchy", "idle-wild"),                           # 195
    ("Ice Skating", "emote-iceskating"),                 # 196
    ("SurpriseBig", "emote-pose6"),                      # 197
    ("Celebration Step", "emote-celebrationstep"),       # 198
    ("Creepycute", "emote-creepycute"),                  # 199
    ("Frustrated", "emote-frustrated"),                  # 200
    ("Pose 10", "emote-pose10"),                         # 201
    ("Relaxed", "sit-relaxed"),                          # 202
    ("Laid Back", "sit-open"),                           # 203
    ("Star gazing", "emote-stargaze"),                   # 204
    ("Slap", "emote-slap"),                              # 205
    ("Boxer", "emote-boxer"),                            # 206
    ("Head Blowup", "emote-headblowup"),                 # 207
    ("KawaiiGoGo", "emote-kawaiigogo"),                  # 208
    ("Repose", "emote-repose"),                          # 209
    ("Tiktok7", "idle-dance-tiktok7"),                   # 210
    ("Shrink", "emote-shrink"),                          # 211
    ("Ditzy Pose", "emote-pose9"),                       # 212
    ("Teleporting", "emote-teleporting"),                # 213
    ("Touch", "dance-touch"),                            # 214
    ("Air Guitar", "idle-guitar"),                       # 215
    ("This Is For You", "emote-gift"),                   # 216
    ("Push it", "dance-employee"),                       # 217
    ("Come Here", "emote-offdutyangels-comehere"),       # 218
    ("Back Off", "emote-offdutyangels-backoff"),         # 219
    ("Sweet Strike", "emote-sugarbite-pose1"),           # 220
    ("Sweet Fix", "emote-sugarbite-pose2"),              # 221
    ("Sweet Lure", "emote-sugarbite-pose3"),             # 222
    ("Storm Groove", "emote-rainstruck-success"),        # 223
    ("Storm Mood", "emote-rainstruck-fail"),             # 224
    ("Midnight Poise", "emote-pose-goth1"),              # 225
    ("Midnight Strut", "emote-pose-goth2"),              # 226
    ("Midnight Allure", "emote-pose-goth3"),             # 227
    ("Spooky Swagger (Legendary)", "emote-littlemonsters-dance"), # 228
    ("Yoinked (Legendary)", "emote-ragdoll"),            # 229
    ("Daydreaming", "emote-idle-daydreaming"),           # 230
]
