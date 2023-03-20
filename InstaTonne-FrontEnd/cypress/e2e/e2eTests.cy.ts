// import Cookies from "js-cookie";
import { USER_AUTHOR_ID_COOKIE } from "../../src/axiosCalls";

describe('e2e tests', () => {
  it('can login', () => {
    cy.intercept('POST', '/login/', { fixture: '../../src/exampleLoginResponse.json' }).as('getLogin')

    cy.intercept('GET', '/authors/1', { fixture: '../../src/exampleAuthorData.json' }).as('getAuthor')

    cy.intercept('GET', '/authors/1/inbox/', { fixture: '../../src/exampleInbox.json' }).as('getInbox')
  
    cy.intercept('GET', '/csrf/', []).as('getCSRF')

    cy.clearCookie(USER_AUTHOR_ID_COOKIE);

    cy.visit('http://127.0.0.1:5173/')

    cy.get("input#input-0").type("username1")

    cy.get("input#input-2").type("password1")

    cy.contains("Login").click()
    
    cy.get("h1").should("contain", "Your Stream")

    cy.getCookie(USER_AUTHOR_ID_COOKIE).should("have.property", "value", "1")

    cy.clearCookie(USER_AUTHOR_ID_COOKIE);
  })
})