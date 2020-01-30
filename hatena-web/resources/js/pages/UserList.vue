<template>
    <div style="display: flex">
        <div style="flex: 1 0 30%;">
            <div>
                <SearchBox/>
                <User
                    v-if="user"
                    :key="user.id"
                    :user="user"
                />
            </div>
        </div>
        <div style="flex: 1 0 5%;"></div>
        <div style="flex: 1 0 65%;">
            <ul class="tab">
                <li
                    class="tab__item"
                    :class="{'tab__item--active': tab === 1 }"
                    @click="tab = 1"
                >
                    アーカイブ
                </li>
                <li
                    class="tab__item"
                    :class="{'tab__item--active': tab === 2 }"
                    @click="tab = 2"
                >
                    フォロー<span v-if="user">({{ user.followings_count }})</span>
                </li>
                <li
                    class="tab__item"
                    :class="{'tab__item--active': tab === 3 }"
                    @click="tab = 3"
                >
                    フォロワー<span v-if="user">({{ user.followers_count }})</span>
                </li>
            </ul>
            <div class="panel" v-show="tab === 1">
                <div v-if="archive !== null">
                    <Post
                        v-for="(post,index) in archive"
                        class="grid__item"
                        :key="index"
                        :post="post"
                    />
                </div>
                <p v-else>アーカイブなし</p>
            </div>
            <div class="panel" v-show="tab === 2">
                <div v-if="followings !== null">
                    <User
                        v-for="(user,index) in followings"
                        class="grid__item"
                        :style="`grid-column: ${index % 2 + 1 }`"
                        :key="user.id"
                        :user="user"
                    />
                    <infinite-loading @infinite="infiniteFollowingsHandler" />
                </div>
                <p v-else>フォローがいません</p>
            </div>
            <div class="panel" v-show="tab === 3">
                <div  v-if="followers !== null">
                    <User
                        v-for="(user,index) in followers"
                        :style="`grid-column: ${index % 2 + 1 }`"
                        :key="user.id"
                        :user="user"
                    />
                    <infinite-loading @infinite="infiniteFollowersHandler" />
                </div>
                <p v-else>フォロワーがいません</p>
            </div>
        </div>
    </div>
</template>
<script>
    import User from "../components/User";
    import SearchBox from "../components/SearchBox"
    import Post from "../components/Post"
    export default {
        components: {User, SearchBox, Post},
        data() {
            return {
                page: 2,
                tab: 1
            }
        },
        methods: {
            infiniteFollowingsHandler($state) {
                axios.get(`/api/users/${this.user.id}/followings`, {
                    params: {
                        page: this.page,
                        per_page: 1
                    }
                }).then(({data}) => {
                    setTimeout(() => {
                        if (data.current_page <= data.last_page) {
                            this.page += 1
                            this.$store.commit('user/setFollowings', this.followings.concat(...data.data))
                            $state.loaded()
                        } else {
                            $state.complete()
                        }
                    }, 200)
                }).catch((err) => {
                    $state.complete()
                });
            },
            infiniteFollowersHandler($state) {
                axios.get(`/api/users/${this.user.id}/followers`, {
                    params: {
                        page: this.page,
                        per_page: 1
                    }
                }).then(({data}) => {
                    setTimeout(() => {
                        if (data.current_page <= data.last_page) {
                            this.page += 1
                            this.$store.commit('user/setFollowers', this.followers.concat(...data.data))
                            $state.loaded()
                        } else{
                            $state.complete()
                        }
                    }, 200)
                }).catch((err) => {
                    $state.complete()
                });
            },
        },
        computed: {
            user() {
                return this.$store.state.user.user
            },
            followings() {
                return this.$store.state.user.followings
            },
            followers() {
                return this.$store.state.user.followers
            },
            archive() {
                return this.$store.state.user.archive
            }
        },
        watch: {
            user () {
                console.log('a');
            },
            archive() {
                console.log(this.archive)
            }
        }
    }
</script>
