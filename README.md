# Oh, you know what would be fun?
## Generating a Graphviz dot-file for every possible permuation of an eight-puzzle

*Oh man that would be awesome right?* Just a sprinkling of a [BFS](http://en.wikipedia.org/wiki/Breadth-first_search)
checking out all the nodes from the start position.

## So how about some Python?

I bet if you were to run `python generate.py > eight-puzzle.dot` after a couple 
minutes you would hit **181439** nodes found and some nice, well-formed dot-file
goodness will appear, directed even!

## How about generating a PNG?

Dunno yet, this thing is HUGE. **423362** lines in a **22M** text file. Will
update when I learn the correct incantation for `sfdp` that gets a pretty file.