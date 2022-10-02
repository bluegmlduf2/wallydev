<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="290">
      <v-alert :type="dialogType" class="ma-0">
        <v-row align="center" justify="center">
          <v-col> {{ dialogMessage }} </v-col>
          <v-btn icon @click="closeDialog()">
            <v-icon>mdi-close-thick</v-icon>
          </v-btn>
        </v-row>
      </v-alert>
    </v-dialog>
  </v-row>
</template>

<script>
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'Alert',
  props: {
    isOpen: {
      type: Boolean,
      default: false,
    },
    // success,info,warning,error의 4가지 타입이 있다
    dialogType: {
      type: String,
      default: 'info',
    },
    dialogMessage: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      dialog: false,
    }
  },
  watch: {
    // data에 직접 isOpen을 할당하면 변경을 인식하지 못하여 watch를 사용
    isOpen() {
      // 에러메세지가 아닌 경우 1.5초뒤에 메세지가 닫힌다
      if (this.dialogType!=='error') {
        setTimeout(() => {
          this.$emit('closeDialog')
        }, 1500);
      }
      this.dialog = this.isOpen
    },
  },
  methods: {
    closeDialog() {
      this.$emit('closeDialog')
    },
  },
}
</script>
<style scoped>
.success {
  background-color: #4caf50 !important;
  border-color: #4caf50 !important;
}
.info {
  background-color: #2196f3 !important;
  border-color: #2196f3 !important;
}
.warning {
  background-color: #fb8c00 !important;
  border-color: #fb8c00 !important;
}
.error {
  background-color: #ff5252 !important;
  border-color: #ff5252 !important;
}
</style>