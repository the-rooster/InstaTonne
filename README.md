# InstaTonne
distributed social media app for CMPUT404 :)


For frontend developers:
Our Vue frontend supports eslint. To use it, open up the "InstaTonne-FrontEnd" folder is VSCode.
(note: opening up a higher level folder means the auto linting will not work)

Then, install the official eslint extension: http://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint  

Edit ESLint's settings.json file and add the following to auto lint Vue and JS files on save:  
"editor.codeActionsOnSave": {  
        "source.fixAll.eslint": true  
    },  
"eslint.validate": [  
        "javascript",  
        "vue"  
    ]

Files should now lint automatically when saved

To run the frontend, open a terminal in InstaTonne-FrontEnd:
npm i
npm run dev

Note: eslint does not like debuggers. To use a debugger, be sure to disable the restriction:
debugger; // eslint-disable-line no-debugger

Frontend tests: npm run test. Runs tests in watch mode.

Cypress E2E testing:

To reset to the test db:
1. delete pycache from Instatonne-Apis, and the db file
2. python3 manage.py makemigrations InstaTonneApis
3. python3 manage.py migrate --run-syncdb
4. python3 manage.py loaddata test_data.json

5. Run backend: python3 manage.py runserver
6. Run frontend: /InstaTonne-Frontend npm run dev
7. Run Cypress: npx cypress open