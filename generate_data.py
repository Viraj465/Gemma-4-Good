import json
import random

themes = [
    "burnout", "loneliness", "anxiety", "academic_pressure", 
    "workplace_stress", "uncertainty", "bullying", "grief",
    "overthinking", "family_pressure", "identity_confusion",
    "emotional_numbness", "self_worth_struggles"
]

dialogue_banks = {
    "overthinking": {
        "starts": [
            ("I can't stop replaying that conversation from this morning. I'm convinced I said something stupid and now they hate me.",
             "The mind has a way of turning small moments into huge catastrophes. It's like a broken record playing the same stressful track. What's the 'worst' thing you imagine they're thinking?"),
            ("My brain is just a loop of everything that could go wrong next week. I can't even focus on what I'm doing right now.",
             "It sounds like your mind is living in a future that hasn't happened yet, which makes the present feel impossible. Can we try to find one thing you can touch or hear right now?"),
            ("I keep analyzing every little thing. I'm so tired of my own thoughts.",
             "That mental fatigue is so real. Overthinking is often just our brain trying to protect us from being caught off guard. What's one thing you're absolutely certain of right now?")
        ],
        "mids": [
            ("I just feel like I always ruin things. Why can't I just be normal?",
             "Being 'normal' is a myth, but feeling like you constantly ruin things is a very heavy burden. Overthinking isn't a flaw; it's an overactive defense mechanism. How long have you been carrying this fear?"),
            ("I try to distract myself, but the thoughts always creep back in.",
             "Distraction works for a moment, but it rarely solves the root anxiety. What happens if, instead of pushing the thoughts away, you just acknowledge them and say 'Okay, I hear you' without engaging?"),
            ("I just want my brain to be quiet for five minutes. It's exhausting.",
             "It is exhausting. Wanting quiet is completely understandable. When you think of a 'quiet' moment in your past, where were you and what were you doing?")
        ],
        "endings": [
            ("I guess I'll try to just watch a show and let the thoughts pass. It's hard, but I'll try.",
             "Watching a show is a gentle way to pass the time. It is hard, and it takes practice to let thoughts pass without grabbing onto them. Be kind to yourself tonight."),
            ("I don't know. The thoughts are still there. I'm just going to try to sleep.",
             "Sleep might be exactly what your brain needs to reset the loop. Give yourself permission to let go of the day's worries. I hope you get some rest."),
            ("I'll try that grounding thing. Just focusing on what's right in front of me.",
             "Focusing on the immediate present is a powerful tool against overthinking. Take it one moment, one object, one breath at a time.")
        ]
    },
    "family_pressure": {
        "starts": [
            ("My parents expect so much from me, and I just feel like I'm constantly disappointing them.",
             "Carrying the weight of family expectations can feel incredibly heavy. It's exhausting to constantly feel like you're falling short, even when you're trying your best. Have they explicitly said they're disappointed, or is it a feeling you carry?"),
            ("Every time I talk to my family, it turns into a lecture about what I should be doing with my life.",
             "That sounds incredibly draining. It makes sense that you'd feel pressured when every interaction turns into a critique. How do you usually respond in those moments?"),
            ("I want to make my own choices, but I feel guilty if they don't align with what my family wants.",
             "That guilt is a heavy burden, often stemming from a deep desire to be loved and accepted by them. It's hard when asserting your independence feels like a betrayal. What is a choice you deeply want to make for yourself right now?")
        ],
        "mids": [
            ("They compare me to my siblings all the time. It makes me feel worthless.",
             "Being compared to others, especially siblings, is a deep emotional wound. You are not meant to be a copy of anyone else. What is something you value about yourself that they might not understand?"),
            ("I just freeze. I can't argue with them because it just makes things worse.",
             "Freezing is a very natural trauma response; it's your brain trying to protect you from further emotional harm. It makes complete sense that you stay quiet to avoid escalation. How do you process those feelings after the conversation ends?"),
            ("I just feel so trapped. Like I'm living a life scripted by someone else.",
             "Feeling trapped in a life you didn't fully choose is suffocating. Recognizing that feeling is the first step toward untangling it. What is one small area of your life where you feel you have total control?")
        ],
        "endings": [
            ("I guess I need to set some boundaries, but I'm terrified to do it.",
             "It is terrifying to set boundaries with family. You don't have to do it all at once. Start small, and remember that protecting your peace is a valid reason. Take care of yourself tonight."),
            ("I don't even know who I am outside of their expectations. It's overwhelming.",
             "It's okay to not know yet. Untangling your identity from their expectations is a long journey, not an overnight realization. Be gentle with yourself in this overwhelming space."),
            ("I'll try to focus on the things I like doing, even if they don't approve. It's a start.",
             "That is a beautiful start. Honoring what you enjoy is a powerful way to reclaim your own life. Enjoy those moments today.")
        ]
    },
    "identity_confusion": {
        "starts": [
            ("I look in the mirror and I don't even know who I am anymore. Everything feels fake.",
             "Feeling disconnected from your own reflection is deeply unsettling. That sense of fakeness often happens when we've been living for others for too long. When was the last time you felt somewhat like 'yourself'?"),
            ("I've changed so much recently, and I'm scared I'm losing the person I used to be.",
             "Change, even positive change, involves grief. It's normal to feel scared when the old version of you is fading, but the new version hasn't fully solidified yet. What parts of your 'old' self do you miss?"),
            ("I don't know what I like, what I want, or what I believe in. I just feel blank.",
             "That blankness can be terrifying, but it can also be a clean slate. When the noise of expectations is stripped away, sometimes nothing is left for a while. What happens if you sit with that blankness without trying to fill it?")
        ],
        "mids": [
            ("I just feel like I'm playing a character in my own life. None of it feels real.",
             "Playing a character is exhausting. It takes a tremendous amount of energy to maintain a facade. What would happen if you let the character drop, just for an hour, when you're completely alone?"),
            ("I miss knowing exactly what my path was. Now, everything is just blurry.",
             "The comfort of a clear path is hard to let go of. The blurriness is uncomfortable, but it's often the space where we do the most growing. What is one small, simple thing you know you enjoy doing, regardless of your path?"),
            ("I try to find things I care about, but I just don't have the energy to care.",
             "It's very hard to explore your identity when you're depleted. Identity exploration requires energy. What if the only thing you need to focus on right now is resting and recovering your strength?")
        ],
        "endings": [
            ("I'll just try to exist today without judging myself for not having answers.",
             "Existing without judgment is a profound act of self-compassion. You don't need all the answers today. Just be."),
            ("Maybe I'll try that. Just sitting with the blankness. It sounds scary but needed.",
             "It is scary, but it's also a very courageous way to honor where you are. Let the blankness just 'be' without rushing to fix it. Take your time."),
            ("I think I just need to sleep. I'm too tired to figure out who I am right now.",
             "Sleep is exactly what you need. Identity can wait until you are rested. Give yourself full permission to just close your eyes and rest.")
        ]
    },
    "emotional_numbness": {
        "starts": [
            ("I feel completely hollow inside. Things that used to make me happy or sad just don't register anymore.",
             "That profound emptiness is often your body's way of shutting down after feeling too much for too long. It's a protective numbness. How long have you felt this emotional disconnect?"),
            ("I know I should be upset about this, but I literally feel nothing. It's scaring me.",
             "It is scary when our emotional reactions don't match the situation, but feeling 'nothing' is actually a very loud signal from your nervous system. It's saying it's overloaded. Can you feel any physical sensations in your body right now?"),
            ("I'm just going through the motions of life. I feel like a robot.",
             "Living like a robot is a survival strategy when the emotional weight of life becomes unbearable. You've had to disconnect to keep functioning. Does anything at all pierce through that numbness, even slightly?")
        ],
        "mids": [
            ("I just feel tired. So deeply tired. But not sad or happy. Just empty.",
             "That deep tiredness makes complete sense. Numbing out takes a massive amount of subconscious energy. What would happen if you just surrendered to the tiredness today instead of fighting it?"),
            ("I sometimes feel a spark of irritation, but that's it. Then it's back to nothing.",
             "Irritation is actually a sign of life underneath the numbness. It means the system isn't completely shut down. When that irritation flares up, what is it usually directed toward?"),
            ("I just want to feel something again. Even if it's pain, I'd prefer it to this emptiness.",
             "The emptiness can be more agonizing than active pain because it feels so isolating. It's okay to crave connection to your own feelings. What is a small, sensory experience you could try right now? Like holding ice or drinking warm tea?")
        ],
        "endings": [
            ("I'll try the warm tea. Just focusing on the heat in my hands. Thanks.",
             "Focusing on the simple heat of the tea is a wonderful, gentle way to connect back to your physical senses. I hope it brings a small moment of grounding."),
            ("I don't think I can force it. I guess I just have to wait it out.",
             "You are absolutely right. You cannot force emotions to return, and waiting it out with self-compassion is often the best approach. Be gentle with yourself in this quiet space."),
            ("I'm going to try to sleep. The numbness is just exhausting.",
             "The numbness is deeply exhausting. Sleep is a safe place to go when you are running on empty. Allow yourself to rest completely.")
        ]
    },
    "self_worth_struggles": {
        "starts": [
            ("I just feel like I'm not good enough at anything. No matter how hard I try, I always fall short.",
             "That feeling of 'never enough' is incredibly heavy to carry. It sounds like you hold yourself to an impossibly high standard. Where do you think that standard comes from?"),
            ("Someone criticized my work today and it completely shattered me. I feel completely worthless.",
             "When we already struggle with self-worth, criticism doesn't just feel like feedback on a project; it feels like an attack on our identity. It makes sense that you feel shattered. What was your immediate physical reaction to the comment?"),
            ("I look at everyone else and they seem so capable. I feel like an imposter in my own life.",
             "Imposter syndrome thrives in isolation and comparison. It tricks you into believing everyone else has a manual for life that you didn't receive. What is one thing you have survived or accomplished that you often brush off?")
        ],
        "mids": [
            ("I just feel like a disappointment. Like people only tolerate me.",
             "Believing that you are only 'tolerated' is a very painful narrative. It isolates you even when you're with people. What if, for just a moment, we considered the possibility that your presence actually brings value to others?"),
            ("I immediately wanted to cry and hide. It just confirmed everything bad I think about myself.",
             "The urge to hide is your body wanting to find safety. The criticism acted as a painful confirmation bias for those harsh inner thoughts. Can you think of one piece of evidence, no matter how small, that contradicts those bad thoughts?"),
            ("I don't know, I just expect perfection. If it's not perfect, I failed.",
             "Perfectionism is often a shield we use to protect ourselves from shame or rejection. But it's a shield that eventually crushes you with its weight. What does 'good enough' look like to you, without the pressure of perfection?")
        ],
        "endings": [
            ("I guess 'good enough' is just getting it done. I need to practice believing that.",
             "Practicing the belief in 'good enough' is a lifelong journey, but a very worthwhile one. You don't have to be perfect to be valuable. Take care today."),
            ("It's hard to see evidence against the bad thoughts right now. I just feel down.",
             "It is very hard to see the light when you are in the thick of the darkness. You don't have to force yourself to see it right now. It's okay to just feel down today."),
            ("I'm going to try to talk to myself like I'd talk to a friend. I know I'm being harsh.",
             "That is a profound shift in perspective. Treating yourself with the gentleness you'd offer a friend is a powerful step in rebuilding self-worth. You deserve that kindness.")
        ]
    },
    "burnout": {
        "starts": [
            ("I'm so exhausted I can barely keep my eyes open, but I have so much to do.",
             "It sounds like you're running on completely empty right now. When you're that depleted, even small tasks feel monumental. How long have you been feeling this exhausted?"),
            ("Every day feels like I'm dragging myself through mud. I just don't care about my projects anymore.",
             "That loss of caring is a very classic sign of deep burnout. It's incredibly heavy to feel like you're just dragging yourself along. What happens when you try to take a break?"),
            ("I stare at my screen and nothing happens. My brain is just static.",
             "That 'static' feeling is your brain's way of saying it has reached absolute capacity. It's protecting itself by shutting down. Are you in a place where you can safely step away for a few minutes?")
        ],
        "mids": [
            ("If I step away, I just feel anxious about falling behind. The guilt eats me alive.",
             "It's a cruel cycle when exhaustion demands rest, but anxiety prevents it. That guilt is lying to you, though. Rest is a biological requirement, not a reward. What is the smallest, lowest-effort thing you could do right now?"),
            ("I don't know how to take a break anymore. My mind just keeps racing.",
             "It sounds like your nervous system is stuck in 'go' mode, even though your energy is gone. When your mind races like that, what is it usually focused on?"),
            ("I just feel like I'm failing everyone because I can't keep up the pace.",
             "Carrying the expectation of others on top of your own burnout is an immense weight. You aren't failing; your body is simply setting a hard limit. Who is the most understanding person in your life right now regarding this?")
        ],
        "endings": [
            ("I guess I just need to close the laptop and try to breathe for a minute. Just getting through the emails is enough for today.",
             "Closing the laptop is a massive victory today. Acknowledging that 'enough is enough' is exactly what you need. Wishing you a peaceful, quiet evening."),
            ("I still feel overwhelmed honestly. I don't know if anything will help.",
             "It makes complete sense that you still feel overwhelmed. Burnout doesn't vanish in an instant. It's okay to just sit with that heavy feeling tonight without trying to fix it."),
            ("Maybe I just need rest. True rest without my phone.",
             "True, disconnected rest sounds profoundly necessary for you right now. I hope you can give yourself permission to just 'be' tonight.")
        ]
    },
    "loneliness": {
        "starts": [
            ("I spent the whole weekend alone and didn't speak a single word out loud. It just hit me how isolated I am.",
             "Going a whole weekend without speaking to anyone can definitely make that loneliness feel so loud and heavy. How did you end up spending that quiet time?"),
            ("Even when I'm in a room full of people, I feel like I'm completely by myself. Nobody really sees me.",
             "Feeling alone in a crowded room is a very specific, sharp kind of ache. It sounds like you're craving a much deeper, authentic connection. What does being 'seen' look like to you?"),
            ("I have acquaintances, but no one I can truly open up to about how exhausted I am.",
             "That surface-level interaction can sometimes make the internal isolation feel even worse. It's exhausting to not have a safe harbor to just vent. Do you feel like you have to mask your real emotions around them?")
        ],
        "mids": [
            ("I mostly just binge-watched shows and scrolled through social media, which honestly just made me feel worse.",
             "Social media has a tragic way of amplifying our loneliness by showing us highlight reels of other people's connections. When you think about a weekend that would feel fulfilling, even alone, what comes to mind?"),
            ("It feels deeper. I just feel like I'm faking my personality to fit in, so no one actually knows the real me.",
             "That is incredibly tiring, having to mask your true self just to feel accepted. It makes sense that you feel disconnected. What is one aspect of your real personality that you feel you have to hide?"),
            ("I feel like my sense of humor is too weird, or that I'm too sensitive, so I just stay quiet.",
             "Many people who feel they are 'too sensitive' or 'weird' are actually incredibly perceptive and empathetic. Suppressing those qualities to fit in denies the world your unique perspective. How might it feel to test the waters and share a small, genuine thought with someone?")
        ],
        "endings": [
            ("I might try sharing a bit more of my real opinions with my coworker tomorrow. Start small.",
             "Starting small is the perfect approach. Showing a little bit of your authentic self is a brave step toward real connection. I hope it goes well."),
            ("I don't know if I have the energy to reach out to anyone right now. I'm just so tired of trying.",
             "It is completely okay to not have the energy right now. Reaching out takes vulnerability and effort. It's okay to just rest in your own company tonight without any pressure to change it."),
            ("I think I'll get my paints out tonight. It feels better to create something than to just consume content.",
             "Getting the paints out sounds like a beautiful act of self-care. Enjoy the process of creating something just for you.")
        ]
    },
    "anxiety": {
        "starts": [
            ("My chest feels so tight today. I can't stop worrying about everything. My brain is running a million miles an hour.",
             "It sounds like you're carrying a lot of physical tension right now, and that tight chest can be really uncomfortable. Are you in a place where you can take a slow, deep breath with me right now?"),
            ("I'm so anxious about tomorrow. What if everything goes wrong? I keep replaying different scenarios.",
             "It sounds like the uncertainty of tomorrow is weighing really heavily on you, causing your mind to work overtime. Replaying worst-case scenarios is very draining. What specific part of tomorrow feels the most daunting?"),
            ("I have this sinking feeling in my stomach and I don't even know why. Everything just feels wrong.",
             "That sinking feeling can be so unsettling, especially when you can't pinpoint the exact cause. It's like an internal alarm bell going off. Has anything happened recently that might have triggered this?")
        ],
        "mids": [
            ("It's just a constant loop of 'what ifs'. I have a big presentation and I'm terrified I'll forget everything.",
             "Those 'what if' loops can be exhausting to get caught in. It makes total sense that you're nervous about a big presentation. What usually helps you feel a bit more anchored when your mind gets stuck like this?"),
            ("I feel like I can't take a deep breath. Nothing specific happened, I just woke up feeling on edge.",
             "Waking up on edge is really tough because you haven't even had a chance to start your day before the anxiety hits. It can sometimes help to gently shift focus. Can you name three things you can see around you right now?"),
            ("I just keep imagining the worst possible outcomes. Taking a breath helps a tiny bit, but the thoughts rush back.",
             "It's a very human response for the mind to jump to worst-case scenarios when we feel stressed. Since the thoughts keep rushing back, what if we try observing them without fighting them? Just acknowledging 'I am having an anxious thought'.")
        ],
        "endings": [
            ("Just getting it out of my head makes it slightly better. Maybe I need to do a practice run of the presentation.",
             "It sounds like expressing it is giving you a little bit of breathing room. A practice run sounds like a practical way to build your confidence. How about you do one run-through, and then consciously step away to rest?"),
            ("I don't know, maybe I need to try some deep breathing. I see my coffee mug, my notebook, and the window. It helps ground me a bit.",
             "Naming what you see is a great way to signal to your nervous system that you are safe in this present moment. Deep breathing can also gently continue that calming process. I hope you find some peace today."),
            ("I'm still really tense, to be honest. I guess I just have to ride it out.",
             "Sometimes riding it out is the only thing we can do. It's incredibly uncomfortable, but it will eventually pass. Be gentle with yourself while you're in the thick of it.")
        ]
    },
    "academic_pressure": {
        "starts": [
            ("I have three exams next week and I feel like I'm going to fail all of them. The anxiety is paralyzing.",
             "It sounds like you're carrying a tremendous amount of academic pressure right now. It's completely understandable that you're feeling paralyzed. Have you been able to take any breaks, or has it been non-stop studying?"),
            ("I study for hours but nothing seems to stick in my brain. I feel like I'm just not smart enough for this program.",
             "It can feel so discouraging to put in hours of effort and feel like you aren't seeing results. Please know that struggling to retain information when you're stressed is a reflection of your cognitive load, not your intelligence. Have you tried changing your study methods?"),
            ("I'm so behind on my coursework. I don't even know where to begin, so I just avoid looking at it.",
             "That feeling of being behind can create a massive wall of overwhelm. Avoidance is a very common coping mechanism when we don't know where to start. If you were to look at your syllabus, what is the single smallest, easiest task you could identify?")
        ],
        "mids": [
            ("It's been non-stop, but mostly I just stare at the pages and panic. I haven't really absorbed anything.",
             "When we are in a state of panic, our brains actually struggle to encode new information. It's like trying to pour water into a full cup. What if you gave yourself absolute permission to take one hour completely off from studying?"),
            ("I usually just re-read the textbook, but my eyes just glaze over. I feel so defeated.",
             "Re-reading is a common strategy, but it can be very passive, especially when you're exhausted. Active recall or teaching the material to someone else can sometimes engage the brain differently. Would you be open to trying a different technique for just 20 minutes?"),
            ("The easiest task would probably be just organizing my notes for one class, but even that feels like a lot.",
             "Organizing notes is a fantastic place to start because it requires less intensive focus. It's okay if it still feels heavy. What if you promised yourself you only had to organize for 10 minutes, and then you could stop if you wanted?")
        ],
        "endings": [
            ("Ten minutes I can do. I'll set a timer. If I know I can stop, it doesn't feel as impossible.",
             "Setting a timer is a brilliant strategy. It lowers the stakes completely. Overcoming the inertia of starting is often the hardest part. How will you reward yourself after those 10 minutes?"),
            ("I guess taking an hour off might actually help. I've just been sitting here panicking anyway.",
             "Exactly. Time spent panicking at a desk isn't effective studying anyway, so stepping away is a strategic move, not a lazy one. What calming activity will you choose for your hour off?"),
            ("I don't know if I can even do that. I'm just so tired. I think I'm just going to sleep.",
             "Sleep sounds like the most responsible and healthy choice you could make right now. Your brain needs rest to process everything anyway. Give yourself permission to sleep without guilt.")
        ]
    },
    "workplace_stress": {
        "starts": [
            ("I feel like I'm constantly walking on eggshells around my team. One person in particular always belittles my contributions.",
             "Walking on eggshells is an exhausting way to live, especially in a professional environment. Having your contributions belittled is a form of workplace bullying. When this person undermines you, does anyone else in the room support you?"),
            ("The workload just never ends. As soon as I finish one impossible task, three more are assigned to me.",
             "That relentless pace sounds incredibly demoralizing. It's like trying to empty the ocean with a bucket. Have you had any conversations with your manager about the unmanageable volume of work?"),
            ("I made a mistake today at work and I can't stop obsessing over it. I feel like I'm going to be fired.",
             "It's awful when that fear of losing your job takes over. Our brains tend to catastrophize when we make mistakes. Was it a mistake that can be fixed, or has it already caused a major issue?")
        ],
        "mids": [
            ("Most people just look down at their notebooks. Nobody says anything. It makes me feel like everyone agrees with the bully.",
             "That silence from others can absolutely feel like complicity, and that multiplies the hurt. Often, bystanders are also afraid of becoming the target. Have you thought about documenting these incidents privately?"),
            ("My manager is the one assigning it. If I push back, I'm seen as 'not a team player'.",
             "That puts you in a very difficult, unfair position where setting a reasonable boundary is penalized. It's a toxic dynamic. How is this constant pressure affecting your life outside of work?"),
            ("It can be fixed, but I just feel so stupid for missing it. I should have known better.",
             "Feeling 'stupid' is a heavy label to put on yourself for a fixable human error. Everyone, even the most experienced professionals, makes mistakes. How would you respond to a colleague if they made the exact same error?")
        ],
        "endings": [
            ("I think I want to say, 'What did you mean by that?' next time they make a comment. I just need the courage.",
             "Asking 'What did you mean by that?' is an excellent, assertive strategy. It calmly puts the spotlight back on their behavior. It takes practice to find that courage, but you are taking a brave step."),
            ("I don't know what to do. I'm just going to try and get through the week and then maybe look at other jobs this weekend.",
             "Looking at other jobs sounds like a very proactive way to reclaim some control over your situation. You deserve to work in an environment that doesn't drain you completely. Take it one day at a time."),
            ("I guess I'd tell a colleague it's okay and we can fix it. I need to be that kind to myself, it's just hard.",
             "It is very hard to turn that compassion inward, but recognizing that you deserve the same grace you'd offer a friend is a huge step. Be gentle with yourself today.")
        ]
    },
    "uncertainty": {
        "starts": [
            ("I feel completely lost in my life right now. I don't know what I'm doing or where I'm going.",
             "Feeling lost is a profoundly unsettling experience. It's like standing in the middle of a dense fog without a compass. What specifically feels the most uncertain to you right now—career, relationships, or just everything?"),
            ("Everyone around me seems to have their lives figured out, and I'm just stumbling in the dark.",
             "It's so easy to look at others and see the 'finished product' while you're intimately aware of all your own messy behind-the-scenes struggles. That comparison can be so painful. Have you always felt this uncertain, or is this a recent phase?"),
            ("I have to make a huge decision soon and I'm terrified of making the wrong choice.",
             "Big decisions carry so much weight, and the fear of making the 'wrong' one can totally paralyze you. What happens in your body when you try to think about this decision?")
        ],
        "mids": [
            ("It's kind of just everything. My career feels stagnant, my social life is quiet, and I just feel stagnant.",
             "When everything feels stagnant at once, the overwhelming urge is often to make a drastic change, which can be scary. What if you just allowed yourself to be in this 'in-between' space for a little while without forcing an answer?"),
            ("It's been building up since I graduated. I thought I'd feel like an adult by now, but I just feel like a kid playing dress-up.",
             "That 'imposter syndrome' of adulthood is incredibly common. The truth is, most people are figuring it out as they go. What is one thing, however small, that you feel genuinely confident doing?"),
            ("My stomach drops and my heart races. I just want someone else to tell me what to do.",
             "That intense physical reaction shows just how much pressure you're putting on yourself. Wanting someone else to take the wheel is a very normal desire when you're overwhelmed. What are the core values driving this decision?")
        ],
        "endings": [
            ("Maybe I can just focus on getting through today. The big picture is too much right now.",
             "Narrowing your focus to just today is a very wise and self-protective strategy. You don't have to figure out the rest of your life right now. Just take care of yourself today."),
            ("I guess I do know how to be a good friend. That's something, at least.",
             "Being a good friend is a profound and deeply valuable skill. That is absolutely something to be proud of, and it proves you have a strong foundation, even when other areas feel uncertain."),
            ("I don't know my values right now. I'm just so confused. I think I need to just stop thinking about it for tonight.",
             "Stopping the cycle of overthinking for tonight is a very healthy boundary. The decision will still be there tomorrow, but tonight, you are allowed to just rest your mind.")
        ]
    },
    "bullying": {
        "starts": [
            ("There's a group that constantly goes out of their way to exclude me and make jokes at my expense. It hurts so much.",
             "It is deeply painful to be deliberately excluded and mocked. That kind of behavior from others is cruel, and it makes sense that you're hurting right now. Is there anyone you feel safe talking to about this?"),
            ("I'm getting targeted online. People are leaving nasty comments and I feel completely exposed and attacked.",
             "That sounds terrifying and deeply unfair. Being targeted online can feel like an invasion of your personal space. Please know their behavior is a reflection of them, not you. Have you considered stepping back from the platform for a few days?"),
            ("I reported someone for harassing me, and now everyone is treating me like I'm the problem. I feel so alone.",
             "That is an incredibly unjust and isolating situation. You did the brave, right thing by reporting it, and being retaliated against socially is a form of secondary bullying. How are you taking care of yourself amidst this backlash?")
        ],
        "mids": [
            ("I have one friend, but they don't see it happen. I feel really isolated.",
             "It's really isolating when the people who care about you aren't there to witness what's happening. I'm glad you have at least one friend you can lean on. Do you think you might have the energy to document these incidents?"),
            ("I haven't logged off because I feel like if I do, they win. But reading the comments is making me sick.",
             "It takes a lot of strength to want to stand your ground, but protecting your mental health doesn't mean 'they win.' It means you are choosing yourself over their negativity. How would it feel to mute them or make your accounts private temporarily?"),
            ("I'm not taking care of myself. I'm barely eating and I just cry when I get home.",
             "Your body and mind are going through a trauma response to this ongoing stress. It makes sense that eating feels impossible and that you're crying so much. What is the gentlest, smallest comforting thing you could do for yourself tonight?")
        ],
        "endings": [
            ("I haven't thought about writing it down. Maybe keeping a record would make me feel less crazy. It's just exhausting.",
             "Keeping a record can be incredibly validating because it takes the incidents out of your head and puts them on paper as facts. It is exhausting, so please be gentle with yourself as you navigate this."),
            ("I guess you're right. Muting them might give me a break. I just hate that people can be so cruel for no reason.",
             "It is profoundly unfair that people act with such cruelty, and it's okay to grieve the lack of kindness you're experiencing. Muting them is a powerful way to reclaim your space. Take care of yourself tonight."),
            ("I don't know what to do anymore. I'm just so incredibly tired.",
             "I hear how deep that exhaustion goes. You don't have to figure out a solution right now. It is okay to just be tired, to wrap yourself in a blanket, and to just survive the evening.")
        ]
    },
    "grief": {
        "starts": [
            ("I lost someone recently and the pain is so heavy I can barely breathe. I don't know how to keep going.",
             "I am so incredibly sorry for your loss. That kind of deep, breathtaking pain is a testament to how much love was there. It's completely understandable that you don't know how to keep going right now. Are you alone today?"),
            ("It's been a year, but today it feels like it just happened all over again. I'm just sobbing uncontrollably.",
             "Grief has a way of ambushing us, regardless of how much time has passed. Anniversary reactions, or even just random days, can bring the raw pain right back to the surface. It is completely okay to sob and let it out. How does your body feel right now?"),
            ("Everyone else seems to have moved on, but I'm still stuck. I feel like I'm grieving wrong.",
             "There is absolutely no 'wrong' way to grieve, and there is no timeline you have to follow. It can feel very isolating when the world keeps spinning and your world has stopped. What is one thing you miss the most about them today?")
        ],
        "mids": [
            ("I'm alone. I just wanted to be by myself, but now the quiet is suffocating.",
             "The quiet can become deafening when you're alone with that much grief. It makes sense that you wanted isolation, but also find it painful. Would it help to just have some gentle background noise, like soft music or a nature documentary?"),
            ("I just feel hollowed out and completely exhausted. My head is pounding.",
             "Crying that deeply takes a massive physical toll on the body. You are physically exhausted from the emotional labor of grieving. Could you drink a glass of water and maybe lie down, even if you don't sleep?"),
            ("I just miss hearing their laugh. It feels like I'm forgetting the sound of it, and that panics me.",
             "The fear of forgetting is a very painful part of grief. The panic is your heart trying to hold on tightly to them. Do you have any videos or voicemails where you can hear their voice, or is it too painful to listen right now?")
        ],
        "endings": [
            ("I might put a familiar show on low volume. Just to not feel so completely alone in the silence.",
             "Putting on a familiar show is a gentle, comforting way to break the silence without requiring any energy from you. I hope it brings you a tiny bit of comfort in the heaviness."),
            ("I think I'll try to drink some water. I just feel so broken.",
             "You are carrying a broken heart, and it's okay to feel that way. Drinking water is a beautiful, simple act of caring for yourself while you carry this immense pain. Take it one gentle moment at a time."),
            ("It's too painful to listen right now. I just need to cry some more.",
             "Then please, give yourself the grace to just cry. The tears are a physical release of the love you still hold for them. I am holding space for you and your grief today.")
        ]
    }
}

def generate_conversation():
    theme = random.choice(themes)
    bank = dialogue_banks[theme]
    num_turns = random.choice([2, 3, 4, 5])
    conversation = []
    
    start_u, start_m = random.choice(bank["starts"])
    conversation.append({"role": "user", "content": start_u})
    conversation.append({"role": "model", "content": start_m})
    
    if num_turns > 2:
        mids_selected = random.choices(bank["mids"], k=num_turns - 2)
        for mid_u, mid_m in mids_selected:
            conversation.append({"role": "user", "content": mid_u})
            conversation.append({"role": "model", "content": mid_m})
            
    end_u, end_m = random.choice(bank["endings"])
    conversation.append({"role": "user", "content": end_u})
    conversation.append({"role": "model", "content": end_m})
    
    return {"messages": conversation}

dataset = []
for _ in range(6000):
    dataset.append(generate_conversation())

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(dataset, f, indent=2)

print(f"Generated {len(dataset)} realistic multi-turn conversations.")
