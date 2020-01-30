const state = {
    user: null,
    followings: null,
    followers: null,
    archive: null
}

const getters = {
    check: state => !! state.user,
    getUser: state => state.user ? state.user : null
}

const mutations = {
    setUser (state, user) {
        state.user = user
    },
    setFollowings(state, followings) {
        state.followings = followings
    },
    setFollowers(state, followers) {
        state.followers = followers
    },
    setArchive(state, archive) {
        state.archive = archive
    }
}

export default  {
    namespaced: true,
    state,
    mutations
}
