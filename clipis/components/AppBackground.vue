<template>
  <div class="app-background">
    <masonry>
      <img
        v-for="i in 60"
        :src="`https://picsum.photos/200/300?random=${i}`"
        :alt="i"
      >
    </masonry>
  </div>
</template>

<script>
  export default {
    name: "AppBackground",
  }
</script>

<style scoped>
.app-background {
  width: 200vw;
  height: 200vh;
  left: -50%;
  top: -50%;
  position: absolute;
  overflow: hidden;
  filter: blur(5px);
}
</style>
