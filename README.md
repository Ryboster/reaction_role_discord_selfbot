# Discord reaction-role bot

## Setup
1. Install the requirements with 
	```python3 install -r requirements.txt```
2. Fill in the missing information in `./config/config.json`.
3. Start the `bot.py` script.

## Usage
For the simplicity's sake, I am going to assume the prefix of "!" for this portion of the document. If you chose a different prefix, simply replace it.

#### Add observed message
To add the role to the database and respond to its reactions with appropriate roles:
1. Navigate to destination chat,
2. Copy the ID of the desired message
3. With your prefix, enter the following command:
```
!add_reaction_role 1267457847290105866 <3 @myRole
```

#### Reset the database
To reset the database, enter any chat the bot (you) have access to and enter the following command:
```
!drop_db
```
**Note** that only the user with the ID equal to the value of `ADMIN_ID` (as entered in `config.json`) can perform this action.

#### Check the contents of the database
To display the contents of the database in chat in form of a message, type the following command in any accessible chat:
```
!read_from_db
```


**Note** that this is a self bot. Before use check Discord's policy on self bots.
