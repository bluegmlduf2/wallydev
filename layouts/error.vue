<template>
  <v-app>
    <div class="mt-10">
      <div class="d-flex justify-center align-center">
        <div class="text-h5">페이지를 찾을 수 없습니다</div>
      </div>
      <div class="d-flex justify-center align-center text-Subtitle-1">
        <NuxtLink to="/"> 여기 </NuxtLink>를 클릭하여 홈화면으로 이동해주세요
      </div>
    </div>
  </v-app>
</template>

<script>
export default {
  name: 'EmptyLayout',
}
</script>
