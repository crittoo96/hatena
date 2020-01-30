<template>
    <div v-if="post">
        <a :href="post.href">
            <div>
                <div class="post-title">
                    <div class="post-title-text">
                        {{ post['entry-title'] }}
                    </div>
                </div>
                <div class="post-content">
                    <div class="post-content-text">
                        {{ post['content'] }}
                    </div>
                </div>
            </div>
        </a>
    </div>
</template>
<script>
    export default {
        props: {
            post: null
        },
    }
</script>
