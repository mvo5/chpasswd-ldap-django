#!/bin/sh

set -e

wget http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/css/bootstrap-combined.min.css
wget http://code.jquery.com/jquery-2.0.3.min.js
echo "Fixing jquery to avoid strange js error!"
awk 'NR != 2' jquery-2.0.3.min.js > jquery.min.js
rm jquery-2.0.3.min.js
wget https://raw.github.com/ablanco/jquery.pwstrength.bootstrap/master/src/pwstrength.js
wget https://raw.github.com/ReactiveRaven/jqBootstrapValidation/master/dist/jqBootstrapValidation-1.3.7.min.js
