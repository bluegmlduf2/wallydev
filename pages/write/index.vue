<template>
  <div>
    <client-only>
      <tiptap-editor />
    </client-only>
  </div>
</template>
<script>
import TiptapEditor from '~/components/TiptapEditor.vue'

export default {
  name: 'IndexPage',
  components: {
    TiptapEditor,
  },
  middleware: ['auth', 'check-admin'],
}
</script>