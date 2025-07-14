{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Initial thoughts", "initial-thoughts")}}

{{text("In this challange, we get a binary file and instructions on how to run it locally.")}}

{{text("Let's begin by trying to run it.")}}

{{image("../../static/writeups/sneakytrain/images/000001.jpg")}}

{{text("We are greeted with a title screen for the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Sneaky Train</code> game, which is just a copy of snake.")}}

{{text("If we keep on playing the game as intended, we notice that the game freezes upon eating the fourth <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>$</code>.")}}

{{header("Reverse engineering", "reverse-engineering")}}

{{text("We continue by loading the program into <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>IDA</code> or <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Ghidra</code> and try to reverse engineer it.")}}

{{image("../../static/writeups/sneakytrain/images/000002.jpg")}}

{{text("Firstly, we see is that the application sets a lot of vague parameters.")}}

{{text("We scroll a little further and see the first interesting thing.")}}

{{image("../../static/writeups/sneakytrain/images/000003.jpg")}}

{{text("It copies the string <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>orfsshxxxx</code> into the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>v30</code> parameter. I renamed it into <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>weird_string</code> so we can read the code more clearly.")}}

{{text("Scrolling even more, we see a mention of <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>flag.txt</code>.")}}

{{image("../../static/writeups/sneakytrain/images/000004.jpg")}}

{{text("It opens a file named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>flag.txt</code> and copies it contents into the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>v126</code> parameter. I renamed it as well.")}}

{{text("Below, we see the screen that was shown to us when we run the binary.")}}

{{image("../../static/writeups/sneakytrain/images/000005.jpg")}}

{{text("Finally, we get to what is probably the main game loop.")}}

{{image("../../static/writeups/sneakytrain/images/000006.jpg")}}

{{text("Remember, when we ate the fourth <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>$</code>, the game crashed. That means when <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>train_length is 5 = crash</code>.")}}

{{text("We clearly see the line <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>if ( std::deque<std::pair<int,int>>::size(v125) == 5 )</code>. This is probably the statement that  froze our game.")}}

{{text("Then, we enter the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>while</code> loop, which ends if <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>v33</code> or <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>v43</code> is zero.")}}

{{text("After that, it reads one character from our input and saves it into <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>v31</code>.")}}

{{text("Lastly, it does some weird pointer deferencing, which is too much for my brain. However, the lines <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>v43 = (v43 + 7) / 10;</code> and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>v43 = v15 - 10 * v43;</code> both contain the number 10?")}}

{{text("Here was my theory, the game upon freezing starts to read our input which is probably supposed to be 10  characters long, from the number 10 used twice. If we type in the correct input, the game continues.")}}

{{text("You can probably see where this is going, but let's continue.")}}

{{image("../../static/writeups/sneakytrain/images/000007.jpg")}}

{{text("After that, it reads the length of our train again and if it's equal to length of the flag, something happens. My guess is - we get the flag.")}}

{{text("Cool, so we get to length of 5, input correct passphrase and get the flag. But what is the passphrase?")}}

{{text("Probably the string from the start, since it is also 10 characters long. We can try inputting <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>orfsshxxxx</code> and hope that the game continues.")}}

{{text("Spoiler: it did not continue.")}}

{{text("Let's make sure that the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>weird_string</code> parameter doesn't get altered along the way.")}}

{{text("If we go up, we can clearly see that the string gets altered in a couple of places.")}}

{{image("../../static/writeups/sneakytrain/images/000008.jpg")}}

{{text("I kept following our passphrase and I finally got <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>secretxxxx</code> as the final string.")}}

{{header("Final flag", "final-flag")}}

{{text("Run the game again, type in the phrase, continue playing, if the length of our snake is be equal to the length of the flag, we should get it.")}}

{{image("../../static/writeups/sneakytrain/images/000009.jpg")}}

{{script()}}