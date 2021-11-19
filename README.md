# filevault
Filevault is a secure file manager, accessed via command line. 
This can be used to store your confidential documents, picture, movies, music etc. securely.

All you have to remember is your Master password.
## Demo
![filevault demo](/art/demo.png)

Below the steps it follows to store your documents securely,
  1. Adds random junks to your document (So that, if someone gets access to your system, they wont know which is part of your document and which is a random junk)
  2. Obfuscates your documents by encrypting it with your master password, using cryptography algoritm (If you want to change the algorithm to your favourite one, you can)
  3. Unrecognizaly shreds your document into chunks of same size
  4. Adds random junks to the document name
  5. Encrypts the document name with master password
  6. Shuffles the document name with your master passowrd
  7. Hides it among other documents of same size, in the vault.
and reverse all the above to get your documents in prestine condition, whenever you need.

It does not store any meta data anywhere.

Hence, Unless the adversary knows your master password, it is nearly impossible to get even a glimpse of your vault.
Longer and random password is more secure.

## Commands supported
1. add - To securely store your documents in the vault
2. get - To retrieve files from your vault
3. delete - Delete files in your vault
4. cd - Change directory, to explore your vault file structure
5. mkdir - Create a folder in your vault
6. exit - Exit the vault

## Configure your vault
Update `filevault.config` to customize the settings
