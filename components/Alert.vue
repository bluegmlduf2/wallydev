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