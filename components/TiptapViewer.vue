<template>
  <div>
    <editor-content :editor="editor" />
  </div>
</template>

<script>
import { Editor, EditorContent } from '@tiptap/vue-2'
import { StarterKit } from '@tiptap/starter-kit'
import { Image } from '@tiptap/extension-image'
import { Underline } from '@tiptap/extension-underline'

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
        Underline,
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
<style lang="scss">
// 아래의 내용들은 editor와 viewer에 둘다 적용됨
.ProseMirror {
  p {
    line-height: 1.75rem;
  }
  
  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    line-height: 3rem;
  }

  code {
    border-radius: 0.375rem;
    display: block;
    white-space: pre-wrap;
    font-size: 0.9rem;
    padding: 0.75rem 0.75rem;
    margin: 0.5rem 0;
    background-color: #1f2937 !important;
    color: #e5e7eb !important;
  }
  img {
    max-width: 800px;
    height: auto;
  }
}
</style>