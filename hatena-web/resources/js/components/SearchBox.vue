<template>
    <div class="grid__item">
        <form class="form" @submit.prevent="search">
            <div class="form__item">
                <input id="keyword" type="text" size="25" placeholder="キーワード検索" v-model="keyword">
                <button type="submit" class="button button--inverse">Submit</button>
            </div>
        </form>
    </div>
</template>
<script>
    import {OK} from "../util";
    export default {
        data() {
            return {
                keyword: '',
            }
        },
        methods: {
            async search () {
                const response = await axios.get(`/api/users/${this.keyword}`)

                if (response.status !== OK) {
                    return false
                }

                this.$store.commit('user/setUser', response.data)

                this.getArchive()
                this.getFollowings()
                this.getFollowers()
            },
            async getFollowings() {
                const response = await axios.get(`/api/users/${this.keyword}/followings`)

                if (response.status !== OK) {
                    return false
                }
                this.$store.commit('user/setFollowings', response.data.data)
            },
            async getFollowers() {
                const response = await axios.get(`/api/users/${this.keyword}/followers`)

                if (response.status !== OK) {
                    return false
                }
                this.$store.commit('user/setFollowers', response.data.data)
            },
            async getArchive() {
                const response = await axios.get(`/api/users/${this.keyword}/archive`)

                if (response.status !== OK) {
                    return false
                }
                console.log(response.data)
                this.$store.commit('user/setArchive', response.data)
            }
        },
        computed: {
            getUser: function getUser() {
                return this.$store.getters['user/getUser'];
            }
        }
    }
</script>
