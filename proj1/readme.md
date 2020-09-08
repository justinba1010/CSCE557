# Approach

I wanted to be efficient so I used a genetic algorithm, a crudely implemented one at that. I first matched the ciphertext with letter frequencies of English. I first got a 26% english word match, which was much higher than I expected, and was a great starting point as I had a 10,000 word dictionary. I then randomly swapped 2 letters that were close by, as it would be unlikely that a z and a should be swapped considering their frequencies are so far apart. If I got to a local minima I would bump up the search space of the 2-swap heuristic. I felt that I might have needed to implement k-swap, as the ciphertext was in a way small, but it worked out with 2-swap. The genetic algorithm found the solution most of the time in less than 250,000 tries. I originally tried a crude genetic algorithm, but shortly found that it was not enough to only pick the best, so I expanded my "parents" and kept the best 10 at all times.

# Decryption

Most of the algorithm is simple frequency analysis and then just randomly tweaking the prospective key until we reach a slightly better guess. I wanted it to be mostly done by the `decipher.py`, as I felt it would be easier to do that then to do anything by hand. The genetic part of it is that I keep the 10 best scoring from the heuristic. Currently the heuristic is just how close the plaintext is to some set of english words, but by changing `KALPHAWEIGHT` we can change the weight of alphabetic over numeric characters, however I found that it was not needed.

Changing `KNUMRUNS` changes how many times it will guess within a certain 2-swap space, say 3 letters apart. This is just a heuristic that prioritizes small swaps as it is unlikely an e will be swapped with a z, unless say the plaintext is the Z page in the dictionary. Changing `KTOTALRUNS` will increase or decrease how long the algorithm will run. I found that 250,000 and 15,000 are a little overkill, but they typically find a good key in the 30-40 seconds it runs for. KSWAPSPACE I felt like it was useful to have as a global variable, because it starts at 1, which typically allows us to get the single letter words in place, or at least almost in place. Then by slowly increasing the 2-swap space we can begin to zero in. I think of it like shaking a jig-saw puzzle until a few pieces connect. If you have a local part that is working, but doesn't fit the rest of it, eventually we break it and re-arrange it, just through keeping 10 of the best matches. `KKEEP` changes how many matches we keep, I found 10 to be reasonable.

# Running the programs

Assuming the ciphertext is in `cipher.txt`, we run

`python3 decipher.py cipher.txt` or `./decipher.py cipher.txt`

Which will output its progress to stdout, and generate 10 key files. We can use the key files to decipher the ciphertext, or try our own key.

`python3 plaintext.py cipher.txt` or `./plaintext.py cipher.txt`

and for a defined key

`python3 plaintext.py cipher.txt ourOwnKey.txt` or `./plaintext.py cipher.txt ourOwnKey.txt`

# Plain text for 03

```
there has been a change of government it began two years ago when the house of representatives became democratic by a decisive majority it has now been completed the senate about to assemble will also be democratic the offices of president and vice president have been put into the hands of democrats what does the change mean that is the question that is uppermost in our minds today that is the question i am going to try to answer in order if i may to interpret the occasion it means much more than the mere success of a party the success of a party means little except when the nation is using that party for a large and definite purpose no one can mistake the purpose for which the nation now seeks to use the democratic party it seeks to use it to interpret a change in its own plans and point of view some old things with which we had grown familiar and which had begun to creep into the very habit of our thought and of our lives have altered their aspect as we have latterly looked critically upon them with fresh awakened eyes have dropped their disguises and shown themselves alien and sinister some new things as we look frankly upon them willing to comprehend their real character have come to assume the aspect of things long believed in and familiar stuff of our own convictions we have been refreshed by a new insight into our own life we see that in many things that life is very great it is incomparably great in its material aspects in its body of wealth in the diversity and sweep of its energy in the industries which have been conceived and built up by the genius of individual men and the limitless enterprise of groups of men it is great also very great in its moral force nowhere else in the world have noble men and women exhibited in more striking forms the beauty and the energy of sympathy and helpfulness and counsel in their efforts to rectify wrong alleviate suffering and set the weak in the way of strength and hope we have built up moreover a great system of government which has stood through a long age as in many respects a model for those who seek to set liberty upon foundations that will endure against fortuitous change against storm and accident our life contains every great thing and contains it in rich abundance but the evil has come with the good and much fine gold has been corroded with riches has come inexcusable waste we have squandered a great part of what we might have used and have not stopped to conserve the exceeding bounty of nature without which our genius for enterprise would have been worthless and impotent scorning to be careful shamefully prodigal as well as admirably efficient we have been proud of our industrial achievements but we have not hitherto stopped thoughtfully enough to
```