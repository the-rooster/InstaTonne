# InstaTonne
distributed social media app for CMPUT404 :)


For frontend developers:
Our Vue frontend supports eslint. To use it, open up the "InstaTonne-FrontEnd" folder is VSCode.
(note: opening up a higher level folder means the auto linting will not work)

Then, install the official eslint extension: https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint  

Edit ESLint's settings.json file and add the following to auto lint Vue and JS files on save:  
"editor.codeActionsOnSave": {  
        "source.fixAll.eslint": true  
    },  
"eslint.validate": [  
        "javascript",  
        "vue"  
    ]

Files should now lint automatically when saved

To run the frontend, open a terminal in "InstaTonne-FrontEnd" and enter "npm run dev" to launch on localhost

Note: eslint does not like debuggers. To use a debugger, be sure to disable the restriction:
debugger; // eslint-disable-line no-debugger