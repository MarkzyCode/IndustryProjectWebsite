# IndustryProjectWebsite

download node.js

npm install
npm install -g @azure/static-web-apps-cli  

cd industry-app

npx swa start -- local dev
npx swa build -- build app
npx swa -- build and deploy
npx swa deploy -- deploy to azure

Not starting? run these commands:
rm -rf node_modules
rm -rf .vite
npm install