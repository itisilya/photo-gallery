<!-- src/App.vue -->
<template>
  <div id="app">

    <router-view />
  </div>
</template>

<style>
#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
nav {
  padding: 20px;
  background: #42b883;
}
nav a {
  color: white;
  text-decoration: none;
  font-weight: bold;
  margin-right: 20px;
}
</style>
