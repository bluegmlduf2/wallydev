<template>
  <div>
    <div v-if="editor" class="editor-menu">
      <button
        :disabled="!editor.can().chain().focus().toggleBold().run()"
        :class="{ 'is-active': editor.isActive('bold') }"
        @click="editor.chain().focus().toggleBold().run()"
      >
        bold
      </button>
      <button
        :class="{ 'is-active': editor.isActive('underline') }"
        @click="editor.chain().focus().toggleUnderline().run()"
      >
        underline
      </button>
      <button
        :disabled="!editor.can().chain().focus().toggleStrike().run()"
        :class="{ 'is-active': editor.isActive('strike') }"
        @click="editor.chain().focus().toggleStrike().run()"
      >
        strike
      </button>
      <button
        :class="{ 'is-active': editor.isActive('codeBlock') }"
        @click="editor.chain().focus().toggleCodeBlock().run()"
      >
        code
      </button>
      <button
        :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }"
        @click="editor.chain().focus().toggleHeading({ level: 1 }).run()"
      >
        h1
      </button>
      <button
        :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }"
        @click="editor.chain().focus().toggleHeading({ level: 2 }).run()"
      >
        h2
      </button>
      <button
        :class="{ 'is-active': editor.isActive('heading', { level: 3 }) }"
        @click="editor.chain().focus().toggleHeading({ level: 3 }).run()"
      >
        h3
      </button>
      <button
        :class="{ 'is-active': editor.isActive('heading', { level: 4 }) }"
        @click="editor.chain().focus().toggleHeading({ level: 4 }).run()"
      >
        h4
      </button>
      <button
        :class="{ 'is-active': editor.isActive('heading', { level: 5 }) }"
        @click="editor.chain().focus().toggleHeading({ level: 5 }).run()"
      >
        h5
      </button>
      <button
        :class="{ 'is-active': editor.isActive('heading', { level: 6 }) }"
        @click="editor.chain().focus().toggleHeading({ level: 6 }).run()"
      >
        h6
      </button>
      <button
        :class="{ 'is-active': editor.isActive('bulletList') }"
        @click="editor.chain().focus().toggleBulletList().run()"
      >
        bullet list
      </button>
      <button
        :class="{ 'is-active': editor.isActive('orderedList') }"
        @click="editor.chain().focus().toggleOrderedList().run()"
      >
        ordered list
      </button>
      <button @click="editor.chain().focus().setHorizontalRule().run()">
        horizontal rule
      </button>
      <button
        :disabled="!editor.can().chain().focus().undo().run()"
        @click="editor.chain().focus().undo().run()"
      >
        undo
      </button>
      <button
        :disabled="!editor.can().chain().focus().redo().run()"
        @click="editor.chain().focus().redo().run()"
      >
        redo
      </button>
      <button @click="openImage">image</button>
      <input
        ref="fileDialog"
        type="file"
        style="display: none"
        accept="image/*"
        @change="addImage"
      />
    </div>
    <v-row>
      <v-col cols="8">
        <v-text-field
          v-model="title"
          clear-icon="title"
          class="mt-2 title"
          dense
          solo
          hide-details="auto"
          spellcheck="false"
          placeholder="제목을 입력해주세요"
        />
      </v-col>
      <v-col cols="4">
        <v-select
          v-model="selectedItem"
          class="mt-2 category"
          :items="categoryItems"
          dense
          solo
          hide-details="auto"
          placeholder="카테고리를 선택해주세요"
        ></v-select>
      </v-col>
    </v-row>
    <editor-content
      class="content-editor"
      :editor="editor"
      spellcheck="false"
    />
    <div class="d-flex mt-3">
      <v-btn class="text-subtitle-1" @click="$router.go(-1)">뒤로</v-btn>
      <v-spacer />
      <v-btn class="text-subtitle-1" @click="onClickWrite">{{
        isEdit ? '수정' : '등록'
      }}</v-btn>
    </div>
    <Alert
      :is-open="isOpen"
      :dialog-message="dialogMessage"
      dialog-type="error"
      @closeDialog="isOpen = false"
    />
  </div>
</template>

<script>
import { Editor, EditorContent } from '@tiptap/vue-2'
import { StarterKit } from '@tiptap/starter-kit'
import { Image } from '@tiptap/extension-image'
import { Underline } from '@tiptap/extension-underline'
import message from '~/assets/js/message'

export default {
  components: {
    EditorContent,
  },

  middleware: ['auth', 'check-admin'],
  data() {
    return {
      isOpen: false,
      isEdit: false,
      dialogMessage: '',
      title: '',
      content: '',
      editor: null,
      categoryItems: ['today', 'food', 'javascript', 'vuejs', 'php', 'others'],
      selectedItem: 'today',
      tempImages: [],
    }
  },
  computed: {
    post() {
      return this.$store.getters.post
    },
  },
  mounted() {
    // 수정모드에 따라 초기값 설정
    if (this.$route.params?.postId) {
      this.isEdit = true
      this.title = this.post.title
      this.content = this.post.content
      this.selectedItem = this.post.category
    }

    this.editor = new Editor({
      content: this.content,
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

  methods: {
    async onClickWrite() {
      // 작성한 글의 정보
      const param = {
        title: this.title,
        category: this.selectedItem,
        content: this.editor.getHTML(),
        tempImages: this.tempImages,
      }
      // 화면에서 유효성 체크
      if (!param.title && !param.content) {
        this.isOpen = true
        this.dialogMessage = message.inputAll
        return
      }
      // 게시글 수정/등록 여부에따라서 분기
      if (this.isEdit) {
        // 수정할 게시글의 번호의 값을 초기화
        param.postId = this.$route.params.postId
        // 글을 수정
        await this.$store
          .dispatch('updatePost', param)
          .catch((e) => {
            // 서버에서 에러가 발생했을때
            this.isOpen = true
            this.dialogMessage = e.message
          })
          .finally(() => {
            this.$store.commit('SET_LOADING', false)
          })
      } else {
        // 글을 등록
        await this.$store
          .dispatch('createPost', param)
          .catch((e) => {
            // 서버에서 에러가 발생했을때
            this.isOpen = true
            this.dialogMessage = e.message
          })
          .finally(() => {
            this.$store.commit('SET_LOADING', false)
          })
      }
    },
    openImage() {
      this.$refs.fileDialog.click()
    },
    async addImage($event) {
      const file = $event.target.files[0]
      if (file) {
        const formData = new FormData()
        formData.append('image', file)
        // 파일등록 등록
        await this.$store
          .dispatch('uploadImage', formData)
          .then((response) => {
            // 업로드한 임시이미지 표시
            this.editor
              .chain()
              .focus()
              .setImage({ src: response.data.imageUrl })
              .run()
            // 임시이미지를 저장용 이미지로 변환하기 위해 추가
            this.tempImages.push(response.data.imagefileName)
          })
          .catch((e) => {
            // 서버에서 에러가 발생했을때
            this.isOpen = true
            this.dialogMessage = e.message
          })
          .finally(() => {
            this.$store.commit('SET_LOADING', false)
          })
      }
    },
  },
}
</script>
<style scoped>
.editor-menu button {
  padding: 0.25rem;
  margin: 0.1rem;
  border: 1px solid black;
  border-radius: 0.5rem;
}

.title,
.category {
  border: 1px solid black !important;
  border-radius: 0.5rem;
}
/* 수정화면 에디터 */
.content-editor {
  border: 1px solid black;
  border-radius: 0.5rem;
  padding: 1rem;
  min-height: 500px;
  margin-top: 0.5rem;
}
</style>