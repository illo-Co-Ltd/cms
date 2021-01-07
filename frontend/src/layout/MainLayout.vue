<template>
    <div class="main_container">
        <div class="dir_hierarchy">
            <tree-browser :node="root"
                     @onClick="nodeWasClicked"/>
        </div>
        <div class="image_hierarchy">
            <thumbnail-card></thumbnail-card>
        </div>
    </div>
</template>

<script>
import TreeBrowser from '../components/TreeBrowser.vue';
import ThumbnailCard from '../components/ThumbnailCard.vue'

export default {
    name: 'app',
    data() {
        return {
            root: {
                name: '/',
                children: [
                    {
                        name: 'music',
                        children: [
                            {
                                name: 'song.mp3'
                            }
                        ]
                    },
                    {
                        name: 'workspace',
                        children: [
                            {
                                name: 'source.js'
                            }
                        ]
                    }
                ]
            }
        }
    },
    components: {
        TreeBrowser,
        ThumbnailCard,
    },
    methods: {
        nodeWasClicked(node) {
            alert(node.name);
        }
    },
}
</script>

<style>
.container {
    width:100%;
    height: 100%;
}
.dir_hierarchy {
    border-right: solid;
    border-right-width: thin;
    border-right-color: black;
    background-color: burlywood;
    width: 20%;
    height: 100%;
    min-height: 100vh;
    float: left;
}
.image_hierarchy {
    border-right: solid;
    border-right-width: thin;
    border-right-color: black;
    background-color: rgb(243, 235, 225);
    width: 20%;
    height: 100%;
    min-height: 100vh;
    float: left;
}
</style>
