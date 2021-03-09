<template>
  <div class="images-grid">
    <div class="images-grid__title">{{ images.length }} images found</div>
    <div class="images-grid__grid">
      <masonry
        :cols="{default: 5, 1000: 4, 800: 3, 400: 2}"
        :gutter="40"
      >
        <div
          class="images-grid__card"
          v-for="img in images.slice(0,50)"
          :key="img"
          @click="setImage(img)"
        >
          <img
            :src="img"
            alt=""
          >
        </div>
      </masonry>
    </div>
  </div>
</template>

<script>
  import { mapActions } from 'vuex'
  export default {
    name: "ImagesGrid",
    props: {
      images: {
        type: Array,
        default: () => ([])
      },
    },
    methods: {
      ...mapActions(['setImage'])
    }
  }
</script>

<style scoped lang="scss">
  .images-grid {
    margin-bottom: 20px;
    overflow: scroll;
    &__title {
      font-weight: bold;
      margin-bottom: 20px;
    }
    &__card {
      position: relative;
      width: 100%;
      /*padding-bottom: 100%;*/
      margin-bottom: 40px;
      border-radius: 12px;
      background: #e5e5e5;
      overflow: hidden;
      transition: transform 0.3s;
      cursor: pointer;

      img {
        width: 100%;
        left: 0;
        top: 0;
        height: 100%;
        /*position: absolute;*/
        object-fit: cover;
      }

      &:hover {
        transform: scale(1.05);
      }
    }
  }
</style>
