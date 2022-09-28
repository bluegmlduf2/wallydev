<template>
  <div>
    <editor-content :editor="editor" />
  </div>
</template>

<script>
import { Editor, EditorContent } from '@tiptap/vue-2'
import { StarterKit } from '@tiptap/starter-kit'
import { Image } from '@tiptap/extension-image'

export default {
  components: {
    EditorContent,
  },

  props: {
    content: {
      type: String,
      default: '',
    },
  },

  data() {
    return {
      editor: null,
      editable: false,
    }
  },

  mounted() {
    this.editor = new Editor({
      content: this.content,
      editable: false,
      extensions: [
        StarterKit,
        Image.configure({
          inline: true, // p태그안에 img태그를 렌더링한다
          allowBase64: true,
        }),
      ],
    })
  },

  beforeDestroy() {
    this.editor.destroy()
  },
}
</script>