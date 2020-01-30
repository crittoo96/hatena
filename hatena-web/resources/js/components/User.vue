<template>
    <div v-if="user" class="panel">
        <div class="user-icon">
            <img v-lazy="user.icon" />
        </div>
        <div class="user-id">
            <p>{{ user.id }}</p>
        </div>
        <div class="user-bio">
            <p>{{ user.bio }}</p>
        </div>
        <div class="user-url">
            <p><a :href="user.url">{{ user.url }}</a></p>
        </div>
        <div class="user-follower-count" style="display: flex">
            <div><b>{{ user.followings_count }}</b> フォロー中 <b>{{ user.followers_count }}</b> フォロワー</div>
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            user: null
        }
    }
</script>
