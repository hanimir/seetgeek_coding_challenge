# Section Normalization

This package contains my solution to the SeatGeek Section Normalization Code Challenge, in the same format as the challenge was given to me.

## Solution Approach

Before starting to code, I took a look at some of the manifest and training/testing data that was given, to get an idea of what types of row/section names would be inputted, and what the manifest contains. I noticed that most of the input sections followed the following formats, assuming that the matching section in the manifest has the name *Reserve 15*:

  1. *Preferred Reserve 15* - In this case, the input section name was a string containing many of the same words that the matching section had in the manifest.
  2. *15PR* or *PR15* - In this case, the input section name contained an acronym or small subsequence of the name of the matching section from the manifest.
  3. *15* - In this case, the input section name was just a number which matched the numbers in the section name from the manifest (although the section name in the manifest may have had more words beyond that).

These input formats accounted for the majority of the data, so I chose to use those heuristics in my normalization algorithm.

### Note: I understand that there may be more sophisticated algorithms (specifically machine learning algorithms) which may perform the normalization more accurately on a larger, more diverse dataset, but I felt that that was outside of the scope of this challenge.

So, based on the previously mentioned input formats, my normalization algorithm does three things:

  1. Checks if any of the numbers from the inputted section name match any of the numbers in the section names from the manifest. Any sections from the manifest which matched were put into a set, which we'll call `S1` for the purposes of this description.
  2. Checks if any of the words from the inputted section name match any of the words in the section names from the manifest. Any sections from the manifest which matched were put into a set, which we'll call `S2` for the purposes of this description.
  3. Checks if any of the words from the inputted section name were a subsequence of any of the section names from the manifest. This is to account for acronyms and small subsequences, as described in #2 of the input formats above. Any sections from the manifest which matched were put into a set, which we'll call `S3` for the purposes of this description.

Then, to determine the matching section (if it exists), the algorithm checks for sections which appear in `S1` and (`S2` or `S3`). These would be sections which matched a number as well as either a word or a subsequence of the section name. This is what I considered to be a strong indicator that the section was indeed a match. If no sections fit this criteria, the algorithm simply returns all sections which matched on any of the three criteria. If more than one section matched based on the previously described criteria, then it was not possible to normalize the ticket.

## Results
My solution was able to score 2000/2000 on my tests of Dodger Stadium and Citifield, using the given test script, [genericgrader.py](./genericgrader.py).
