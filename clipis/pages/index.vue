<template>
  <div class="core">
    <AppBackground/>
    <div
      class="block"
      :class="{'block--content': images.length > 0 && query !== ''}"
      @dragover.stop.prevent="dragOver = true"
    >
      <div
        class="dropzone"
        v-if="dragOver"
        @dragleave.stop.prevent="dragOver = false"
        @drop.prevent="parseImage"
      >
        <img src="~/assets/upload.svg" alt="Upload">
      </div>
      <div class="block__title">
        CLIPIS
      </div>
      <div class="block__subtitle">
        The next-era image search
      </div>
      <div class="block__input">
        <span>Enter your text query</span>
        <input
          v-model="query"
          type="text"
          placeholder="Kitties in the garden..."
        >
        <span>
          Drag your image here or <a href="" @click.prevent="$refs.fileUpload.click()">upload it</a>
        </span>
        <input
          type="file"
          ref="fileUpload"
          class="fileUpload"
          @change="uploadFilesFromInput"
          multiple
        />
      </div>
      <ImagesGrid
          v-if="images.length && query !== ''"
          :images="images"
      />
      <span>Farit Galeev, Arina Kuznetsova, Mikhail Tkachenko, 2021</span>
    </div>
  </div>
</template>

<script>
  import _ from "lodash"
  import AppBackground from '~/components/AppBackground'
  import { getImages, getImagesByImage } from "../api";

  export default {
    components: {AppBackground},
    data: () => ({
      dragOver: false,
      images: [],
      text: '',
      fileName: ''
    }),
    computed: {
      query: {
        get() {
          return this.text || this.fileName || ''
        },
        set(v) {
          this.text = v
          this.fileName = ''
          this.getLocalImages()
        }
      }
    },
    methods: {
      getLocalImages: _.debounce(async function() {
        const { data: { results: images }} = await getImages(this.text)
        this.images = images.map((im) => `https://api.clipis.co/media/thumbs/${im}`)
      }, 400, { leading: false, trailing: true }),
      async getImageImages(base64, name) {
        const { data: { results: images }} = await getImagesByImage(base64, name)
        this.images = images.map((im) => `https://api.clipis.co/media/thumbs/${im}`)
      },
      getBase64Image (f) {
        const reader = new FileReader();
        const self = this
        reader.onload = function () {
          self.dragOver = false
          self.text = ''
          self.fileName = f.name
          const base64 = reader.result.split(',')[1]
          self.getImageImages(base64, f.name)
        };
        reader.readAsDataURL(f);
      },
      uploadFilesFromInput(e) {
        // CAUTION! Only one file can be uploaded
        this.getBase64Image(e.target.files[0]);
      },
      parseImage(e) {
        this.getBase64Image(e.dataTransfer.files[0]);
      }
    },
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
    /*transition: width 0.5s, height 0.5s;*/
    display: flex;
    flex-direction: column;

    @media screen and (max-width: 767px){
        width: 80%;
      }

    &--content {
      width: calc(100vw - 32px);
      height: calc(100vh - 32px);
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
      .fileUpload {
        display: none;
      }
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

  .dropzone {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: #ECE8EF;
    border: 3px dashed #DC493A;
    border-radius: 10px;

    img {
      position: absolute;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
    }
  }
</style>

