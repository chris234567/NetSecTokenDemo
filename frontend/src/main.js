import { Buffer } from "buffer";
globalThis.Buffer = Buffer;
import { createApp, h } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import App from "./App.vue";
import Vuex from "vuex";
import store from "./store";
import uuid from "vue-uuid";
import Login from "./components/Login.vue";


const router = createRouter({
  history: createWebHistory(),
  routes: [
    { 
      path: "/", 
      name: "Home", 
      component: Login 
    },
  ],
});

const app = createApp({
  router,
  render: () => h(App),
  components: { App },
});

app.use(router);
app.use(uuid);
app.use(store);
app.use(Vuex);
app.mount("#app");
