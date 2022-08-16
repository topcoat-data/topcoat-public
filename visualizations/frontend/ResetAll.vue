<template>
<button @click="handleClick">yo it's me. A nasty button</button>
</template>

<script>
    export default {
        props: {
            text: {
                type: String,
                default: 'nasty'
            },
        },
        methods: {
            handleClick(e) {
                console.log('event in ResetAll', e)
            }
        }
    }
</script>
