import PostEditor from './PostEditor.vue'
import ExamplePost from '../examplePost.json'

describe('<PostEditor />', () => {
  it('renders', () => {
    const mockSaveFunction = (postInfo) => {
      postInfo.should("exist")
    }

    // see: https://on.cypress.io/mounting-vue
    cy.mount(PostEditor, {
      props: {
        postData: ExamplePost,
        saveFunction: mockSaveFunction
      }
    })
  })
})