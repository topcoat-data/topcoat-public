<template>
    <div>
        {{ text }}
    </div>
</template>

<script>
    export default {
        props: {
            seperator: {
                type: String,
                default: ' ',
            },
            showTime: Boolean,
            showDate: {
                type: Boolean,
                default: true,
            }
        },
        data: () => ({
            text: '',
        }),
        mounted() {
            const today = new Date();
            const s = this.seperator;
            if (this.showDate) {
                let date = today.getDate();
                date = date < 10 ? `0${date}` : date;

                let month = today.getMonth() + 1;
                month = month < 10 ? `0${month}` : month;

                let year = today.getFullYear();
                this.text = `${year}${s}${month}${s}${date}`
            }

            if (this.showTime) {
                let hour = today.getHours();
                let minutes = today.getMinutes();
                let startSeperator = this.showDate ? ' ' : '';
                this.text += `${startSeperator}${hour}${s}${minutes}`;
            }
            
        }
    }
</script>