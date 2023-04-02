# InstaTonne
[InstaTonne](https://cmput404-group6-instatonne.herokuapp.com/app/) is a revolutionary social networking app that embraces the interconnectedness and the web's peer-to-peer nature. Our aim is to provide users with more autonomy and choice while connecting them to various independent social networks without being limited to a single platform like Facebook, Instagram or Twitter.

Join us in redefining the social networking experience by taking control of your own content and connections. Welcome to InstaTonne!

## Working Website
Access the live website at: https://cmput404-group6-instatonne.herokuapp.com/app/

## Features
- Importing posts from various sources like GitHub and other social networks
- Distribution and sharing of posts and content across different servers
- Aggregating friends' posts from other servers
- Inbox model for sharing posts directly with friends

## Technologies
- Django
- Vue
- Deployed on Heroku
- JavaScript
- Python3

## How to run locally
 - Clone this repository
 - Install dependencies with pip install -r requirements.txt
 ### Run admin
 - Load data
   - `python3 manage.py makemigrations`
   - `python3 manage.py migrate --run-syncdb`
   - `python3 manage.py loaddata initial_data.json`
 - Run the Django server with python manage.py runserver
 - Access the admin at http://127.0.0.1:8000/
 ### Run app
 - Open a new terminal and change to the InstaTonne-Frontend directory
 - Run `npm i` then `npm run dev`
 - Access the locally running app with sample data at http://127.0.0.1:5173/
 
## Running Tests
Run tests with python manage.py test

## OpenAPI Specification
Find the OpenAPI Specification at: https://cmput404-group6-instatonne.herokuapp.com/docs/

## Video
Watch our demonstration video at: (add link to video)

## Contributors
 - culberso
 - lmvaugha
 - mrudolf
 - diep
 - rjg

## License
This project is forked from [CMPUT404-project-socialdistribution](https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org) and is released under the W3C Software and Document Short Notice.

   - Parts of this document are derived from the W3C Documentation for Activity Pub
   - Copyright © 2018 W3C® (MIT, ERCIM, Keio, Beihang). W3C liability, trademark and permissive document license rules apply. 
   - https://www.w3.org/Consortium/Legal/2015/copyright-software-and-document
```License
     
By obtaining and/or copying this work, you (the licensee) agree that you have read, understood, and will comply with the following terms and conditions.
     
Permission to copy, modify, and distribute this work, with or without modification, for any purpose and without fee or royalty is hereby granted, provided that you include the following on ALL copies of the work or portions thereof, including modifications:
     
The full text of this NOTICE in a location viewable to users of the redistributed or derivative work.
Any pre-existing intellectual property disclaimers, notices, or terms and conditions. If none exist, the W3C Software and Document Short Notice should be included.Notice of any changes or modifications, through a copyright statement on the new code or document such as "This software or document includes material copied from or derived from [title and URI of the W3C document]. Copyright © [YEAR] W3C® (MIT, ERCIM, Keio, Beihang)." 
     
Disclaimers
     
THIS WORK IS PROVIDED "AS IS," AND COPYRIGHT HOLDERS MAKE NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO, WARRANTIES OF MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF THE SOFTWARE OR DOCUMENT WILL NOT INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADEMARKS OR OTHER RIGHTS.
     
COPYRIGHT HOLDERS WILL NOT BE LIABLE FOR ANY DIRECT, INDIRECT, SPECIAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF ANY USE OF THE SOFTWARE OR DOCUMENT.
     
The name and trademarks of copyright holders may NOT be used in advertising or publicity pertaining to the work without specific, written prior permission. Title to copyright in this work will at all times remain with copyright holders.```

