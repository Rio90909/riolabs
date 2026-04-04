import re

with open('index.html', 'r') as f:
    html = f.read()

# Stop Timer - Reduce wait to 1.5 seconds instead of 3.
html = html.replace('start: Date.now() + 3000', 'start: Date.now() + 1500')

# Reaction Tap - Reduce wait to 1.5 + Random(2s) instead of 3 + Random(5s)
html = html.replace('greenTime: Date.now() + 3000 + Math.random()*5000', 'greenTime: Date.now() + 1500 + Math.random()*2000')

# Stop Timer & Reaction Tap interval ticks from 100ms to 50ms so state updates feel faster.
html = html.replace('}, 100);', '}, 50);')

# Matchsticks interval is not an interval, it's instant Firebase update.

# Coin Flip spin time. It's using CSS transition.
# We will reduce the setTimeout resolve wait from 1000ms to 300ms, and change the CSS transition on the coin to 0.3s.
html = html.replace('setTimeout(() => {\n                        gameRef.update({ result: res, winner: win });\n                    }, 1000);', 'setTimeout(() => {\n                        gameRef.update({ result: res, winner: win });\n                    }, 400);')
html = html.replace('transition: transform 1s ease-in-out;', 'transition: transform 0.4s ease-in-out;')

# High Card draw delay doesn't exist, it's instant.

with open('index.html', 'w') as f:
    f.write(html)
