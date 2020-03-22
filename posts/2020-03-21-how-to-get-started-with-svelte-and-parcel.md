---
title: How to get started with Svelte and Parcel
---

Assuming that you already have `npm` installed, then creating and publishing a new website is really easy and fast.

Here's the minimal steps needed to get a website created with Svelte.js and Parcel.js:

## Walkthrough
1. Create a new npm project: `mkdir my-project && cd my-project && npm init -y`
2. Install dependencies: `npm i -D svelte parcel-bundler parcel-plugin-svelte @babel/polyfill`
3. Create 'index.html' with the following code:

        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1.0" />
          <meta http-equiv="X-UA-Compatible" content="ie=edge" />
          <title>Parcel Plugin Svelte Example</title>
        </head>
        <body>
        <div id="demo"></div>

        <!-- This script tag points to the source of the JS file we want to load and bundle -->
        <script src="main.js"></script>
        </body>
        </html>

4. Create 'main.js':

        import '@babel/polyfill';
        import App from "./App.svelte";

        const app = new App({
          target: document.getElementById('demo'),
          data: {
            name: 'world'
          }
        });

5. Create 'App.svelte':

        <p>Hello, {name}!</p>
        
        <script>
          export let name = 'Anonymous';
        </script>

6. Update the 'script' block in 'package.json':

          "scripts": {
            "start": "parcel index.html",
            "build": "parcel build index.html"
          }

7. Run the app locally: `npm run start`
8. Go to localhost to see your site (i.e., http://localhost:1234) and you should see the output `Hello, Anonymous!`

**Bonus**

How to easily deploy the Svelte app:
1. Install Surge dependency: `npm i --global surge`
2. Deploy: `cd dist && surge`, then complete the interactive prompts, including choosing a subdomain of surge.sh
3. Go to the domain you specified and see the output `Hello, Anonymous!`

## Resources
- [Svelte](https://svelte.dev/)
- [Parcel](https://parceljs.org/)
- [Surge](https://surge.sh/)
