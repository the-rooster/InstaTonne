#!/bin/bash

# build script for the front end. run from project root directory!
cd 'InstaTonne-FrontEnd'
npm run build
mkdir ../templates
mv dist/* ../templates/
echo DONE!