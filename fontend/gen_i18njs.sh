#!/bin/sh

cd `dirname $(realpath $0)`/src/i18n/

[ -z "$1" ] && echo "Usage: $0 <localefilename>" && exit 1
[ -f "$1.js" ] && echo "Locale file $1.js is existed" && exit 1

echo -e "const title = ''\n\
\n\
const message = {\n\
    warninfo: {\n\
        l1: '',\n\
        l1Strong: '',\n\
        l2: '',\n\
        l3: '',\n\
        l4: ''\n\
    },\n\
    inputTitle: '',\n\
    loadImages: '',\n\
    commit: '',\n\
    speedLimit: '',\n\
    result: '',\n\
    cover: '',\n\
    linkList: '',\n\
    inputErrorMsg: '',\n\
    warning: '',\n\
    loadImageIsOpen: '',\n\
    loadFailed: '',\n\
    failToConnect: '',\n\
    failUnknownError: '',\n\
    loadSuccess: '',\n\
    loadFromCache: '',\n\
    loadFromWeb: '',\n\
}\n\
\n\
export default { title, message }" > "${1}.js"

[ $? -ne 0 ] && echo "Create ${1}.js failed" && exit 1

headcommitline=$(grep -E "^//" index.js | wc -l)
importlines=$(grep -Ev "^//" index.js | grep -n "import" -A 1 | tac | head -1|cut -d'-' -f1)
[[ ! "$importlines" =~ ^[0-9]+$ ]] && echo "Failed to get import line in `realpath index.js`. You need import your locale file into index.js by hand"
let insertImportIn=importlines+headcommitline
sed -i "${insertImportIn}iimport $1 from './$1'" index.js
settingline=$(grep -n "const messages" -A$importlines index.js | tac | head -1 | cut -d'-' -f1)
sed -i "${settingline}i\ \ $1," index.js

echo "Create ${1}.js success. Now you need edit it."