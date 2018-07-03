---
layout: post
title:  "Ember.js notes"
date:  2018-06-30 23:00:00 +0800
categories: dev
tags:
 - Ember.js
---

## install ember

```
npm install -g ember-cli
```

## new project

```
ember new devops-dashboard
cd devops-dashboard
ember serve 
```

## new route

```
ember generate route projects

# update index template application.hbs
{{!-- The following component displays Ember's default welcome message. --}}
{{!-- {{welcome-page}} --}}
{{!-- Feel free to remove this! --}}
<h1>DevOps Dashboard</h1>
{{outlet}}

# update project.hbs:
<h2>projects</h2>
<ul>
    {{#each model as |p|}}
        <li>{{p}}</li>
    {{/each}}
</ul>

# update projects.js to provide modeling:
import Route from '@ember/routing/route';

export default Route.extend({
    model() {
        return ['java-project-A', 'python-project-B', 'emberjs-project-C'];
    }
});

```

now we get a /projects page contains a list of projects. 


## setup default route
now I want to set the /projects as the index:

```
# vi routes/index.js
import Route from '@ember/routing/route';

// https://guides.emberjs.com/release/routing/redirection/#toc_transitioning-before-the-model-is-known
export default Route.extend({
  beforeModel(/* transition */) {
    this.transitionTo('projects'); // Implicitly aborts the on-going transition.
  }
});

```

## fetch data from http as modeling

```
# use github/python projects as modeling
# projects.js
import Route from '@ember/routing/route';

export default Route.extend({
    model() {
        // return ['java-project-A', 'python-project-B', 'emberjs-project-C'];
        return $.getJSON("https://api.github.com/orgs/python/repos");
    }
});


# show project names in projects.hbs
<h2>projects</h2>
<ul>
    {{#each model as |p|}}
        <li>{{p.name}}</li>
    {{/each}}
</ul>

```

now our app lists all projects belongs to github/python.

## create sub-route for project details

```
ember generate route projects/view

# add link from projects to proejct/view
# projects.hbs

<h2>projects</h2>
<ul>
    {{#each model as |p|}}
        <li>{{#link-to "projects.view" p.id}} {{p.name}} {{/link-to}}</li>
    {{/each}}
</ul>

{{outlet}}


# route.js to accpet parameter from link
Router.map(function() {
  this.route('projects', function() {
    this.route('view', {path: '/:id'});
  });
});


# view.js to collect parameters 
import Route from '@ember/routing/route';

export default Route.extend({
    model(params) {
        // Ember.Logger.log("params: " + params.id);
        return params.id;
    }
});


# view.hbs to display
<h3>current project: {{model}}</h3>

```

## stop rendering parents outlet

> Each template will be rendered into the {{outlet}} of its parent route's template. 
> https://guides.emberjs.com/release/routing/rendering-a-template/

we don't really need to display the projects list in `projects/view`, so:
https://stackoverflow.com/questions/32160056/ember-how-not-to-render-parents-template

```
ember generate route projects/index

// migrate code from projects.js/projects.hbs to projects/index.js(.hbs)
```

## add bootstrap

```
ember install ember-bootstrap
// then restart ember server
```

## add static file

```
mkdir public/assets
vi public/assets/data/projects.json

// use in js:
 // return $.getJSON("https://api.github.com/orgs/python/repos");
  return $.getJSON("/assets/data/projects.json");
```




