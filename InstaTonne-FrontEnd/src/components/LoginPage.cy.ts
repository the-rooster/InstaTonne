import LoginPage from './LoginPage.vue'

describe('<LoginPage />', () => {
  it('renders', () => {
    cy.intercept('GET', '/csrf/', []).as('getCSRF')
    // see: https://on.cypress.io/mounting-vue
    cy.mount(LoginPage)
  })
})