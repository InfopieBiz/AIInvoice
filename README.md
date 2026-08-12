# Password Checker 

A command line Python app to demonstrate the fundamentals of password security.

It allows users to check the strength of their password, how weak passwords are guessed with dictionary and brute-force demos and how passwords should be securely stored.

## What have been done until now

### Phase 1 - Application setup > Complete

The application so far includes:

* Project folder structure 
* Main menu is working
* An ethical usage 
* Navigation between placeholder screens
* Menu option input validation 
* A safe exit strategy

### Phase 2 - Password Strength Analyzer > Complete 

#### Stage 1 - Basic Password Checks 

    Completed:
    * Secure hidden password input
    * Empty-input validation
    * Password-length checking, and checks for lowercase letters, uppercase letters, numbers, and special characters
    * The results are displayed in the terminal using PASS or FAIL

#### Stage 2 - Strength Scoring 

    Completed: 
    * Scoring based on password length
    * Character-variety points
    * Strength Rating ( Very Weak - Very Strong )
    * Structured analysis results using dataclass

#### Stage 3 - Common Password Detection 

    Completed: 
    * Detect exact common passwords
    * Detection of common password words within longer passwords
    * Character-substitution normalization
    * Detection of easily guessed passwords like P@ssw0rd123
    * Penalties for common and predictable passwords

#### Stage 4 - Advanced Pattern Detection 

    Completed: 
    * Detection of sequential characters (like abc, 123, and 321)
    * Detection of keyboard patterns (such as qwerty and asdf)
    * Detection of repeated characters (like aaa and 111)
    * Detection of repeated words or blocks (such as abcabc and passpass)
    * Detection of predictable endings (such as 123, 1234, and years)
    * Score penalties for every predictable pattern detected

#### Stage 5 - Personalized Recommendations

    Completed: 
    * Password length recommendations
    * Suggestions for missing lowercase, uppercase letters, numbers, and special characters
    * Common Passwords and Common Password Words Warnings
    * Warnings about sequential characters and keyboard patterns
    * Warnings for repeating characters, repeating blocks, and predictable endings
    * Tips on how to make your passwords unique
    * Recommendation to use a password manager you trust

#### Stage 6 - Final CLI integration and polish

    Completed: 
    * Clean and formatted results screen
    * Detailed Results for characters and patterns
    * Success and warning messages
    * Clear-screen and pause helpers
    * Local password reference removed after analysis
    * Final testing and code cleanup

### Phase 3 - Dictionary Attack Simulator > Complete

#### Stage 1 - Wordlist Configuration and Loader

    Completed:
    * Added a local common-password wordlist
    * Set the wordlist path using pathlib
    * Added UTF-8 loading, including blank-line removal
    * Added controlled handling for missing, unreadable, invalid and empty files

#### Stage 2 - Dictionary Comparison Engine

    Completed:
    * Added a structured attack result using a frozen dataclass
    * Added exact and case sensitive password comparison
    * Added attempt counter and total candidate tracking
    * Added time measurement using perf_counter
    * Added immediate stopping when a match is found
    * Added average attempts-per-second calculation
    * Manual Testing of found, not-found, case-sensitive, and attempt-count results

#### Stage 3 - Interactive Dictionary Attack Screen

    Completed:
    * Secure loading and setup of local wordlists
    * Dictionary comparison, case sensitive and exact
    * Secure hidden password input and validation
    * Found and not-found result display
    * Calculation of attack-rate and security advice
    * Safe wordlist error handling through the CLI

#### Stage 4 - Final Testing and Documentation

    Completed:
    * Performed extensive manual testing of Dictionary Attack Simulator
    * Found and not found password results verified
    * Verified case sensitive comparison, execution time and attempt counting
    * Validation for blank input and max length of password
    * Verified missing and empty wordlist error handling

### Phase 4 - Automatic Brute-Force Attack Simulator > In Progress

#### Stage 1 - Brute-Force Foundations

    Completed:
    * Added safety limits for brute-force testing
    * Added validation for the maximum password length
    * Added eight character sets to test in order
    * Added a result structure for brute-force attempts
    * Added theoretical search-space calculation
    * Added memory-efficient password combination generation
    * Added checks to match passwords with the correct character set

#### Stage 2 - Single-Charset Brute-Force Engine

    Completed:
    * Added the core brute-force search engine for one character set
    * Added exact case sensitive password comparison
    * Added attempt count and execution time
    * Added timeout and max attempts stops 
    * Added character set compatibility checking
    * Added safe cancellation and search-exhausted handling
    * Added structured brute-force results

#### Stage 3 - Automatic All-Charset Controller

    Completed:
    * Added automatic testing of supported character sets, in order
    * Added skipping of incompatible character sets with zero attempts
    * Added global attempt and timeout limits to all charsets
    * Added auto stop when password is found
    * Added safe stop for cancel, timeout and max attempts
    * Added maximum length check before brute-force testing

### In the next stages

The following will be implemented:
* Build the Interactive CLI and Reporting
* Complete Testing, Documentation and Final Verification

## In the next phases

The following will be implemented:
* Secure Password Storage
* Results Dashboard

## Prerequisites 
* Python 3.10+
* No external python packages needed 

## Start the app

1. Activate the virtual environment
   
macOS or Linux - source .venv/bin/activate

Windows - .venv\Scripts\activate.bat

2. Run the app

python main.py

On some systems, you may need to use:

python3 main.py

## VERY IMPORTANT NOTE:

This is for educational purpose only in the Cybersecurity field.

The dictionary and brute-force features will be demonstration-only controlled, where the passwords will be entered directly in the local application. The intention is not to attack real accounts, websites, devices, networks or systems.