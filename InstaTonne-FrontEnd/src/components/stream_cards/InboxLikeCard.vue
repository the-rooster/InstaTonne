<template>
    <v-card class="mx-auto" color="#fff" theme="light" max-width="90%">
      <v-card-actions>
        <v-list-item class="w-100">
          <v-list-item-title>{{ author.displayName }} liked your post</v-list-item-title>
          <template v-slot:append>
            <div class="justify-self-end">
            </div>
          </template>
          <div style="display:flex;flex-direction:row;justify-content:space-between">
            <v-list-item>{{ props.likeData.summary }}</v-list-item>
            <a v-bind:href="postUrl">
                <div class="post-tiny" >
                    <h1
                    style="
                        text-overflow: ellipsis;
                        white-space: nowrap;
                        max-width: 100%;
                        overflow: hidden;
                    "
                    >
                    {{ postData.title }}
                    </h1>
                    <span
                    style="
                        text-overflow: ellipsis;
                        white-space: nowrap;
                        max-width: 100%;
                        overflow: hidden;
                    "
                    >{{ postData.description }}</span>
                </div>
            </a>
            </div>

        </v-list-item>
      </v-card-actions>
    </v-card>
  </template>
  
  <script setup lang="ts">
  import { onBeforeMount } from "vue";
import { createHTTP } from "../../axiosCalls";
  import { defineProps, ref, toRaw } from "vue";
  
  const postData = ref({});
  const postUrl = ref({});
  let author = ref({});

  const props = defineProps({
    likeData: {
      type: Object,
      required: true,
    },
  });

  onBeforeMount(() => {

    let postId : string = props.likeData.object;

    let groups = postId.match(/http:\/\/(.*)\/authors\/(?<authorId>.*)\/posts\//)?.groups;


    
    let authorId = "";

    if (groups){
        authorId = groups.authorId;
    }

    

    console.log("POSTID",postId);
    console.log("AUTHORID",authorId);
    createHTTP(`authors/${authorId}/posts/${postId}`).get()
    .then((result) => {
        console.log("POST",result.data)
        postData.value = result.data;
    })

    createHTTP(`authors/${props.likeData.author}/`)
    .get()
    .then((response) => {
      console.log(response.data, 51515);
      author.value = response.data;
      console.log(response.data, 567);
      postUrl.value=`authors/${encodeURIComponent(author.value.id)}/posts/${encodeURIComponent(postId)}/`;
    });
  })
  
  console.log(toRaw(props.likeData).id, 555);
  


  // defineProps<{ msg: string }>();
  </script>
  
  <style scoped>
  .read-the-docs {
    color: #888;
  }

  .post-tiny {
    border: 0.2em solid black;
    padding: 1em;
    margin: 1em;
    width: 10vw;
    height: 10vw;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-size: 60%;
  }
  </style>
  