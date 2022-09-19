<template>
  <div>write</div>
</template>

<script>
export default {
  name: 'IndexPage',
  middleware: ['auth', 'check-admin'],
}
</script>