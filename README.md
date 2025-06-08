# How it works
The algorithm favours:
1. For each section, favours earliest applicant who places it the highest on their preference.
2. Early applicants.

After that, there will be switchings to make sure all sections meet their quota.

`tests` folder contains data used for testing. Go to `tests/tests` to see input format.

# Advantages
1. It is relatively fair in terms of what it favours
2. Make sure all sections meet their quota. i.e. the algorithm tries its best to ensure no section is left unattended

# What can be improved?
A LOT. I wrote this in like 5 days ok.

1. Biggest red flag is that slots and people are currently identified using their index in a list. (I am so, so sorry. It hurts me to see it too).
Improvement: Each Person/SLot object should be identified using a unique ID.

2. Artist and Writer mode. Currently it's just hardcoded and needs to be changed manually in the code before running.
Improvement: It can take execution mode as an argument from input (command line,...).

3. File path to data. Currently it's just hardcoded and needs to be changed manually in the code before running. Also currently it can only read `.csv` files.
Improvement: It can take file path an argument from input (command line,...).

4. Repeating chunks of code. Yeah, there is A LOT.
Improvement: Refactoring. I just don't have time.

5. Bad naming convention. I am, once again, sorry.

6. Messy log. The log file was intended to be read by me only so it's probably not really helpful for you.