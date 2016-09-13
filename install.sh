#! /bin/bash

python=$(python -c "import sys; v=sys.version_info; print('python'+str(v[0])+'.'+str(v[1]))")
version="1.1.0"

cp -v   releases/$version/venc.py    	/usr/bin/venc
cp -vR  releases/$version/VenC       	/usr/lib/$python/
cp -vR  src/share/*    			/usr/share/VenC
chmod +rx     /usr/bin/venc
chmod +rx     /usr/lib/$python/VenC
chmod +rx -R  /usr/share/VenC
chmod +rx     /usr/lib/$python/VenC/languages
chmod +rx     /usr/lib/$python/VenC/*.py
chmod +rx     /usr/lib/$python/VenC/languages/*.py
