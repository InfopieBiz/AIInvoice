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

### Phase 2 - Password Strength Analyzer > in progress 

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
    

#### To be completed in the next stages: 
    * Advanced pattern detection
    * Personalized recommendations
    * Final CLI integration and polish
    
## In the next phases

The following will be implemented:
* Dictionary Attack Simulator
* Brute Force Attack Simulator
* Secure Password Storage
* Results Dashboard

## Prerequisites 
* Python 3.10+
* No external python packages needed for Phase 1

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
