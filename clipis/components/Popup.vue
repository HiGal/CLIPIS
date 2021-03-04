<template>
  <div class="popup">
    <div class="popup__body">
      <div class="popup__title">
        <span>{{ image.split('/').slice(-1)[0] }}</span>
        <img
          src="~/assets/cross.svg"
          alt="Cross"
          @click="setImage()"
        >
      </div>
      <img class="popup__image" :src="image" alt="image">
    </div>
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex'
  export default {
    name: "Popup",
    computed: {
      ...mapState({
        image: (state) => state.image
      })
    },
    methods: {
      ...mapActions(['setImage'])
    }
  }
</script>

<style scoped lang="scss">
  .popup {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    z-index: 10000;

    &__body {
      position: absolute;
      left: 32px;
      top: 32px;
      width: calc(100% - 64px);
      height: calc(100% - 64px);
      background: white;
      border-radius: 12px;
      padding: 40px;
      box-sizing: border-box;

      @media screen and (max-width: 767px){
        padding: 10px;
        left: 10px;
        top: 10px;
        width: calc(100% - 20px);
        height: calc(100% - 20px);
      }
    }
    &__title {
      font-weight: bold;
      margin-bottom: 40px;
      display: flex;
      justify-content: space-between;
      img {
        cursor: pointer;
      }
    }
    &__image {
      width: 100%;
      object-fit: contain;
    }
  }
</style>
