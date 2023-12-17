<template>
    <div>
        <label>Username</label>
        <input v-model="username"/>
    </div>
    <div>
        <label>Passwort</label>
        <input v-model="password"/>
    </div>
    <button @click="login()">Login</button>

    <div>
        {{ this.loggedInUser }} möchte {{ this.giftCount }} Geschenke zu Weihnachten haben! wow...
    </div>

    <button @click="increment()">Mehr!</button>

</template>

<script>

export default {
    mounted: function () {
        this.$store.dispatch('getUser')
        .then((user) => { 
            this.loggedInUser = user;

            this.$store.dispatch('getCount', { 
                username: user
            })
            .then((count) => { this.giftCount = count })
        })
    },
    components: { },
    data() {
        return {
            username: "",
            password: "",
            loggedInUser: "[Undefined]",
            giftCount: "[Undefined]",
        }
    },
    methods: {
        login() {
            this.$store.dispatch('login', { 
                username: this.username, 
                password: this.password 
            })
        },
        increment() {
            this.$store.dispatch('increment', { 
                username: this.loggedInUser, 
            })
        }
    }
}
</script>

<style>
</style>
