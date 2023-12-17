import Vuex from "vuex";
import axios from "../axios-auth";


export default new Vuex.Store({
  state: {
    jwt: { "token": sessionStorage.getItem("token") }
  },
  getters: { },
  mutations: {
    setJwtToken(state, payload) {
      sessionStorage.token = payload.jwt.token
      state.jwt = payload.jwt
    }
  },
  actions: {
    getUser({ state }) {
      return new Promise((resolve, reject) => {
        axios
          .get("/user", { headers: { Authorization: `Bearer: ${state.jwt.token}`} })
          .then((res) => {
            resolve(res.data);
          })
          .catch(() => {
            reject();
          });
      });
    },
    increment({ state }, user) {
      return new Promise((resolve, reject) => {
        axios
          .put("/count", user, { headers: { Authorization: `Bearer: ${state.jwt.token}` } }) 
          .then(() => {
            resolve();
          })
          .catch(() => {
            reject();
          });
      });
    },
    getCount({ state }, user) {
      return new Promise((resolve, reject) => {
        axios
          .get("/count", { params: user, headers: { Authorization: `Bearer: ${state.jwt.token}`} })
          .then((res) => {
            resolve(res.data);
          })
          .catch(() => {
            reject();
          });
      });
    },
    login({ commit }, userData) {
      return new Promise((resolve, reject) => {
        axios
          .put("/login", userData)
          .then((res) => {
            commit('setJwtToken', { jwt: res.data })
            resolve(res);
          })
          .catch(() => {
            reject();
          });
      });
    },
  },
});
