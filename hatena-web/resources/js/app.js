import './bootstrap'
import Vue from 'vue'
// ルーティングの定義をインポートする
import router from './router'
import store from './store'
// ルートコンポーネントをインポートする
import App from './App.vue'

import VueLazyload from 'vue-lazyload'

import InfiniteLoading from 'vue-infinite-loading';

Vue.use(InfiniteLoading);
Vue.use(VueLazyload, {
    preLoad: 1.3, // 事前ロードする高さの割合指定
    error: '', // エラー時に表示する画像指定
    loading: '', // ロード中に表示する画像指定
    attempt: 1 // ロード失敗した時のリトライの上限指定
});


new Vue({
    el: '#app',
    router, // ルーティングの定義を読み込む
    store,
    components: { App }, // ルートコンポーネントの使用を宣言する
    template: '<App />' // ルートコンポーネントを描画する
})
