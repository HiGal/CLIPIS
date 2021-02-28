<template>
  <div class="core">
    <AppBackground/>
    <div
      class="block"
      :class="{'block--dragover': dragOver}"
      @dragover="dragOver = true"
      @dragleave="dragOver = false"
    >
      <div class="block__title" v-if="!dragOver">
        CLIPIS
      </div>
      <div class="block__subtitle" v-if="!dragOver">
        The next-era image search
      </div>
      <div class="block__input">
        <span v-if="!dragOver">Enter your text query</span>
        <input v-if="!dragOver" type="text" placeholder="Kitties in the garden...">
        <span>or drag an image here</span>
      </div>
      <span>Farit Galeev, Arina Kuznetsova, Mikhail Tkachenko, 2021</span>
    </div>
  </div>
</template>

<script>
  import AppBackground from '~/components/AppBackground'

  export default {
    components: {AppBackground},
    data: () => ({
      dragOver: false
    })
  }
</script>

<style lang="scss">
  .core {
    position: relative;
    overflow: hidden;
    width: 100vw;
    height: 100vh;
  }

  .block {
    position: absolute;
    height: 322px;
    z-index: 1000;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 500px;
    background: rgba(255, 255, 255, 0.55);
    padding: 20px;
    border-radius: 10px;
    box-sizing: border-box;
    font-family: Roboto, sans-serif;

    &--dragover {
      border: 3px dashed #00AAEE;
    }

    &__title {
      color: black;
      font-weight: bold;
      font-size: 40px;
      width: 100%;
    }

    &__subtitle {
      margin-top: 8px;
      font-size: 18px;
      width: 100%;
    }

    &__input {
      margin: 40px 0;
    }

    input {
      padding: 16px;
      box-sizing: border-box;
      border: 1px solid #eeeeee;
      width: 100%;
      border-radius: 6px;
      outline: none;
      margin: 10px 0;
    }

    span {
      color: rgba(0, 0, 0, 0.8)
    }
  }
</style>

