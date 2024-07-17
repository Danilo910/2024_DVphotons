
outg = 5
selection = [1, 2, 3]



print("Before the outer if statement")
if True:  # condition1
    print("Inside the outer if statement")

    come_frome_n = True
    if outg not in selection:
        come_frome_n = False
        print("Come frome_n is False. Executing special handling.")
        pass  # Placeholder for special handling
    else:
        print("Come frome_n is False. Executing the if section.")
        # Code for the if section
    
    print("this code is not neccesary")
else:
    print("Inside the else section of the outer if statement")
    # Code for the else section
print("After the outer if statement")
