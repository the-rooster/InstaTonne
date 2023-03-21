#!/bin/bash

# build script for the front end. run from project root directory!
cd 'InstaTonne-FrontEnd'
npm run build
rm -r -f ../templates
mkdir ../templates
mv dist/* ../templates/
echo DONE!